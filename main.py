import os
from math import radians, cos, sin, asin, sqrt

import pandas as pd
from pandas import DataFrame


def get_files(path: str) -> list:
    """ Returns a list of file names find in the path"""
    for root, subdirs, files in os.walk(path):
        return files


def dist(lat1, long1, lat2, long2):
    """
    Replicating the same formula as mentioned in Wiki
    """
    # convert decimal degrees to radians
    lat1, long1, lat2, long2 = map(radians, [lat1, long1, lat2, long2])
    # haversine formula
    dlon = long2 - long1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    # Radius of earth in kilometers is 6371
    miles = 6371 * c
    return miles


def find_nearest(lat, long, data: DataFrame):
    distances = data.apply(
        lambda row: dist(lat, long, row['lat'], row['lon']),
        axis=1)
    return data.loc[distances.idxmin(), 'iata_code']


def main():
    data_dir = "./data/"
    files = get_files(data_dir)

    # Create Dataframes from the csv files
    users_df = None
    airports_df = None
    for file in files:
        if "user" in file:
            users_df = pd.read_csv(data_dir + file)
        elif "airports" in file:
            airports_df = pd.read_csv(data_dir + file)

    # Renaming the names to match the names of the functions
    users_df = users_df.rename(columns={'geoip_latitude': 'lat', 'geoip_longitude': 'lon'})
    airports_df = airports_df.rename(columns={'latitude': 'lat', 'longitude': 'lon'})

    # fetching a portion of the data for testing
    # Uncomment the line below for testing
    # users_df = users_df.head(50)

    users_df['nearest_airport'] = users_df.apply(
        lambda row: find_nearest(row['lat'], row['lon'], airports_df),
        axis=1
    )

    print(users_df[['uuid', 'nearest_airport']].to_markdown())


if __name__ == '__main__':
    main()
