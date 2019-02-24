import os
import json
import re
import datetime
import requests
import hashlib
import random

from amadeus import Client, Location, ResponseError, NotFoundError, ServerError

import googlemaps

from datetime import datetime, timedelta
from flask import request, Response, jsonify
from flask_restplus import Resource

from .security import require_auth
from .database import get_database
from . import api_rest

amadeus = Client(
    client_id=os.getenv('AMADEUS_API_KEY'),
    client_secret=os.getenv('AMADEUS_SECRET_KEY'),
    #log_level='debug'
)

gmaps = googlemaps.Client(key=os.getenv('GOOGLE_MAPS_SERVER_KEY'))

cache_timeout = os.getenv('CACHE_TIMEOUT', 30)

db_connection, db_cursor = get_database()

def check_date(date):
    if re.match(r'\d{4}-\d{2}-\d{2}', date):
        return True
    else:
        return False

class SecureResource(Resource):
    """ Calls require_auth decorator on all requests """
    method_decorators = [require_auth]

@api_rest.route('/get_flights')
@api_rest.param('origin', 'Origin of the flight')
@api_rest.param('uuid', 'UUID of the user')
@api_rest.param('budget', 'Budget of the flight')
@api_rest.param('start_date', 'Start date of the flight')
@api_rest.param('end_date', 'End date of the flight')
@api_rest.param('num_passengers', 'Number of passengers')
class FlightResource(Resource):
    def get(self):
        arguments = {'currency': 'USD', 'nonStop': False}

        if not request.args.get('origin'):
            return {'error':'Origin city is mandatory', 'status':400}, 400

        if not request.args.get('uuid'):
            return {'error':'UUID is mandatory', 'status':400}, 400

        arguments['origin'] = request.args.get('origin')
        uuid = request.args.get('uuid')

        if request.args.get('budget'):
            arguments['maxPrice'] = abs(int(request.args.get('budget')))

        if request.args.get('start_date'):
            if not check_date(request.args.get('start_date')):
                return {'error':'Start date is not using the right format', 'status':400}, 400
            arguments['departureDate'] = request.args.get('start_date')

        if request.args.get('end_date') and request.args.get('start_date'):
            if not check_date(request.args.get('end_date')):
                return {'error':'End date is not using the right format', 'status':400}, 400

            start_date = datetime.strptime(request.args.get('start_date'), '%Y-%m-%d').date()
            end_date = datetime.strptime(request.args.get('end_date'), '%Y-%m-%d').date()

            if start_date > end_date:
                return {'error':'End date is earlier than the start day', 'status':400}, 400

            difference = end_date - start_date
            arguments['duration'] = difference.days

        if request.args.get('num_passengers'):
            num_passengers = abs(int(request.args.get('num_passengers')))
        else:
            num_passengers = 1

        arguments_hash = hashlib.sha256(str(arguments).encode('ascii')).hexdigest()
        db_cursor.execute(f"SELECT query_id, time FROM QUERIES WHERE query_hash=? AND uuid==?", (arguments_hash, uuid))

        result = []
        query_cache_result = db_cursor.fetchone()

        if query_cache_result and datetime.strptime(query_cache_result[1], '%Y-%m-%d %H-%M-%S') + timedelta(minutes=cache_timeout) > datetime.utcnow():
            db_cursor.execute(f"SELECT PLAN.start_date, PLAN.end_date, PLAN.origin, PLAN.destination, PLAN.price, IMAGES.image FROM PLAN INNER JOIN IMAGES ON PLAN.destination = IMAGES.iata_name WHERE PLAN.query_id=?", (query_cache_result[0],))
            for query_result in db_cursor.fetchall():
                flight = {
                    'departureDate': query_result[0],
                    'returnDate': query_result[1],
                    'origin': query_result[2],
                    'destination': query_result[3],
                    'price': {
                        'total': query_result[4],
                    },
                    'image': query_result[5]
                }
                result.append(flight)
        else:

            try:
                flights = amadeus.shopping.flight_destinations.get(**arguments).result
                status_code = 200
            except NotFoundError:
                return {'flights': []}, 201
            except ServerError:
                return {'error':500, 'status':'Server Error', 'message':'Probably the city does not exist'}, 500

            query_id = int(random.getrandbits(256)) % (2 << 63 - 1)
            db_cursor.execute("INSERT INTO QUERIES VALUES(?,?,?,strftime('%Y-%m-%d %H-%M-%S','now'),?,?,?,?,?,?)",
            (
                query_id,
                arguments_hash,
                uuid,
                status_code,
                arguments['origin'],
                request.args.get('budget') if request.args.get('budget') else None,
                request.args.get('start_date') if request.args.get('start_date') else None,
                request.args.get('end_date') if request.args.get('end_date') else None,
                num_passengers
            ))
            db_cursor.execute("INSERT OR IGNORE INTO USERS (uuid, last_query) VALUES (?,?)", (uuid, query_id))
            db_cursor.execute("UPDATE USERS SET last_query=? WHERE uuid=?", (query_id, uuid))

            for flight in flights['data']:
                db_cursor.execute('INSERT INTO PLAN VALUES(?,?,?,?,?,?,?,?)', (
                    flight['departureDate'],
                    flight['returnDate'],
                    flight['origin'],
                    flight['destination'],
                    flight['price']['total'],
                    flight['links']['flightOffers'],
                    None,
                    query_id,
                    ))
                db_cursor.execute('SELECT image FROM IMAGES WHERE iata_name=?', (flight['destination'],))
                query_result = db_cursor.fetchall()
                if query_result == []:
                    destination_name = amadeus.reference_data.locations.get(
                        keyword=flight['destination'],
                        subType=Location.CITY
                    )
                    if len(destination_name.result['data']) > 0:
                        destination_name = destination_name.result['data'][0]['address']['cityName'].lower()
                    else:
                        destination_name = flight['destination']

                    db_cursor.execute('INSERT INTO CITIES VALUES(?,?)', (flight['destination'], destination_name))

                    """
                    json_response = requests.get(f'https://api.teleport.org/api/urban_areas/slug:{destination_name}/images/')
                    try:
                        json_response = json_response.json()
                        if 'status' not in json_response:
                            if len(json_response['photos']) > 0:
                                image_url = json_response['photos'][0]['image']['mobile']
                            else:
                                image_url = json_response['photos']['image']['mobile']
                        else:
                            image_url = ''

                    except json.decoder.JSONDecodeError:
                        image_url = ''
                    """
                    place_id = gmaps.find_place(destination_name, 'textquery')['candidates']
                    if len(place_id) > 0:
                        place_id = place_id[0]['place_id']
                        place_details = gmaps.place(place_id, random.getrandbits(256), ['photo'])
                        images = []
                        if place_details['result'] != {}:
                            for photo in place_details['result']['photos']:
                                image_url = 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=750&photoreference=' + photo['photo_reference'] + '&key=' + os.getenv('GOOGLE_MAPS_SERVER_KEY')
                                images.append(image_url)
                        else:
                            images.append('')
                    else:
                        images.append('')

                    for image in images:
                        db_cursor.execute('INSERT INTO IMAGES VALUES(?,?)', (flight['destination'], image))
                        
                    image_url = random.choice(images)

                else:
                    image_url = random.choice(query_result)[0]

                flight['image'] = image_url
                del flight['type']
                del flight['links']
                result.append(flight)

        for flight in result:
            flight['price']['passenger'] = float(flight['price']['total'])
            flight['price']['total'] = round(float(flight['price']['total']) * num_passengers, 2)

        db_connection.commit()
        return {'flights': result}


