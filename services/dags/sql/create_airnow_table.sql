CREATE TABLE IF NOT EXISTS ReadingsAirnow(
            reading_id serial primary key,
            station_name varchar not null,
            latitude    numeric(10,6) not null,
            longitude   numeric(10,6) not null,
            reading_datetime timestamp not null,
            pm_10_conc       numeric(5,3),
            pm_10_AQI       numeric(5,3),
            pm_10_AQI_CAT   integer,
            pm_25_conc       numeric(5,3),
            pm_25_AQI       numeric(5,3),
);

DROP TABLE IF EXISTS ;
CREATE TABLE ReadingsTempAirnow(
            reading_id serial primary key,
            station_name varchar not null,
            latitude    numeric(10,6) not null,
            longitude   numeric(10,6) not null,
            reading_datetime timestamp not null,
            pm_10_conc       numeric(5,3),
            pm_10_AQI       numeric(5,3),
            pm_10_AQI_CAT   integer,
            pm_25_conc       numeric(5,3),
            pm_25_AQI       numeric(5,3),
);
