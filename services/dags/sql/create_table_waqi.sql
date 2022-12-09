CREATE TABLE IF NOT EXISTS ReadingsWaqi(
            reading_id serial primary key,
            station_name varchar not null,
            reading_datetime timestamp not null,
            latitude    numeric(10,6)
            longitude   numeric(10,6)
            pm_10       numeric(5,3)
            pm_25       numeric(5,3)
            co          numeric(5,3)
            h           numeric(5,3)
            no2         numeric(5,3)
);
