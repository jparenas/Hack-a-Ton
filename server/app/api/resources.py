import os
import json

from amadeus import Client, ResponseError, Location

from pyairports.airports import Airports

from datetime import datetime
from flask import request
from flask_restplus import Resource

from .security import require_auth
from . import api_rest

import requests

amadeus = Client(
    client_id=os.getenv('AMADEUS_API_KEY'),
    client_secret=os.getenv('AMADEUS_SECRET_KEY'),
    #log_level='debug'
)

airports = Airports()

iata_to_cityname = {}
cityname_to_picture = {}

class SecureResource(Resource):
    """ Calls require_auth decorator on all requests """
    method_decorators = [require_auth]

@api_rest.route('/get_flights')
@api_rest.param('origin', 'Origin of the flight')
class FlightResource(Resource):
    """ Unsecure Resource Class: Inherit from Resource """
    def get(self):
        flights = amadeus.shopping.flight_destinations.get(
            origin=request.args.get('origin'), 
            maxPrice=float(request.args.get('budget')), 
            departureDate=request.args.get('start_date'), 
            duration=int(request.args.get('end_date')),
            currency='USD'
        ).result
        result = []
        for flight in flights['data']:
            if flight['destination'] in iata_to_cityname:
                destination = iata_to_cityname[flight['destination']]
            else:
                destination = amadeus.reference_data.locations.get(
                    keyword=flight['destination'],
                    subType=Location.ANY
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

@api_rest.route('/secure-resource/<string:resource_id>')
class SecureResourceOne(SecureResource):
    """ Unsecure Resource Class: Inherit from Resource """

    def get(self, resource_id):
        timestamp = datetime.utcnow().isoformat()
        return {'timestamp': timestamp}
