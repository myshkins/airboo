insert into stations_airnow (
    station_id,
    station_name,
    agency_name,
    latitude,
    longitude,
    location_coord
    )
select
    station_id,
    station_name,
    agency_name,
    latitude,
    longitude,
    location_coord
    from stations_airnow_temp
on conflict (station_id) do update set
    station_id=excluded.station_id,
    station_name=excluded.station_name,
    agency_name=excluded.agency_name,
    latitude=excluded.latitude,
    longitude=excluded.longitude,
    location_coord=excluded.location_coord