create table if not exists prod_airnow_stations(
    station_name varchar not null primary key,
    agency_name varchar,
    latitude    numeric(10,6) not null,
    longitude   numeric(10,6) not null,
    location_coord  point
);

create table if not exists stations_waqi(
    station_id      integer not null,
    station_name    varchar(500),
    latitude        numeric(10,6),
    longitude       numeric(10,6),
    aqi_id          varchar(10)
)