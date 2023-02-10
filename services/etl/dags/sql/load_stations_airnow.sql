insert into stations_airnow (
    full_aqs_id,
    station_id,
    station_name,
    agency_name,
	status,
    latitude,
    longitude,
	elevation,
	country,
    location_coord
    )
select
    full_aqs_id,
	station_id, 
	site_name,
	agency_name,
	status,
	latitude,
	longitude,
	elevation,
	country_fips as country,
	ST_GeomFromText('point(' || longitude || ' ' || latitude || ')',4326) as location_coord
from stations_airnow_temp
group by full_aqs_id, station_id, site_name, agency_name, status, latitude, longitude, elevation, country_fips, location_coord
on conflict (full_aqs_id) do update set
    station_id = excluded.station_id,
    station_name = excluded.station_name,
    agency_name = excluded.agency_name,
	status = excluded.status,
    latitude = excluded.latitude,
    longitude = excluded.longitude,
    elevation = excluded.elevation,
	country = excluded.country,
    location_coord=excluded.location_coord