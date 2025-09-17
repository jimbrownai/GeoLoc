from django.shortcuts import render

# Create your views here.
# apps/location/views.py
from django.http import JsonResponse

from .services import get_place_location

from .helpers import find_nearby_airports

def nearby_airports(request):
    lat = request.GET.get("lat")
    lon = request.GET.get("lon")
    max_distance_km = request.GET.get("distance")
    if not lat or not lon:
        return JsonResponse({"error": "Provide lat and lon"}, status=400)

    try:
        lat, lon = float(lat), float(lon), 
        airports = find_nearby_airports(lat, lon,float(max_distance_km))
        return JsonResponse({"airports": airports})
        # name,city,country,iata,distance = find_nearby_airports(lat, lon,float(max_distance_km))
        # return JsonResponse({"name":name,"city":city,"country":country,"iata":iata,"distance_km":distance})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def fetch_location(request):
    """
    GET endpoint:
    ?place=Big_Ben
    """
    place = request.GET.get("place")
    if not place:
        return JsonResponse({"error": "Provide place parameter"}, status=400)

    try:
        place_name, formatted_address,lat,lng = get_place_location(place)

        # location_info = get_place_location(place)
        return JsonResponse({
            "place_name": place_name,
            "formatted_address": formatted_address,
            "lat": lat,
            "lon": lng
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def get_location_details(request):
    return JsonResponse({"country": "United Arab Emirates", "city": "Dubai"})
