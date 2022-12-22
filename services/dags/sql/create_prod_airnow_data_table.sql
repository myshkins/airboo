CREATE TABLE IF NOT EXISTS airnow_readings(
            station_name varchar not null,
            reading_datetime timestamp not null,
            pm_10_conc       numeric(7,3),
            pm_10_AQI       numeric(7,3),
            pm_10_AQI_CAT   numeric(2,1),
            pm_25_conc       numeric(7,3),
            pm_25_AQI       numeric(7,3),
            pm_25_AQI_CAT   numeric(2,1),
            primary key (station_name, reading_datetime)
);