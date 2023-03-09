from pydantic import BaseModel, confloat
from enum import Enum
from datetime import timedelta, datetime as dt


class Location(BaseModel):
    lat: confloat(ge=-90, le=90)
    long: confloat(ge=-180, le=180)


class TimeEnum(str, Enum):
    twelve_hr = "twelve_hr"
    twenty_four_hr = "twenty_four_hr"
    forty_eight_hr = "forty_eight_hr"
    five_day = "five_day"
    ten_day = "ten_day"
    one_month = "one_month"
    one_year = "one_year"
    all_time = "all_time"

    def letter(self):
        # use that chart.js (https://www.npmjs.com/package/chartjs-plugin-downsample) plugin if all_time selected?
        code_dict = {
            "twelve_hr": "H",
            "twenty_four_hr": "H",
            "forty_eight_hr": "H",
            "all_time": "H",
            "ten_day": "10H",
            "one_month": "M",
            "one_year": "A",
        }
        return code_dict[self.value]

    def start(self):
        start_dict = {
            "twelve_hr": dt.now() - timedelta(hours=12),
            "twenty_four_hr": dt.now() - timedelta(hours=24),
            "forty_eight_hr": dt.now() - timedelta(hours=48),
            "all_time": dt(2023, 1, 1),
            "ten_day": dt.now() - timedelta(days=10),
            "one_month": dt.now() - timedelta(days=30),
            "one_year": dt.now() - timedelta(days=365),
        }
        return start_dict[self.value]


class PollutantEnum(str, Enum):
    pm25 = "pm25"
    pm10 = "pm10"
    o3 = "o3"
    co = "co"
    no2 = "no2"
    so2 = "so2"
