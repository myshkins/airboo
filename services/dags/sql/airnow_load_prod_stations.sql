INSERT INTO prod_airnow_stations (station_name, agency_name, latitude, longitude, location_coord)
    SELECT * FROM temp_airnow_stations
    ON CONFLICT DO NOTHING