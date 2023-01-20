import pendulum
import requests
from config import Settings

AIRNOW_URL = "https://www.airnowapi.org/aq/data/"
STATION_URL = "https://s3-us-west-1.amazonaws.com//files.airnowtech.org/airnow/"

settings = Settings()
yesterday = (pendulum.now() - pendulum.duration(days=1)).format('YMMDD')
year = pendulum.now().year
params = {
    "startDate": dt.utcnow().strftime('%Y-%m-%dT%H'),
    "endDate": (dt.utcnow() + timedelta(hours=1)).strftime('%Y-%m-%dT%H'),
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
    response = requests.get(AIRNOW_URL, params=params, timeout=20)
    return response.text

def get_airnow_stations():
    station_url = f"{STATION_URL}{year}/{yesterday}/Monitoring_Site_Locations_V2.dat"
    response = requests.get(station_url)
    return response.text