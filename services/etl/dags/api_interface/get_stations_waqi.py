from datetime import datetime as dt

import requests
from config import Settings

# URL for all US stations:
# https://api.waqi.info/v2/map/bounds?latlng=32.000000,-125.000000,47.500000,-69.000000&networks=all&token=bb10d851797e497b46823a5b4f984354c6ff4d9a

# URL for all global stations:
# https://api.waqi.info/v2/map/bounds?latlng=-90.000000,-180.000000,90.000000,180.000000&networks=all&token=bb10d851797e497b46823a5b4f984354c6ff4d9a

settings = Settings()


def get_stations_waqi():
    us_lat_long = "32.000000,-125.000000,47.500000,-69.000000"
    station_url = settings.WAQI_BASE_URL + "map/bounds/"
    station_params = {
        "latlng": us_lat_long,  # "32.000000,-125.000000,47.500000,-69.000000",
        "networks": "all",
        "token": settings.WAQI_TOKEN
    }
    try:
        response = requests.get(station_url, params=station_params)
        stations = response.json().get("data")
        station_result = []
        now = str(dt.now())
        for station in stations:
            station_result.append(
                {
                    "station_name": station.get("station").get("name"),
                    "latitude": station.get("lat"),
                    "longitude": station.get("lon"),
                    "station_id": station.get("uid"),
                    "aqi_id": station.get("aqi"),
                    "request_datetime": now,
                }
            )
        return station_result
    except requests.exceptions.RequestException as e:
        raise e