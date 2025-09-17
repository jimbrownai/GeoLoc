from ..services import predict_image
from ...location.helpers import find_nearby_airports
from ...flights.services import get_flights
from ...location.services import get_place_location
from ...genai.services.travel_guide import generate_travel_guide
from .models import PredictionResult,LocationInfo,AirportInfo,AirportResult,FlightLeg,AirportDetail,CarbonEmissions,Layover,FlightOption,FlightsResult,GuideResponse
from dataclasses import asdict

def famous_places_pipeline(model,img_file, user_origin_iata, depart_data,return_date):
    place_name,confidence = predict_image(model,img_file)
    prediction = PredictionResult(place_name,confidence,model="resnet_50_famous_places")
    print(prediction.place_name, prediction.confidence)
    # {
    # "result": {
    #     "place_name": "Big_Ben",
    #     "confidence": 0.9998717308044434
    # },
    # "model": "resnet_50_famous_places"
    # }

    # place_name, formatted_address,lat,lng  = get_place_location(place_name)
    place_name, formatted_address,lat,lng  = get_place_location(prediction.place_name)
    location = LocationInfo(place_name,formatted_address,lat,lon=lng)

    print(location.place_name, location.formatted_address,location.lat,location.lon)
    # {
    # "place_name": "Big_Ben",
    # "formatted_address": "London SW1A 0AA, UK",
    # "lat": 51.50072919999999,
    # "lon": -0.1246254
    # }

    guide = generate_travel_guide(prediction.place_name)
    guideResult = GuideResponse(prediction.place_name,guide['guide'])
    airports_info = find_nearby_airports(lat,lng,20.0)

    airports_objs = [
        AirportInfo(**a) for a in airports_info
    ]

    
    airport_result = AirportResult(airports=airports_objs)
    # {
    # "airports": [
    #     {
    #         "name": "London City Airport",
    #         "city": "London",
    #         "country": "United Kingdom",
    #         "iata": "LCY",
    #         "type": "airport",
    #         "distance_km": 12.5
    #     }
    # ]
    # }
    # flights_info = get_flights(user_origin_iata,airports_info['airports'][0]['iata'],'09/09/25','15/09/25')

    # flights = get_flights(user_origin_iata, airports_objs[0].iata, '15/09/25',  '25/09/25')
    flights = get_flights(user_origin_iata, airports_objs[0].iata, depart_data,  return_date)
    flight_options = []
    for f in flights:  # SERP returns list of flight options
        legs = [
            FlightLeg(
                departure_airport=AirportDetail(**leg["departure_airport"]),
                arrival_airport=AirportDetail(**leg["arrival_airport"]),
                duration=leg["duration"],
                airplane=leg["airplane"],
                airline=leg["airline"],
                airline_logo=leg["airline_logo"],
                travel_class=leg["travel_class"],
                flight_number=leg["flight_number"],
                legroom=leg.get("legroom"),
                extensions=leg.get("extensions", []),
                overnight=leg.get("overnight", False),
            )
            for leg in f.get("flights", [])
        ]

        layovers = [
            Layover(**layover) for layover in f.get("layovers", [])
        ] if "layovers" in f else None

        emissions = CarbonEmissions(**f["carbon_emissions"])

        option = FlightOption(
            flights=legs,
            layovers=layovers,
            total_duration=f["total_duration"],
            carbon_emissions=emissions,
            price=f["price"],
            type=f["type"],
            airline_logo=f.get("airline_logo"),
            departure_token=f.get("departure_token"),
        )
        flight_options.append(option)

    flights_result = FlightsResult(options=flight_options)

    return{
        "prediction":asdict(prediction),
        "information":guideResult.info,
        "nearest_airports":asdict(airport_result),
        "flights":asdict(flights_result)
    }
    # return location,airport_result