CREATE TABLE IF NOT EXISTS prod_airnow_stations(
            station_name varchar not null primary key,
            agency_name varchar,
            latitude    numeric(10,6) not null,
            longitude   numeric(10,6) not null,
            location_coord  point
);