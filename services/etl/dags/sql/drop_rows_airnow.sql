-- removes all canadian station readings, which were included in the api call
-- bounding box parameter
delete from readings_airnow_temp 
where station_name not in 
(select distinct station_name from stations_airnow_temp);