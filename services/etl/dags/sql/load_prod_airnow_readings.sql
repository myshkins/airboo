INSERT INTO prod_airnow_data (
    station_name,
    reading_datetime,
    pm_10_conc,
    pm_10_AQI, 
    pm_10_AQI_CAT,
    pm_25_conc,
    pm_25_AQI,
    pm_25_AQI_CAT
    )
SELECT
    station_name,
    reading_datetime,
    pm_10_conc,
    pm_10_AQI, 
    pm_10_AQI_CAT,
    pm_25_conc,
    pm_25_AQI,
    pm_25_AQI_CAT
    FROM temp_airnow_data
ON CONFLICT ON CONSTRAINT prod_airnow_data_pk DO UPDATE SET
    station_name=EXCLUDED.station_name,
    reading_datetime=EXCLUDED.reading_datetime,
    pm_10_conc=EXCLUDED.pm_10_conc,
    pm_10_AQI=EXCLUDED.pm_10_AQI, 
    pm_10_AQI_CAT=EXCLUDED.pm_10_AQI_CAT,
    pm_25_conc=EXCLUDED.pm_25_conc,
    pm_25_AQI=EXCLUDED.pm_25_AQI,
    pm_25_AQI_CAT=EXCLUDED.pm_25_AQI_CAT