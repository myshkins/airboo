COPY stations_airnow_temp(
    station_id,
    station_name,
    agency_name,
    latitude,
    longitude
) FROM stdin WITH DELIMITER AS '|' 
NULL AS ''