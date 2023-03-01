from pydantic import BaseModel, confloat


class Location(BaseModel):
    lat: confloat(ge=-90, le=90)
    long: confloat(ge=-180, le=180)
