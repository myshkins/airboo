import pprint
from datetime import datetime as dt

import requests
from config import Settings
from db.db_engine import get_db
from db.models.waqi_stations import WAQI_Stations
from sqlalchemy import select

# latitude = "40.04967209583848"
# longitude = "-105.28730354750316"



def get_station_list():
    """query database for list of all WAQI station and returns list of all station ids"""
    sql_stmt = select(WAQI_Stations.station_name)
    with get_db() as db:
        stations_result = db.execute(sql_stmt).all()
    station_list = [station.station_name for station in stations_result]
    return station_list


def collect_waqi_readings():
    """loops through all waqi stations and asynchronously requests data for each."""
    station_list = get_station_list()
    for station in station_list:
        get_readings_waqi(station)


def get_readings_waqi(station: str) -> dict:
    get_url = Settings().WAQI_BASE_URL + "feed/" + station + "/?token=" + Settings().WAQI_TOKEN
    try:
        response = requests.get(get_url)
        aq_json = response.json()['data']
        time_now = str(dt.now())
        result_json = {
            'station_name': aq_json.get('city', {}).get('name', None),
            'longitude': aq_json.get('city', {}).get('geo', [])[0],
            'latitude': aq_json.get('city', {}).get('geo', [])[1],
            'reading_datetime': aq_json.get('time', {}).get('iso', None),
            'request_datetime': time_now,
            'co': aq_json.get('iaqi', {}).get('co', {}).get('v', None),
            'h': aq_json.get('iaqi', {}).get('h', {}).get('v', None),
            'no2': aq_json.get('iaqi', {}).get('no2', {}).get('v', None),
            'o3': aq_json.get('iaqi', {}).get('o3', {}).get('v', None),
            'p': aq_json.get('iaqi', {}).get('p', {}).get('v', None),
            'pm_10': aq_json.get('iaqi', {}).get('pm10', {}).get('v', None),
            'pm_25': aq_json.get('iaqi', {}).get('pm25').get('v', None),
            'so2': aq_json.get('iaqi', {}).get('so2', {}).get('v', None),
            't': aq_json.get('iaqi', {}).get('t', {}).get('v', None),
            'w': aq_json.get('iaqi', {}).get('w', {}).get('v', None),
            'wg': aq_json.get('iaqi', {}).get('wg', {}).get('v', None)
        }
        return result_json
    except requests.exceptions.RequestException as e:
        raise e


get_readings_waqi("Intermediate School 143, New York, USA")
get_readings_waqi("Boulder")



