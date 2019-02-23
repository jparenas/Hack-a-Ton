import os
import json
import re
import datetime
import requests
import hashlib
import random 

from amadeus import Client, Location, ResponseError, NotFoundError, ServerError

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
class FlightResource(Resource):
    def get(self):
        arguments = {'currency': 'USD'}

        if not request.args.get('origin'):
            return {'error':'Origin city is obligatory', 'status':400}, 400

        if not request.args.get('uuid'):
            return {'error':'UUID is obligatory', 'status':400}, 400

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

        arguments_hash = hashlib.sha256(str(arguments).encode('ascii')).hexdigest()
        db_cursor.execute(f"SELECT query_id, time FROM QUERIES WHERE query_hash=?", (arguments_hash,))

        result = []
        query_cache_result = db_cursor.fetchone()

        if query_cache_result and datetime.strptime(query_cache_result[1], '%Y-%m-%d %H-%M-%S') + timedelta(minutes=cache_timeout) > datetime.utcnow():
            db_cursor.execute(f"SELECT PLAN.start_date, PLAN.end_date, PLAN.origin, PLAN.destination, PLAN.price, CITIES.image FROM PLAN INNER JOIN CITIES ON PLAN.destination = CITIES.iata_name WHERE PLAN.query_id=?", (query_cache_result[0],))
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
            db_cursor.execute("INSERT INTO QUERIES VALUES(?,?,strftime('%Y-%m-%d %H-%M-%S','now'),?,?)", (query_id, uuid, status_code, arguments_hash))
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
                db_cursor.execute('SELECT image FROM CITIES WHERE iata_name=?', (flight['destination'],))
                query_result = db_cursor.fetchone()
                if query_result is None:
                    destination_name = amadeus.reference_data.locations.get(
                        keyword=flight['destination'],
                        subType=Location.CITY
                    )
                    if len(destination_name.result['data']) > 0:
                        destination_name = destination_name.result['data'][0]['address']['cityName'].lower()
                    else: 
                        db_cursor.execute('INSERT INTO CITIES VALUES(?,?,?)', (flight['destination'], flight['destination'], ''))
                        continue

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

                    db_cursor.execute('INSERT INTO CITIES VALUES(?,?,?)', (flight['destination'], destination_name, image_url))
                else:
                    image_url = query_result[0]

                flight['image'] = image_url
                del flight['type']
                del flight['links']
                result.append(flight)

        db_connection.commit()
        return {'flights': result}

@api_rest.route('/like_place')
class CityLikeResource(Resource):
    def post(self):
        data = request.json if request.json else request.form
        print(data)
        print(request.json)
        if 'uuid' not in data:
            return {'error':'UUID is obligatory', 'status':400}, 400
        if 'destination' not in data:
            return {'error': 'destination is required', 'status': 400}, 400
        if 'like' not in data:
            return {'error': 'like status is required', 'status': 400}, 400
        like = True if data['like'] else False

        db_cursor.execute("SELECT last_query FROM USERS WHERE uuid=?", (data['uuid'],))
        query_id = db_cursor.fetchone()[0]
        db_cursor.execute("UPDATE PLAN SET like=? WHERE query_id=? AND destination=?", (like, query_id, data['destination']))

        db_connection.commit()
        
        return {}, 400

"""
@api_rest.route('/secure-resource/<string:resource_id>')
class SecureResourceOne(SecureResource):

    def get(self, resource_id):
        timestamp = datetime.utcnow().isoformat()
        return {'timestamp': timestamp}
"""