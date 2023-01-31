-- removes all stations not represented in airnow_readings
delete from stations_airnow_temp 
where station_name not in 
(select distinct stations_airnow_temp.station_name 
from stations_airnow_temp 
join readings_airnow
on stations_airnow_temp.station_name = readings_airnow.station_name);