
insert into readings_waqi
(
    station_name,
    longitude,
    latitude,
    reading_datetime,
    request_datetime,
    co,
    h,
    no2,
    o3,
    p,
    pm_10,
    pm_25,
    so2,
    t,
    w,
    wg
)
values
    %(city_name)s,
    %(longitude)s,
    %(latitude)s,
    %(reading_datetime)s,
    %(request_datetime)s,
    %(co)d,
    %(h)d,
    %(no2)d,
    %(o2)d,
    %(p)d,
    %(pm10)d,
    %(pm25)d,
    %(so2)d,
    %(t)d,
    %(w)d,
    %(wg)d
);
-- values
-- (
--     'boulder',
--     104.5,
--     103.5,
--     '2023-1-3',
--     '2023-1-3',
--     3.4,
--     4.5,
--     4.5,
--     4.5,
--     4.5,
--     4.5,
--     4.5,
--     4.5,
--     4.5,
--     4.5,
--     4.5
-- )