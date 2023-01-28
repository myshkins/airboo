insert into readings_airnow (
    station_name,
    request_datetime,
    reading_datetime,
    pm_10_conc,
    pm_10_AQI, 
    pm_10_AQI_CAT,
    pm_25_conc,
    pm_25_AQI,
    pm_25_AQI_CAT
    )
select
    station_name,
    request_datetime,
    reading_datetime,
    pm_10_conc,
    pm_10_AQI, 
    pm_10_AQI_CAT,
    pm_25_conc,
    pm_25_AQI,
    pm_25_AQI_CAT
    from readings_airnow_temp
on conflict (station_name, reading_datetime) do update set 
    station_name=excluded.station_name,
    request_datetime=excluded.request_datetime,
    reading_datetime=excluded.reading_datetime,
    pm_10_conc=excluded.pm_10_conc,
    pm_10_AQI=excluded.pm_10_AQI, 
    pm_10_AQI_CAT=excluded.pm_10_AQI_CAT,
    pm_25_conc=excluded.pm_25_conc,
    pm_25_AQI=excluded.pm_25_AQI,
    pm_25_AQI_CAT=excluded.pm_25_AQI_CAT;