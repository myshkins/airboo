import asyncio
import pprint
from datetime import datetime as dt
from typing import List

from aiohttp import ClientSession, InvalidURL  # ClientError
# from aiohttp.web import HTTPException
from config import Settings
from db.db_engine import get_db
from db.models.waqi_stations import WAQI_Stations
from sqlalchemy import select


def get_station_list():
    """query database for list of all WAQI station and returns list of all station ids"""
    sql_stmt = select(WAQI_Stations.station_name)
    with get_db() as db:
        stations_result = db.execute(sql_stmt).all()
    station_list = [station.station_name for station in stations_result]
    return station_list


def init_urls():
    """loops through all waqi stations and asynchronously requests data for each."""
    station_list = get_station_list()
    url_list = [Settings().WAQI_BASE_URL
                + "feed/" + station
                + "/?token=" + Settings().WAQI_TOKEN
                for station in station_list]
    return url_list


async def create_task_list(session: ClientSession):
    task_list = []
    url_list = init_urls()
    for url in url_list:
        new_task = asyncio.create_task(
            fetch_readings_urls(session, url)
        )
        task_list.append(new_task)
    return task_list


async def format_waqi_response(response: dict) -> dict:
    aq_json = response['data']
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


async def fetch_readings_urls(session: ClientSession, url: str) -> dict:
    try:
        async with session.get(url) as response:
            response_json = await response.json()
            print(f"response_json = {response_json}")
            result_json = await format_waqi_response(response_json)
        # if response.status >= 400:
        #     raise HTTPException as e:
    except InvalidURL as e:
        print('Invalid sation URL for waqi readings', str(e))

    return result_json


async def get_waqi_readings():
    async with ClientSession() as session:
        task_list = await create_task_list(session)
        readings_list = await asyncio.gather(*task_list)
    return readings_list
# get_readings_waqi("Intermediate School 143, New York, USA")
# get_readings_waqi("Boulder")


readings = asyncio.run(get_waqi_readings())
pprint.pprint(readings)
