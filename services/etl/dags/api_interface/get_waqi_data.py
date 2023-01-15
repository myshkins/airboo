import requests
from config import Settings

latitude = "40.04967209583848"
longitude = "-105.28730354750316"

def get_waqi_data(lat: str = latitude, long: str = longitude) -> dict:
    """
    TO-DO: add exception handling...better way to format dictionary?
    """
    get_url = Settings().WAQI_BASE_URL + "feed/geo:" + latitude + ";" + longitude + "/?token=" + Settings().WAQI_TOKEN
    response = requests.get(get_url)
    aq_json = response.json()['data']
    result_json = {'station_name': aq_json.get('city').get('name'),
                    'longitude': aq_json.get('city').get('geo')[0],
                    'latitude': aq_json.get('city').get('geo')[1],
                    'reading_datetime': aq_json.get('time').get('iso'),
                    'request_datetime': aq_json.get('debug').get('sync'),
                    'co': aq_json.get('iaqi').get('co').get('v'),
                    'h': aq_json['iaqi']['h']['v'],
                    'no2': aq_json['iaqi']['no2']['v'],
                    'o3': aq_json['iaqi']['o3']['v'],
                    'p': aq_json['iaqi']['p']['v'],
                    'pm_10': aq_json['iaqi']['pm10']['v'],
                    'pm_25': aq_json['iaqi']['pm25']['v'],
                    'so2': aq_json['iaqi']['so2']['v'],
                    't': aq_json['iaqi']['t']['v'],
                    'w': aq_json['iaqi']['w']['v'],
                    'wg': aq_json['iaqi']['wg']['v']
    }
    return result_json 