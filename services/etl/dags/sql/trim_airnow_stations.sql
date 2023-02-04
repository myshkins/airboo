-- removes all stations not represented in airnow_readings
delete from stations_airnow_temp 
where station_id not in 
(select distinct stations_airnow_temp.station_id 
from stations_airnow_temp 
join readings_airnow
on stations_airnow_temp.station_id = readings_airnow.station_id);