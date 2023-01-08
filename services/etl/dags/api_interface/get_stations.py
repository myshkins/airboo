import json
from datetime import datetime as dt

import requests

# from config import get_env_configs

# URL for all US stations:
# https://api.waqi.info/v2/map/bounds?latlng=32.000000,-125.000000,47.500000,-69.000000&networks=all&token=bb10d851797e497b46823a5b4f984354c6ff4d9a

# URL for all global stations:
# https://api.waqi.info/v2/map/bounds?latlng=-90.000000,-180.000000,90.000000,180.000000&networks=all&token=bb10d851797e497b46823a5b4f984354c6ff4d9a

us_lat_long = "latlng=32.000000,-125.000000,47.500000,-69.000000"

def get_waqi_stations():
    """get list of all stationsa and return as json"""

    station_url = "https://api.waqi.info/v2/map/bounds?latlng=32.000000,-125.000000,47.500000,-69.000000&networks=all&token=bb10d851797e497b46823a5b4f984354c6ff4d9a"
    # station_url = get_env_configs().WAQI_BASE_URL + "map/bounds?" + us_lat_long + get_env_configs().WAQI_TOKEN
    response = requests.get(station_url)
    stations = response.json().get('data')
    station_result = []
    now = str(dt.now())
    for station in stations:
        print(f"STATION = {station}")
        station_result.append({
                "station_name": station.get("station").get("name"),
                "latitude": station.get("lat"),
                "longitude": station.get("lon"),
                "station_id": station.get("uid"),
                "aqi_id": station.get("aqi"),
                "request_datetime": now
            })
    return station_result

get_waqi_stations()