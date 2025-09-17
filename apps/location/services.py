import googlemaps 
from django.conf import settings
# apps/location/services.py

def fetch_location_from_gmaps(lat: float, lon: float):
    # TODO: implement Google Maps API call
    return {"country": "United Arab Emirates", "city": "Dubai"}

gmaps_client = googlemaps.Client(key=settings.GMAPS_API_KEY)

def get_place_location(place_name: str):
    """
    Given a place name, return location details including:
    - formatted_address
    - latitude
    - longitude
    """
    geocode_result = gmaps_client.geocode(place_name)
    if not geocode_result:
        raise ValueError(f"No results found for {place_name}")

    result = geocode_result[0]  # Take the first match

    location = result['geometry']['location']
    formatted_address = result.get('formatted_address', place_name)

    # return {
    #     "place_name": place_name,
    #     "formatted_address": formatted_address,
    #     "lat": location['lat'],
    #     "lon": location['lng']
    # }
    return place_name, formatted_address,location['lat'],location['lng']
    