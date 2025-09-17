from serpapi import GoogleSearch
from django.conf import settings

def get_flights(origin_iata: str, destination_iata: str, depart_date: str, return_date: str = None):
    """
    Fetch flight information using SerpAPI
    """
    params = {
        "engine": "google_flights",
        "departure_id": origin_iata,
        "arrival_id": destination_iata,
        "hl": "en",
        "gl": "us",
        "currency": "USD",
        "api_key": settings.SERPAPI_KEY,
        "outbound_date": depart_date,
    }
    # print(params)
    if return_date:
        params["return_date"] = return_date

    search = GoogleSearch(params)
    results = search.get_dict()
    
    # Extract flights list safely
    flights = results.get("best_flights", [])
    
    return flights


def fetch_flights(iata_code: str, date: str):
    # TODO: implement SerpAPI call
    return [{"from": iata_code, "to": "JFK", "date": date}]
