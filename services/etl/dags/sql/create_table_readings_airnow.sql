create table if not exists readings_airnow (
    station_name        varchar not null,
    request_datetime    timestamp not null,
    reading_datetime    timestamp not null,
    pm_10_conc          numeric(7,3),
    pm_10_aqi           numeric(7,3),
    pm_10_aqi_cat       numeric(2,1),
    pm_25_conc          numeric(7,3),
    pm_25_aqI           numeric(7,3),
    pm_25_aqi_cat       numeric(2,1),
    primary key (station_name, reading_datetime)
);
