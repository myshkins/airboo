import requests
import pprint as pp

base_url = "https://api.waqi.info/feed/geo:"
latitude = "40.04967209583848"
longitude = "-105.28730354750316"
token="bb10d851797e497b46823a5b4f984354c6ff4d9a"
# https://api.waqi.info/feed/geo:40.04967209583848;-105.28730354750316/?token=bb10d851797e497b46823a5b4f984354c6ff4d9a

def get_aq_data(lat: str = latitude, long: str = longitude) -> dict:
    get_url = base_url + latitude + ";" + longitude + "/?token=" + token
    response = requests.get(get_url)
    aq_json = response.json()
    return aq_json

