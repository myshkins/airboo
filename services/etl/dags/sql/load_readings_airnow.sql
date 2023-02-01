insert into readings_airnow (
    station_name,
    request_datetime,
    reading_datetime,
    pm_10_conc,
    pm_10_aqi, 
    pm_10_aqi_cat,
    pm_25_conc,
    pm_25_aqi,
    pm_25_aqi_cat
    )
select
    station_name,
    request_datetime,
    reading_datetime,
    pm_10_conc,
    pm_10_aqi, 
    pm_10_aqi_cat,
    pm_25_conc,
    pm_25_aqi,
    pm_25_aqi_cat
    from readings_airnow_temp
on conflict (station_name, reading_datetime) do update set 
    station_name=excluded.station_name,
    request_datetime=excluded.request_datetime,
    reading_datetime=excluded.reading_datetime,
    pm_10_conc=excluded.pm_10_conc,
    pm_10_aqi=excluded.pm_10_aqi, 
    pm_10_aqi_cat=excluded.pm_10_aqi_cat,
    pm_25_conc=excluded.pm_25_conc,
    pm_25_aqi=excluded.pm_25_aqi,
    pm_25_aqi_cat=excluded.pm_25_aqi_cat;