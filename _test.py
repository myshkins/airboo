import csv
from datetime import timedelta, datetime as dt

import requests
import pandas as pd

BASE_URL = "https://s3-us-west-1.amazonaws.com//files.airnowtech.org/airnow/"

URL = "https://s3-us-west-1.amazonaws.com//files.airnowtech.org/airnow/2022/20221221/Monitoring_Site_Locations_V2.dat"
rul2 = "https://s3-us-west-1.amazonaws.com//files.airnowtech.org/airnow/2022/20221114/Monitoring_Site_Locations_V2.dat"


yesterday = (dt.now() - timedelta(days=1)).strftime("%Y%m%d")
year = dt.now().year
url = f"{BASE_URL}{year}/{yesterday}/Monitoring_Site_Locations_V2.dat"

def get_station_data():
    """gets station data file from airnow.org and writes it to .csv"""
    with open('site-data.csv', mode='w') as file:
        response = requests.get(url)
        file.write(response.text)
    # csv_reader = csv.reader(file, delimiter="|")

def shape_station_data():
    """reads station data from csv and shapes it with pandas"""
    df = pd.read_csv("site-data.csv", delimiter="|")
    df = df.drop(["StationID","AQSID","FullAQSID","MonitorType","SiteCode","AgencyID", "EPARegion","CBSA_ID","CBSA_Name","StateAQSCode","StateAbbreviation", "Elevation", "GMTOffset", "CountyName", "CountyAQSCode"], axis=1)
    df = df.groupby("CountryFIPS").get_group("US")
    df = df.groupby("Status").get_group("Active")
    df = df.drop(["Status", "CountryFIPS"], axis=1)
    param_groups = df.groupby("Parameter")
    PM2_5 = param_groups.get_group("PM2.5").drop("Parameter", axis=1)
    PM10 = param_groups.get_group("PM10").drop("Parameter", axis=1)
    df = pd.merge(
        PM10,
        PM2_5,
        how="outer",
        on=["Latitude", "Longitude", "SiteName", "AgencyName"],
    )
    df = df.drop_duplicates(subset="SiteName", keep='first')
    df = df.replace({',': '-'}, regex=True)
    df.to_csv('site-data.csv', header=False, index=False)

get_station_data()
shape_station_data()