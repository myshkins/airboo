import pendulum
import requests
from config import Settings

AIRNOW_URL = "https://www.airnowapi.org/aq/data/"
STATION_URL = "https://s3-us-west-1.amazonaws.com//files.airnowtech.org/airnow/"

settings = Settings()
yesterday = (pendulum.now() - pendulum.duration(days=1)).format('YMMDD')
now = pendulum.now(tz='UTC')
year = now.year
params = {
    "startDate": now.format('Y-MM-DDTH'),
    "endDate": (now + pendulum.duration(hours=1)).format('Y-MM-DDTH'),
    "parameters": "OZONE,PM25,PM10,CO,NO2,SO2",
    "BBOX": "-167.716404,3.233406,-63.653904,70.867976",
    "dataType": "B",
    "format": "text/csv",
    "verbose": "1",
    "monitorType": "2",
    "includerawconcentrations": "0",
    "API_KEY": settings.AIRNOW_API_KEY,
    }


def get_airnow_data():
    try:
        response = requests.get(AIRNOW_URL, params=params, timeout=20)
        return response.text
    except requests.exceptions.RequestException as e:
        raise e

def get_airnow_stations():
    station_url = f"{STATION_URL}{year}/{yesterday}/Monitoring_Site_Locations_V2.dat"
    response = requests.get(station_url)
    return response.text