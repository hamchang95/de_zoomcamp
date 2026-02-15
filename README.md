# Data Engineering Zoomcamp
This is a repo to review lessons and complete homeworks for DE Zoomcamp 2026.

# Homework Links
Week 1: 
Week 2: [🔗](https://github.com/hamchang95/de_zoomcamp/blob/main/wk2_hw/q1_q6.sql)
Week 3: [🔗](https://github.com/hamchang95/de_zoomcamp/blob/main/wk3_hw/q1_q9.sql)
Week 4: [🔗](https://github.com/hamchang95/de_zoomcamp/blob/main/wk4_hw/q1_q6.md)

# Week 4 HW
## Question 1. dbt Lineage and Execution
Given a dbt project with the following structure:

models/
├── staging/
│   ├── stg_green_tripdata.sql
│   └── stg_yellow_tripdata.sql
└── intermediate/
    └── int_trips_unioned.sql (depends on stg_green_tripdata & stg_yellow_tripdata)
If you run dbt run --select int_trips_unioned, what models will be built?

*stg_green_tripdata, stg_yellow_tripdata, and int_trips_unioned (upstream dependencies)*

## Question 2. dbt Tests
You've configured a generic test like this in your schema.yml:

columns:
  - name: payment_type
    data_tests:
      - accepted_values:
          arguments:
            values: [1, 2, 3, 4, 5]
            quote: false
Your model fct_trips has been running successfully for months. A new value 6 now appears in the source data.

What happens when you run dbt test --select fct_trips?

*dbt will fail the test, returning a non-zero exit code*

Question 3. Counting Records in fct_monthly_zone_revenue
After running your dbt project, query the fct_monthly_zone_revenue model.

What is the count of records in the fct_monthly_zone_revenue model?

*15,421*

## Question 4. Best Performing Zone for Green Taxis (2020)
Using the fct_monthly_zone_revenue table, find the pickup zone with the highest total revenue (revenue_monthly_total_amount) for Green taxi trips in 2020.

Which zone had the highest revenue?

*East Harlem North*

## Question 5. Green Taxi Trip Counts (October 2019)
Using the fct_monthly_zone_revenue table, what is the total number of trips (total_monthly_trips) for Green taxis in October 2019?

*384,624*

select pickup_zone, max(revenue_monthly_total_amount) as max_revenue
from dbt_prod.fct_monthly
where service_type = 'green' and 
revenue_month >= '2020-01-01' and
revenue_month < '2021-01-01'
group by pickup_zone
order by max_revenue desc
limit 1;

select sum(total_monthly_trips)
from dbt_prod.fct_monthly
where service_type = 'green' and 
revenue_month >= '2019-10-01' and
revenue_month < '2019-11-01';

## Question 6. Build a Staging Model for FHV Data
Create a staging model for the For-Hire Vehicle (FHV) trip data for 2019.

Load the FHV trip data for 2019 into your data warehouse
Create a staging model stg_fhv_tripdata with these requirements:
Filter out records where dispatching_base_num IS NULL
Rename fields to match your project's naming conventions (e.g., PUlocationID → pickup_location_id)
What is the count of records in stg_fhv_tripdata?

*43,244,693*

WITH stg_fhv AS(
    SELECT
        dispatching_base_num,
        pickup_datetime,
        `dropOff_datetime` as dropoff_datetime,
        `PUlocationID` as pickup_location_id,
        `DOlocationID` as dropoff_location_id,
        `SR_Flag` as sr_flag,
        `Affiliated_base_number` as affiliated_base_number
    FROM 
    {{source('raw_data', 'external_fhv')}}
    WHERE dispatching_base_num IS NOT NULL
)

SELECT 
    COUNT(1)
FROM stg_fhv

--Q9. Write a SELECT count(*) query FROM the materialized table you created. How many bytes does it estimate will be read? Why?
SELECT COUNT(*)
FROM ny_taxi.yellow_tripdata;
--A9. This query will process 0 B when run as BigQuery stores row counts as table metadata.
