INSERT INTO prod_airnow_data (
    station_name, reading_datetime, pm_10_conc, pm_10_AQI, 
    pm_10_AQI_CAT, pm_25_conc, pm_25_AQI, pm_25_AQI_CAT
    )
SELECT * FROM temp_airnow_data
ON CONFLICT DO NOTHING