COPY stations_airnow_temp(
    station_id,
    aqs_id,
    full_aqs_id,
    parameter,
    monitor_type,
    site_code,
    site_name,
    status,
    agency_id,
    agency_name,
    epa_region,
    latitude,
    longitude,
    elevation,
    gmt_offset,
    country_fips,
    cbsa_id,
    cbsa_name,
    state_aqs_code,
    state_abbrev,
    county_code,
    county_name
) 
FROM stdin WITH DELIMITER AS '|' 
NULL AS ''
HEADER;
