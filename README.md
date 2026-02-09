# Data Engineering Zoomcamp
This is a repo to review lessons and complete homeworks for DE Zoomcamp 2026.

# Homework Links
Week 1: 
Week 2: [🔗](https://github.com/hamchang95/de_zoomcamp/blob/main/wk2_hw/q1_q6.sql)
Week 3: [🔗](https://github.com/hamchang95/de_zoomcamp/blob/main/wk3_hw/q1_q9.sql)

# Week 3 HW
--Create an external table using the Yellow Taxi Trip Records.
CREATE OR REPLACE EXTERNAL TABLE `ny_taxi.external_yellow`
OPTIONS (
    format = 'PARQUET',
    uris = ['gs://{bucket_name}/*.parquet']
);

-- Create a non partitioned table from external table
CREATE OR REPLACE TABLE ny_taxi.yellow_tripdata AS
SELECT * FROM ny_taxi.external_yellow;

--Q1. What is count of records for the 2024 Yellow Taxi Data?
SELECT COUNT(1)
FROM
ny_taxi.external_yellow;

--A1. 20332093

--Q2. Write a query to count the distinct number of PULocationIDs for the entire dataset on both the tables.
-- What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?
SELECT COUNT(DISTINCT(PULocationID))
FROM ny_taxi.external_yellow;
--This query will process 0 B when run.

SELECT COUNT(DISTINCT(PULocationID))
FROM ny_taxi.yellow_tripdata;
--This query will process 155.12 MB when run.
--A2. 0 MB for the External Table and 155.12 MB for the Materialized Table

--Q3. Write a query to retrieve the PULocationID from the table (not the external table) in BigQuery. Now write a query to retrieve the PULocationID and DOLocationID on the same table. Why are the estimated number of Bytes different?
SELECT PULocationID
FROM ny_taxi.yellow_tripdata;
--This query will process 155.12 MB when run.

SELECT PULocationID, DOLocationID
FROM ny_taxi.yellow_tripdata;
--This query will process 310.24 MB when run.
--A3. BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed.

--Q4. How many records have a fare_amount of 0?
SELECT COUNT(1)
FROM ny_taxi.external_yellow
WHERE fare_amount = 0;

--A4. 8,333

--Q5. What is the best strategy to make an optimized table in Big Query if your query will always filter based on tpep_dropoff_datetime and order the results by VendorID (Create a new table with this strategy)
CREATE OR REPLACE TABLE ny_taxi.yellow_tripdata_partitioned_clustered
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID AS
SELECT * FROM ny_taxi.external_yellow;
--A5. Partition by tpep_dropoff_datetime and Cluster on VendorID

--Q6. Write a query to retrieve the distinct VendorIDs between tpep_dropoff_datetime 2024-03-01 and 2024-03-15 (inclusive)
--Use the materialized table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 5 and note the estimated bytes processed. What are these values?
SELECT DISTINCT(VendorID)
FROM ny_taxi.yellow_tripdata_partitioned_clustered
WHERE tpep_dropoff_datetime >= '2024-03-01' AND tpep_dropoff_datetime <= '2024-03-15';
--This query will process 26.84 MB when run.

SELECT DISTINCT(VendorID)
FROM ny_taxi.yellow_tripdata
WHERE tpep_dropoff_datetime >= '2024-03-01' AND tpep_dropoff_datetime <= '2024-03-15';
--This query will process 310.24 MB when run.

--A6. 310.24 MB for non-partitioned table and 26.84 MB for the partitioned table

--Q7. Where is the data stored in the External Table you created?
--A7. GCP Bucket

--Q8. It is best practice in Big Query to always cluster your data:
--A8. False

--Q9. Write a SELECT count(*) query FROM the materialized table you created. How many bytes does it estimate will be read? Why?
SELECT COUNT(*)
FROM ny_taxi.yellow_tripdata;
--A9. This query will process 0 B when run as BigQuery stores row counts as table metadata.
