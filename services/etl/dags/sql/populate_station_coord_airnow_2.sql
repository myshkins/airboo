update stations_airnow_temp_2
set location_coord = ST_GeomFromText(
    'point(' || longitude || ' ' || latitude || ')',4326
);