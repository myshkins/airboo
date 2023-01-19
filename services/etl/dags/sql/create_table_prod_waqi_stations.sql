create table if not exists stations_waqi(
    station_id      integer not null,
    station_name    varchar(500),
    latitude        numeric(10,6),
    longitude       numeric(10,6),
    aqi_id          varchar(10)
)