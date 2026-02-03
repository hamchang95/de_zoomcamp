import sys
import pandas as pd

trip = pd.read_parquet('data/green_tripdata_2025-11.parquet')
zone = pd.read_csv('data/taxi_zone_lookup.csv')

print(trip.head())

print(zone.head())
