drop table if exists temp_airnow_data;
create table temp_airnow_data(
    station_name        varchar not null,
    request_datetime    timestamp not null,
    reading_datetime    timestamp not null,
    pm_10_conc          numeric(7,3),
    pm_10_AQI           numeric(7,3),
    pm_10_AQI_CAT       numeric(2,1),
    pm_25_conc          numeric(7,3),
    pm_25_AQI           numeric(7,3),
    pm_25_AQI_CAT       numeric(2,1)
);