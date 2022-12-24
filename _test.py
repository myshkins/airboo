"""airnow etl functions"""
from datetime import datetime as dt, timedelta
import os

import pandas as pd
import requests

params = {
    "startDate": dt.utcnow().strftime('%Y-%m-%dT%H'),
    "endDate": (dt.utcnow() + timedelta(hours=1)).strftime('%Y-%m-%dT%H'),
    "parameters": "OZONE,PM25,PM10,CO,NO2,SO2",
    "BBOX": "-124.205070,28.716781, -75.337882,45.419415",
    "dataType": "B",
    "format": "text/csv",
    "verbose": "1",
    "monitorType": "2",
    "includerawconcentrations": "0",
    "API_KEY": "AA5AB45D-9E64-41DE-A918-14578B9AC816",
}
AIRNOW_BY_STATION_API_URL = "https://www.airnowapi.org/aq/data/"



def extract_current_data():
    """extracts data from airnow api and stages it in csv file."""
    data_path = "site-data.csv"

    response = requests.get(
        AIRNOW_BY_STATION_API_URL, params=params, timeout=20
    )
    csv_data = response.text
    with open(data_path, 'w') as file:
        file.write(csv_data)

def shape_airnow_data(df):
    """
    Uses .groupby() to split 'parameter' column into pm2.5 and pm10 groups.
    Then merge groups together under columns:

    site name | datetime | PM10 conc. | PM10 AQI |
    PM10 AQI cat. | PM2_5 conc. | PM2_5 AQI | PM2_5 AQI cat.
    """
    parameter_groups = df.groupby("parameter")
    pm10 = parameter_groups.get_group("PM10").drop(["parameter"], axis=1)
    pm10.rename(
        columns={
            "concentration": "pm_10_conc",
            "AQI": "pm_10_AQI",
            "AQI cat": "pm_10_cat"},
        inplace=True
    )
    pm10.to_csv('pm10.csv', header=True, index=False)
    pm2_5 = parameter_groups.get_group("PM2.5").drop(["parameter"], axis=1)
    pm2_5.rename(
        columns={
            "concentration": "pm_25_conc",
            "AQI": "pm_25_AQI",
            "AQI cat": "pm_25_AQI_cat"},
        inplace=True
    )
    pm2_5.to_csv('pm25.csv', header=True, index=False)
    merged_df = pd.merge(
        pm10,
        pm2_5,
        how="outer",
        on=["station_name", "datetime"],
        sort=False,
        suffixes=('_x', '_y')
    )
    cols = merged_df.columns.tolist()
    cols = [cols[-4]] + cols[:4] + cols[-3:]
    merged_df = merged_df[cols]
    return merged_df

def load_to_temp():
    """load new data to temp table"""
    column_names = [
        "latitude",
        "longitude",
        "datetime",
        "parameter",
        "concentration",
        "unit",
        "AQI",
        "AQI cat",
        "station_name",
        "agency name",
        "station id",
        "full station id", ]
    df = pd.read_csv(
        "site-data.csv", names=column_names,
    )
    df.dropna(axis=0)
    df = df.drop(
        ["latitude", "longitude", "unit", "agency name", "station id",
         "full station id"],
        axis=1
    )
    df.to_csv('site-data2.csv', header=True, index=False)
    merged_df = shape_airnow_data(df)
    merged_df = merged_df.replace({',': '-'}, regex=True)
    merged_df.to_csv('merged-data.csv', header=True, index=False)

extract_current_data()
load_to_temp()
