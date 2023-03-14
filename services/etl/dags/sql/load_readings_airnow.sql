insert into readings_airnow
(
	station_id,
	reading_datetime,
	pm25_conc,
	pm25_aqi,
	pm25_cat,
	pm10_conc,
	pm10_aqi,
	pm10_cat,
	no2_conc,
	no2_aqi,
	no2_cat,
	so2_conc,
	so2_aqi,
	so2_cat,
	co_conc,
	co_aqi,
	co_cat,
	o3_conc,
	o3_aqi,
	o3_cat
)
select
	full_aqs_id,
	timestamp_utc::timestamp,
	max(case when Pollutant = 'PM2.5' then concentration end)::numeric(7,3) as pm25_conc,
	max(case when Pollutant = 'PM2.5' then aqi end)::int as pm25_aqi,
	max(case when Pollutant = 'PM2.5' then category end)::int as pm25_cat,
	max(case when Pollutant = 'PM10' then concentration end)::numeric(7,3) as pm10_conc,
	max(case when Pollutant = 'PM10' then aqi end)::int as pm10_aqi,  
	max(case when Pollutant = 'PM10' then category end)::int as pm10_cat,
	max(case when Pollutant = 'NO2' then concentration end)::numeric(7,3) as no2_conc,
	max(case when Pollutant = 'NO2' then aqi end)::int as no2_aqi,
	max(case when Pollutant = 'NO2' then category end)::int as no2_cat,
	max(case when Pollutant = 'SO2' then concentration end)::numeric(7,3) as so2_conc,
	max(case when Pollutant = 'SO2' then aqi end)::int as so2_aqi,
	max(case when Pollutant = 'SO2' then category end)::int as so2_cat,
	max(case when Pollutant = 'CO' then concentration end)::numeric(7,3) as co_conc,
	max(case when Pollutant = 'CO' then aqi end)::int as co_aqi,
	max(case when Pollutant = 'CO' then category end)::int as co_cat,
	max(case when Pollutant = 'OZONE' then concentration end)::numeric(7,3) as o3_conc,
	max(case when Pollutant = 'OZONE' then aqi end)::int as o3_aqi,
	max(case when Pollutant = 'OZONE' then category end)::int as o3_cat
from readings_airnow_temp
group by
  full_aqs_id, timestamp_utc
on conflict (station_id, reading_datetime) do update
set
	pm25_conc = excluded.pm25_conc,
	pm25_aqi = excluded.pm25_aqi,
	pm25_cat = excluded.pm25_cat,
	pm10_conc = excluded.pm10_conc,
	pm10_aqi = excluded.pm10_aqi,
	pm10_cat = excluded.pm10_cat,
	no2_conc = excluded.no2_conc,
	no2_aqi = excluded.no2_aqi,
	no2_cat = excluded.no2_cat,
	so2_conc = excluded.so2_conc,
	so2_aqi = excluded.so2_aqi,
	so2_cat = excluded.so2_cat,
	co_conc = excluded.co_conc,
	co_aqi = excluded.co_aqi,
	co_cat = excluded.co_cat,
	o3_conc = excluded.o3_conc,
	o3_aqi = excluded.o3_aqi,
	o3_cat = excluded.o3_cat
;