from googleplaces import GooglePlaces, types, lang

YOUR_API_KEY = 'AIzaSyDr-4IYXoqdeB7VSMlvLROVfi5Ngn6iYd4'

google_places = GooglePlaces(YOUR_API_KEY)

# You may prefer to use the text_search API, instead.
query_result = google_places.text_search(location='DePauw University', radius=5)
# If types param contains only 1 item the request to Google Places API
# will be send as type param to fullfil:
# http://googlegeodevelopers.blogspot.com.au/2016/02/changes-and-quality-improvements-in_16.html

# if query_result.has_attributions:
#     print query_result.html_attributions


for place in query_result.places:
    # Returned places from a query are place summaries.
    print (place.name)
    print (place.geo_location)
    print (place.place_id)

    # The following method has to make a further API call.
    # place.get_details()
    # Referencing any of the attributes below, prior to making a call to
    # get_details() will raise a googleplaces.GooglePlacesAttributeError.
    # print (place.details) # A dict matching the JSON response from Google.
    # Getting place photos

    for photo in place.photos:
        # 'maxheight' or 'maxwidth' is required
        photo.get(maxheight=500, maxwidth=500)
        # MIME-type, e.g. 'image/jpeg'
        # Image URL
        print(photo.url)
        # Raw image data


# Are there any additional pages of results?
# if query_result.has_next_page_token:
#     query_result_next_page = google_places.nearby_search(
#             pagetoken=query_result.next_page_token)
