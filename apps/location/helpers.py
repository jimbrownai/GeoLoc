import pandas as pd 
import os 
from django.conf import settings
from geopy.distance import geodesic

AIRPORTS_CSV = os.path.join(settings.BASE_DIR, "datasets", "airports.csv")
columns = [
    "airport_id",        # 1
    "name",              # 2
    "city",              # 3
    "country",           # 4
    "IATA",              # 5
    "ICAO",              # 6
    "latitude",          # 7
    "longitude",         # 8
    "altitude",          # 9
    "timezone",          # 10
    "DST",               # 11
    "tz_database_time_zone", # 12
    "type",              # 13
    "source"             # 14
]
airports_df = pd.read_csv(AIRPORTS_CSV,header=None,names=columns)

def find_nearby_airports(lat: float, lon: float, max_distance_km: float = 120):
    """
    Return airports within max_distance_km from given lat/lon
    """
    results = []

    for _, row in airports_df.iterrows():
        airport_coord = (row['latitude'], row['longitude'])
        distance = geodesic((lat, lon), airport_coord).km
        if distance <= max_distance_km :
            if row['IATA'] != "\\N":
                results.append({
                    "name": row["name"],
                    "city": row["city"],
                    "country": row["country"],
                    "iata": row["IATA"],
                    "type":row["type"],
                    "distance_km": round(distance, 2)
                })

    # Sort by distance
    results.sort(key=lambda x: x["distance_km"])
    return results