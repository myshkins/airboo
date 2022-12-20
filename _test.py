import os
import requests
from datetime import datetime as dt
from datetime import timedelta


params = {
    "startDate": dt.utcnow().strftime('%Y-%m-%dT%H'),
    "endDate": (dt.utcnow() + timedelta(hours=1)).strftime('%Y-%m-%dT%H'),
    "parameters": "OZONE,PM25,PM10,CO,NO2,SO2",
    "BBOX": "-124.205070,28.716781, -75.337882,45.419415",
    "dataType": "B",
    "format": "text/csv",
    "verbose": "1",
    "monitorType": "2",
    "includerawconcentrations": "1",
    "API_KEY": "AA5AB45D-9E64-41DE-A918-14578B9AC816",
    }
AIRNOW_BY_STATION_API_URL = "https://www.airnowapi.org/aq/data/"


data_path = "dags/files/aqi_data.csv"
os.makedirs(os.path.dirname(data_path), exist_ok=True)

response = requests.get(
    AIRNOW_BY_STATION_API_URL, params=params, timeout=20
    )
csv_data = response.text
with open(data_path, 'w') as file:
    file.write(csv_data)