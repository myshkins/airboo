drop table if exists air_quality.public.stations_waqi_temp;
create table stations_waqi_temp(
    station_id          integer primary key,
    station_name        varchar(500),
    latitude            numeric(10,6),
    longitude           numeric(10,6),
    aqi_id              varchar(10),
    request_datetime    timestamp
)