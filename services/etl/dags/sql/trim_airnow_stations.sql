-- removes all stations not represented in airnow_data readings
delete from temp_airnow_stations 
where station_name not in 
(select distinct temp_airnow_stations.station_name 
from temp_airnow_stations 
join prod_airnow_data
on temp_airnow_stations.station_name = prod_airnow_data.station_name);