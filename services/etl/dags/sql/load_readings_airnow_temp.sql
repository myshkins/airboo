copy readings_airnow_temp(
    latitude,
    longitude,
    timestamp_utc,
    pollutant,
    concentration,
    unit,
    aqi,
    category,
    site_name,
    site_agency,
    aqs_id,
    full_aqs_id
)
from stdin with csv delimiter as ',' quote as '"' null as ''

