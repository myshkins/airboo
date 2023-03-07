from pydantic import BaseModel, confloat
from enum import Enum


class Location(BaseModel):
    lat: confloat(ge=-90, le=90)
    long: confloat(ge=-180, le=180)


class PeriodEnum(str, Enum):
    twelve_hr = "twelve_hr"
    twenty_four_hr = "twenty_four_hr"
    forty_eight_hr = "forty_eight_hr"
    five_day = "five_day"
    ten_day = "ten_day"
    one_month = "one_month"
    one_year = "one_year"
    all_time = "all_time"

    def pd_repr(self):
        # use that chart.js plugin if all_time selected?
        hr = ["twelve_hr", "twenty_four_hr", "forty_eight_hr", "all_time"]
        if self.value in hr:
            return 'H'
        elif self.value == "ten_day":
            return '10H'
        elif self.value == "one_month":
            return 'M'
        elif self.value == "one_year":
            return 'A'


class TimePeriod(BaseModel):
    time: PeriodEnum
