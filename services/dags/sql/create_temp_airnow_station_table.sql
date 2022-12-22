DROP TABLE IF EXISTS airnow_stations_temp;
CREATE TABLE airnow_stations_temp(
            station_name varchar not null primary key,
            agency_name varchar,
            latitude    numeric(10,6) not null,
            longitude   numeric(10,6) not null
);