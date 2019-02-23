import os
import json
import re
import datetime
import requests

from amadeus import Client, Location, ResponseError, NotFoundError, ServerError

from datetime import datetime
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

iata_to_cityname = {}
cityname_to_picture = {}

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
@api_rest.param('budget', 'Budget of the flight')
@api_rest.param('start_date', 'Start date of the flight')
@api_rest.param('end_date', 'End date of the flight')
class FlightResource(Resource):
    """ Unsecure Resource Class: Inherit from Resource """
    def get(self):
        arguments = {'currency': 'USD'}

        if not request.args.get('origin'):
            return Response(jsonify({'error':'Origin city is obligatory', 'status':400}), status=400, mimetype='application/json')

        arguments['origin'] = request.args.get('origin')

        if request.args.get('budget'):
            arguments['maxPrice'] = abs(int(request.args.get('budget')))

        if request.args.get('start_date'):
            if not check_date(request.args.get('start_date')):
                return Response(jsonify({'error':'Start date is not using the right format', 'status':400}), status=400, mimetype='application/json')
            arguments['departureDate'] = request.args.get('start_date')

        if request.args.get('end_date') and request.args.get('start_date'):
            if not check_date(request.args.get('end_date')):
                return Response(jsonify({'error':'End date is not using the right format', 'status':400}), status=400, mimetype='application/json')

            start_date = datetime.strptime(request.args.get('start_date'), '%Y-%m-%d').date()
            end_date = datetime.strptime(request.args.get('end_date'), '%Y-%m-%d').date()

            if start_date > end_date:
                return Response(jsonify({'error':'End date is earlier than the start day', 'status':400}), status=400, mimetype='application/json')

            difference = end_date - start_date
            arguments['duration'] = difference.days

        try:
            flights = amadeus.shopping.flight_destinations.get(**arguments).result
        except NotFoundError:
            return {'flights': []}
        except ServerError:
            return {'error':500, 'status':'Server Error', 'message':'Probably the city does not exist'}

        result = []
        for flight in flights['data']:
            if flight['destination'] in iata_to_cityname:
                destination = iata_to_cityname[flight['destination']]
            else:
                destination = amadeus.reference_data.locations.get(
                    keyword=flight['destination'],
                    subType=Location.CITY
                )
                if len(destination.result['data']) > 0:
                    destination = destination.result['data'][0]['address']['cityName'].lower()
                    iata_to_cityname[flight['destination']] = destination
                else: 
                    continue

            if destination in cityname_to_picture:
                image_url = cityname_to_picture[destination]
            else:
                json_response = requests.get(f'https://api.teleport.org/api/urban_areas/slug:{destination}/images/')
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
                finally:
                    cityname_to_picture[destination] = image_url

            flight['image'] = image_url
            del flight['type']
            result.append(flight)

        return {'flights': result}

@api_rest.route('/like_place')
class CityLikeResource(Resource):
    """ Unsecure Resource Class: Inherit from Resource """
    def put(self):
        pass

@api_rest.route('/secure-resource/<string:resource_id>')
class SecureResourceOne(SecureResource):
    """ Unsecure Resource Class: Inherit from Resource """

    def get(self, resource_id):
        timestamp = datetime.utcnow().isoformat()
        return {'timestamp': timestamp}
