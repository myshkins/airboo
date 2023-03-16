from datetime import datetime as dt
from datetime import timedelta
from enum import Enum
import os

from pydantic import BaseModel, confloat
from shared_models.readings_airnow import ReadingsAirnow

TESTING_START_DATE = dt(2023, 3, 13, 14)
# test


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
        # use that chart.js (https://www.npmjs.com/package/chartjs-plugin-downsample)
        # plugin if all_time selected?
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
        time_zero = dt.now()
        if os.environ["DEV_MODE"] == "true":
            time_zero = TESTING_START_DATE
        start_dict = {
            "twelve_hr": time_zero - timedelta(hours=13),
            "twenty_four_hr": time_zero - timedelta(hours=25),
            "forty_eight_hr": time_zero - timedelta(hours=49),
            "all_time": dt(2023, 1, 1),
            "ten_day": time_zero - timedelta(days=10),
            "one_month": time_zero - timedelta(days=30),
            "one_year": time_zero - timedelta(days=365),
        }
        return start_dict[self.value]


class PollutantEnum(str, Enum):
    pm25 = "pm25"
    pm10 = "pm10"
    o3 = "o3"
    co = "co"
    no2 = "no2"
    so2 = "so2"

    def column(self):
        col_dict = {
            "pm25": ReadingsAirnow.pm25_aqi,
            "pm10": ReadingsAirnow.pm10_aqi,
            "o3": ReadingsAirnow.o3_aqi,
            "co": ReadingsAirnow.co_conc,
            "no2": ReadingsAirnow.no2_aqi,
            "so2": ReadingsAirnow.so2_aqi,
        }
        return col_dict[self.value]
