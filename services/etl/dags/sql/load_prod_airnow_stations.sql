insert into prod_airnow_stations (
    station_name,
    agency_name,
    latitude,
    longitude,
    location_coord
    )
select
    station_name,
    agency_name,
    latitude,
    longitude,
    location_coord
    from temp_airnow_stations
on conflict (station_name) do update set
    station_name=excluded.station_name,
    agency_name=excluded.agency_name,
    latitude=excluded.latitude,
    longitude=excluded.longitude,
    location_coord=excluded.location_coord