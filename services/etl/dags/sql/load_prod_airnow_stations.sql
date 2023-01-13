INSERT INTO prod_airnow_stations (
    station_name,
    agency_name,
    latitude,
    longitude,
    location_coord
    )
SELECT
    station_name,
    agency_name,
    latitude,
    longitude,
    location_coord
    FROM temp_airnow_stations
ON CONFLICT (station_name) DO UPDATE SET 
    station_name=EXCLUDED.station_name,
    agency_name=EXCLUDED.agency_name,
    latitude=EXCLUDED.latitude,
    longitude=EXCLUDED.longitude,
    location_coord=EXCLUDED.location_coord