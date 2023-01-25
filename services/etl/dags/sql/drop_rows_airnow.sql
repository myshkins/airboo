-- removes all canadian station readings, which were included in the api call
-- bounding box parameter
delete from temp_airnow_data 
where station_name not in 
(select distinct station_name from temp_airnow_stations);