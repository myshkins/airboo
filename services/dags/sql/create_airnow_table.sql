CREATE TABLE IF NOT EXISTS ReadingsAirnow(
            reading_id serial primary key,
            station_name varchar not null,
            reading_datetime timestamp not null,
            latitude    numeric(10,6)
            longitude   numeric(10,6)
            pm_10_conc       numeric(5,3)
            pm_25_conc       numeric(5,3)
);

DROP TABLE IF EXISTS ;
CREATE TABLE ReadingsTempAirnow(
            reading_id serial primary key,
            station_name varchar not null,
            reading_datetime timestamp not null,
            latitude    numeric(10,6)
            longitude   numeric(10,6)
            pm_10_conc       numeric(5,3)
            pm_25_conc       numeric(5,3)
);