@api_rest.route('/like_place')
class CityLikeResource(Resource):
    def post(self):
        data = request.json if request.json else request.form
        if 'uuid' not in data:
            return {'error':'UUID is obligatory', 'status':400}, 400
        if 'destination' not in data:
            return {'error': 'destination is required', 'status': 400}, 400
        if 'like' not in data:
            return {'error': 'like status is required', 'status': 400}, 400
        like = True if data['like'] else False

        db_cursor.execute("SELECT last_query FROM USERS WHERE uuid=?", (data['uuid'],))
        query_id = db_cursor.fetchone()
        if query_id:
            db_cursor.execute("UPDATE PLAN SET like=? WHERE query_id=? AND destination=?", (like, query_id[0], data['destination']))

            db_connection.commit()

            return {}, 200
        else:
            return {'error': 'User does not exist', 'status': 404}, 404

@api_rest.route('/retrieve_previous_search')
@api_rest.param('uuid', 'UUID of the user')
class PreviousSearchResource(Resource):
    def get(self):
        if not request.args.get('uuid'):
            return {'error':'UUID is obligatory', 'status':400}, 400

        db_cursor.execute("SELECT last_query FROM USERS WHERE uuid=?", (request.args.get('uuid'),))
        query_results = db_cursor.fetchone()
        if not query_results:
            result = {
                'error': 'User not found',
                'status': 404
            }
            return result, 404

        db_cursor.execute("SELECT departure, budget, start_day, end_day, num_passengers FROM QUERIES WHERE query_id=?", (query_results[0],))
        query_results = db_cursor.fetchone()
        if query_results:
            result = {
                'departure': query_results[0],
                'budget': query_results[1],
                'start_day': query_results[2],
                'end_day': query_results[3],
                'num_passengers': query_results[4],
            }

            return result
        else:
            result = {
                'error': 'No search found',
                'status': 404
            }
            return result, 404

@api_rest.route('/get_tickets')
@api_rest.param('num_passengers', 'the number of passangers')
@api_rest.param('returnDate', 'the date of arrival')
@api_rest.param('departureDate', 'the date of departure')
@api_rest.param('destination', 'the destination')
@api_rest.param('origin', 'the origin')
class TicketResource(Resource):
    def get(self):
        arguments = {}
        arguments['origin'] = request.args.get('origin')
        arguments['destination'] = request.args.get('destination')
        arguments['departureDate'] = request.args.get('departureDate')
        arguments['returnDate'] = request.args.get('returnDate')

        if request.args.get('num_passengers'):
            num_passengers = request.args.get('num_passengers')
        else:
            num_passengers = 1

        try:
            flights = amadeus.shopping.flight_offers.get(**arguments).result
            status_code = 200
        except NotFoundError:
            return {'flights': []}, 201
        except ServerError:
            return {'error': 500, 'status': 'Server Error', 'message': 'Probably the city does not exist'}, 500
        extracted_flight_list = []
        for offer_item in flights['data']:
            flight_data = {}
            flight_data['price_per_passenger'] = (float(offer_item['offerItems'][0]['price']['total']) + float(offer_item['offerItems'][0]['price']['totalTaxes']))
            flight_data['price_total'] = round(flight_data['price_per_passenger'] * num_passengers, 2)
            
            extracted_flight_list.append(price)
        print(extracted_flight_list)
        return extracted_flight_list, status_code
