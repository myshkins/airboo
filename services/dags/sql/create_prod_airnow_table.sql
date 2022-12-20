CREATE TABLE IF NOT EXISTS airnow_readings(
            reading_id serial,
            station_name varchar primary key not null,
            latitude    numeric(10,6) not null,
            longitude   numeric(10,6) not null,
            reading_datetime timestamp not null,
            pm_10_conc       numeric(7,3),
            pm_10_AQI       numeric(7,3),
            pm_10_AQI_CAT   numeric(2,1),
            pm_25_conc       numeric(7,3),
            pm_25_AQI       numeric(7,3),
            pm_25_AQI_CAT   numeric(2,1)
);