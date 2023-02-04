drop table if exists stations_airnow_temp;
create table stations_airnow_temp(
    station_id  integer primary key,
    station_name varchar not null,
    agency_name varchar,
    latitude    numeric(10,6) not null,
    longitude   numeric(10,6) not null,
    location_coord geometry(point, 4326)
);