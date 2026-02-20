"""@bruin

# TODO: Set the asset name (recommended pattern: schema.asset_name).
# - Convention in this module: use an `ingestion.` schema for raw ingestion tables.
name: ingestion.trips

# TODO: Set the asset type.
# Docs: https://getbruin.com/docs/bruin/assets/python
type: python

# TODO: Pick a Python image version (Bruin runs Python in isolated environments).
# Example: python:3.11
image: python:3.11

# TODO: Set the connection.
connection: duckdb-default

# TODO: Choose materialization (optional, but recommended).
# Bruin feature: Python materialization lets you return a DataFrame (or list[dict]) and Bruin loads it into your destination.
# This is usually the easiest way to build ingestion assets in Bruin.
# Alternative (advanced): you can skip Bruin Python materialization and write a "plain" Python asset that manually writes
# into DuckDB (or another destination) using your own client library and SQL. In that case:
# - you typically omit the `materialization:` block
# - you do NOT need a `materialize()` function; you just run Python code
# Docs: https://getbruin.com/docs/bruin/assets/python#materialization
materialization:
  # TODO: choose `table` or `view` (ingestion generally should be a table)
  type: table
  # TODO: pick a strategy.
  # suggested strategy: append
  strategy: append

# TODO: Define output columns (names + types) for metadata, lineage, and quality checks.
# Tip: mark stable identifiers as `primary_key: true` if you plan to use `merge` later.
# Docs: https://getbruin.com/docs/bruin/assets/columns
columns:
  - name: pickup_datetime
    type: timestamp
    description: "When the meter was engaged"
  - name: dropoff_datetime
    type: timestamp
    description: "When the meter was disengaged"

@bruin"""

# TODO: Add imports needed for your ingestion (e.g., pandas, requests).
import os
os.environ["TZDIR"] = ""

import json
import pandas as pd
from datetime import datetime, timedelta
import io
import requests

# - Put dependencies in the nearest `requirements.txt` (this template has one at the pipeline root).
# Docs: https://getbruin.com/docs/bruin/assets/python
import pyarrow.parquet as pq
import pyarrow as pa

def read_parquet_no_tz(content):
    table = pq.read_table(io.BytesIO(content))
    # cast any tz-aware timestamp columns to tz-naive
    new_fields = []
    for i, field in enumerate(table.schema):
        if pa.types.is_timestamp(field.type) and field.type.tz is not None:
            new_fields.append(field.with_type(pa.timestamp(field.type.unit)))
        else:
            new_fields.append(field)
    new_schema = pa.schema(new_fields)
    return table.cast(new_schema).to_pandas()

import pyarrow.compute as pc

def make_timestamps_utc(df: pd.DataFrame) -> pd.DataFrame:
    """Convert all naive timestamp columns to UTC-aware at PyArrow level"""
    table = pa.Table.from_pandas(df)
    new_fields = []
    new_columns = []
    
    for i, field in enumerate(table.schema):
        col = table.column(i)
        if pa.types.is_timestamp(field.type) and field.type.tz is None:
            # Cast to UTC without assume_timezone (no tzdb needed)
            new_type = pa.timestamp(field.type.unit, tz="UTC")
            new_col = col.cast(new_type)
            new_fields.append(field.with_type(new_type))
            new_columns.append(new_col)
        else:
            new_fields.append(field)
            new_columns.append(col)
    
    return pa.Table.from_arrays(new_columns, schema=pa.schema(new_fields)).to_pandas()
# TODO: Only implement `materialize()` if you are using Bruin Python materialization.
# If you choose the manual-write approach (no `materialization:` block), remove this function and implement ingestion
# as a standard Python script instead.
def materialize():
  start_date = os.environ["BRUIN_START_DATE"]
  end_date = os.environ["BRUIN_END_DATE"]
  taxi_types = json.loads(os.environ["BRUIN_VARS"]).get("taxi_types", ["yellow"])
  print(taxi_types)

  start_dt = datetime.strptime(start_date, "%Y-%m-%d")
  end_dt = datetime.strptime(end_date, "%Y-%m-%d")  # bug fix: was using start_date twice

  # Generate month-start dates within window
  date_range = pd.date_range(start_dt, end_dt - timedelta(days=1), freq="MS")
  print(date_range)
  l_df = []
  
  for taxi_type in taxi_types:
    for date in date_range:
      year = date.year
      month = f"{date.month:02d}"    # zero-pad: 01, 02
      url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/{taxi_type}_tripdata_{year}-{month}.parquet"
      print(url)

      response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
      response.raise_for_status()
      df = read_parquet_no_tz(response.content)
      df["taxi_type"] = taxi_type
      l_df.append(df)      

  df_final = pd.concat(l_df, ignore_index=True)
  df_final["extracted_at"] = os.environ["BRUIN_EXECUTION_DATETIME"]
  df_final = make_timestamps_utc(df_final)
  return df_final


