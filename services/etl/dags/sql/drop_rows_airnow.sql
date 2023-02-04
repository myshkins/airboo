-- removes all canadian station readings, which were included in the api call
-- bounding box parameter
delete from readings_airnow_temp 
where station_id not in 
(select distinct station_id from stations_airnow_temp);