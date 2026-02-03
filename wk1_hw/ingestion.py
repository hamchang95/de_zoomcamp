#!/usr/bin/env python
# coding: utf-8

# ## Set Up

import pandas as pd
import pyarrow
import os

# load data
trip = pd.read_parquet('https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet')
zones = pd.read_csv('https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv')
print("data downloaded")

# ## Inesert tables into postgres db
# create engine to insert data into the PostgreSQL database ny_taxi
from sqlalchemy import create_engine
DB_HOST = os.getenv("DB_HOST", "postgres")
engine = create_engine(
    f"postgresql+psycopg://root:root@{DB_HOST}:5432/ny_taxi"
)

# insert headers first
trip.head(n=0).to_sql(name='green_trip_data', con=engine, if_exists='replace')
zones.head(n=0).to_sql(name='taxi_zone', con=engine, if_exists='replace')
print("headers inserted")

# insert rest 
trip.to_sql(name='green_trip_data', con=engine, if_exists='append')
zones.to_sql(name='taxi_zone', con=engine, if_exists='append')
print("insert completed")
