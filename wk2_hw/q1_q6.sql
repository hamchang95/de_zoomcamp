--Q1
--Within the execution for Yellow Taxi data for the year 2020 and month 12: what is the uncompressed file size (i.e. the output file yellow_tripdata_2020-12.csv of the extract task)?

--A1
--128.3 MiB

--Q2
--What is the rendered value of the variable file when the inputs taxi is set to green, year is set to 2020, and month is set to 04 during execution?

--A2
--green_tripdata_2020-04.csv

--Q3
--How many rows are there for the Yellow Taxi data for all CSV files in the year 2020?
SELECT COUNT(1) FROM
yellow_tripdata
WHERE filename LIKE '%2020%';

--A3
--24,648,499

--Q4
--How many rows are there for the Green Taxi data for all CSV files in the year 2020?
SELECT COUNT(1) FROM
green_tripdata
WHERE filename LIKE '%2020%';
--1,734,051

--Q5
--How many rows are there for the Yellow Taxi data for the March 2021 CSV file?
SELECT COUNT(1) FROM
yellow_tripdata
WHERE filename LIKE '%2021-03%';
--1,925,152

--Q6
--How would you configure the timezone to New York in a Schedule trigger?
--Add a timezone property set to America/New_York in the Schedule trigger configuration
