update stations_airnow_temp
set location_coord = ST_GeomFromText(
    'point(' || longitude || ' ' || latitude || ')',4326
);