CREATE TABLE IF NOT EXISTS airnow_readings(
            reading_id serial primary key,
            station_name varchar not null,
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

DROP TABLE IF EXISTS airnow_readings_temp;
CREATE TABLE airnow_readings_temp(
            -- reading_id serial primary key,
            station_name varchar not null,
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

-- DROP TABLE IF EXISTS airnow_readings_temp;
-- CREATE TABLE airnow_readings_temp(
--             reading_id serial primary key,
--             latitude        numeric(10,6),
--             longitude       numeric(10,6),
--             reading_datetime timestamp,
--             parameter       varchar,
--             concentration   numeric(5,3),
--             unit            varchar,
--             AQI             integer,
--             AQI_cat         integer,
--             station_name    varchar,
--             station_id      bigint,
--             station_idx     bigint
-- );
