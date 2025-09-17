from django.shortcuts import render

# Create your views here.
# apps/flights/views.py
from django.http import JsonResponse

from .services import get_flights

def fetch_flights(request):
    origin = request.GET.get("origin")  # IATA code
    destination = request.GET.get("destination")  # IATA code
    depart_date = request.GET.get("depart_date")
    return_date = request.GET.get("return_date")  # optional
    print(request)
    if not origin or not destination or not depart_date:
        return JsonResponse({"error": "Provide origin, destination, and depart_date"}, status=400)

    try:
        flights = get_flights(origin, destination, depart_date, return_date)
        return JsonResponse({"flights": flights})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)