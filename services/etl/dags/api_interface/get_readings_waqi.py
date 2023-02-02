import asyncio
from datetime import datetime as dt

from aiohttp import ClientError, ClientSession, InvalidURL
from aiohttp.web import HTTPException
from config import Settings
from db.db_engine import get_db
from db.models.waqi_stations import Waqi_Stations
from sqlalchemy import select


def get_station_list():
    """query database for list of all WAQI station and returns list of all station ids"""
    sql_stmt = select(Waqi_Stations.station_id)
    with get_db() as db:
        stations_result = db.execute(sql_stmt).all()
    station_list = [station.station_id for station in stations_result]
    return station_list


def init_urls():
    """loops through all waqi stations and asynchronously requests data for each."""
    station_list = get_station_list()
    url_list = [Settings().WAQI_BASE_URL
                + "feed/@" + str(station)
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
        'station_id': aq_json.get('idx', None),
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
        'pm_25': aq_json.get('iaqi', {}).get('pm25', {}).get('v', None),
        'so2': aq_json.get('iaqi', {}).get('so2', {}).get('v', None),
        't': aq_json.get('iaqi', {}).get('t', {}).get('v', None),
        'w': aq_json.get('iaqi', {}).get('w', {}).get('v', None),
        'wg': aq_json.get('iaqi', {}).get('wg', {}).get('v', None)
    }
    return result_json


async def fetch_readings_urls(session: ClientSession, url: str) -> dict:
    try:
        async with session.get(url) as response:
            if response.status >= 400:
                raise HTTPException(message='HTTP 400+ error calling waqi readings')
            response_json = await response.json()
            if response_json.get('status') == 'ok':
                result_json = await format_waqi_response(response_json)
            else:
                result_json = None
    except InvalidURL as e:
        print('Invalid sation URL for waqi readings', str(e))
    except ClientError as e:
        print('Client error getting waqi readings', str(e))
    except HTTPException as e:
        print('HTTP Exception', str(e))

    return result_json


async def get_waqi_readings():
    async with ClientSession() as session:
        task_list = await create_task_list(session)
        readings_list = await asyncio.gather(*task_list)
        result_list = [reading for reading in readings_list if reading]  # remove None values
    return result_list


# readings = asyncio.run(get_waqi_readings())
# pprint.pprint(readings)
