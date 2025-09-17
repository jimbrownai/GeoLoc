from dataclasses import dataclass
from typing import List,Optional

@dataclass
class PredictionResult:
    place_name: str
    confidence: float 
    model: str

@dataclass
class LocationInfo:
    place_name: str 
    formatted_address: str 
    lat: float
    lon: float

@dataclass
class AirportInfo:
    name: str 
    city: str 
    country: str
    iata: str
    type: str 
    distance_km: float 

@dataclass
class AirportResult:
    airports: List[AirportInfo]

@dataclass
class AirportDetail:
    name: str
    id: str
    time: str


@dataclass
class FlightLeg:
    departure_airport: AirportDetail
    arrival_airport: AirportDetail
    duration: int
    airplane: str
    airline: str
    airline_logo: str
    travel_class: str
    flight_number: str
    legroom: Optional[str] = None
    extensions: Optional[List[str]] = None
    overnight: Optional[bool] = False


@dataclass
class Layover:
    duration: int
    name: str
    id: str


@dataclass
class CarbonEmissions:
    this_flight: int
    typical_for_this_route: int
    difference_percent: int


@dataclass
class FlightOption:
    flights: List[FlightLeg]
    layovers: Optional[List[Layover]]
    total_duration: int
    carbon_emissions: CarbonEmissions
    price: float
    type: str
    airline_logo: Optional[str] = None
    departure_token: Optional[str] = None


@dataclass
class FlightsResult:
    options: List[FlightOption]

@dataclass
class GuideResponse:
    place: str
    info: str 