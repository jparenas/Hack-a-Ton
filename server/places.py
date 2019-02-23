from googleplaces import GooglePlaces, types, lang
import os



# if query_result.has_attributions:
#     print query_result.html_attributions

def get_places():
    API_KEY = os.getenv("GOOGLE_API_KEY")

    google_places = GooglePlaces(API_KEY)

    # You may prefer to use the text_search API, instead.
    query_result = google_places.text_search(location='DePauw University', radius=5)
    # If types param contains only 1 item the request to Google Places API
    # will be send as type param to fullfil:
    # http://googlegeodevelopers.blogspot.com.au/2016/02/changes-and-quality-improvements-in_16.html
    places = query_result.places

    return places