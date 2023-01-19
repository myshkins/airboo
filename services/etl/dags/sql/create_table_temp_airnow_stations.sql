drop table if exists temp_airnow_stations;
create table temp_airnow_stations(
            station_name varchar not null primary key,
            agency_name varchar,
            latitude    numeric(10,6) not null,
            longitude   numeric(10,6) not null,
            location_coord  point
);