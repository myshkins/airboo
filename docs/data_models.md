## How do we model this stuff anyhow?
--- 

### World Air Quality Index feed:
Example request: https://api.waqi.info/feed/geo:40.04967209583848;-105.28730354750316/?token=bb10d851797e497b46823a5b4f984354c6ff4d9a

We could do fact tables by feed, and dimension tables for city / geo data


WAQI fact table would be

--- 
|column_name|type|length|notes|example|
|-----------|----|------|-----|-------|
|station_name|varchar()|500|guessed length|Athens, Boulder-CU, Colorado, USA|
|reading_datetime|datetime|||2022-12-04 17:00:00|
|latitude|float|||40.012969|
|longitude|float|||-105.267212|
|pm10|float|||26|   
|pm25|float|||30|
|co|float|||1.9|
|h|float|||48.5|   
|no2|float|||9.2|


