# Data Engineering Zoomcamp
This is a repo to review lessons and complete homeworks for DE Zoomcamp 2026.

# Homework Links
Week 1: 
Week 2: [🔗](https://github.com/hamchang95/de_zoomcamp/blob/main/wk2_hw/q1_q6.sql)
Week 3: [🔗](https://github.com/hamchang95/de_zoomcamp/blob/main/wk3_hw/q1_q9.sql)
Week 4: [🔗](https://github.com/hamchang95/de_zoomcamp/blob/main/wk4_hw/q1_q6.md)
Week 5: [🔗](https://github.com/hamchang95/de_zoomcamp/blob/main/wk5_hw/q1_q7.md)
# Week 5 HW 
### Question 1. Bruin Pipeline Structure

In a Bruin project, what are the required files/directories?

- `bruin.yml` and `assets/`
- `.bruin.yml` and `pipeline.yml` (assets can be anywhere)
- **`.bruin.yml` and `pipeline/` with `pipeline.yml` and `assets/`**
- `pipeline.yml` and `assets/` only

---

### Question 2. Materialization Strategies

You're building a pipeline that processes NYC taxi data organized by month based on `pickup_datetime`. Which incremental strategy is best for processing a specific interval period by deleting and inserting data for that time period?

- `append` - always add new rows
- `replace` - truncate and rebuild entirely
- **`time_interval` - incremental based on a time column**
- `view` - create a virtual table only

---

### Question 3. Pipeline Variables

You have the following variable defined in `pipeline.yml`:

```yaml
variables:
  taxi_types:
    type: array
    items:
      type: string
    default: ["yellow", "green"]
```

How do you override this when running the pipeline to only process yellow taxis?

- `bruin run --taxi-types yellow`
- `bruin run --var taxi_types=yellow`
- **`bruin run --var 'taxi_types=["yellow"]'`**
- `bruin run --set taxi_types=["yellow"]`

---

### Question 4. Running with Dependencies

You've modified the `ingestion/trips.py` asset and want to run it plus all downstream assets. Which command should you use?

- `bruin run ingestion.trips --all`
- **`bruin run ingestion/trips.py --downstream`**
- `bruin run pipeline/trips.py --recursive`
- `bruin run --select ingestion.trips+`

---

### Question 5. Quality Checks

You want to ensure the `pickup_datetime` column in your trips table never has NULL values. Which quality check should you add to your asset definition?

- `name: unique`
- **`name: not_null`**
- `name: positive`
- `name: accepted_values, value: [not_null]`

---

### Question 6. Lineage and Dependencies

After building your pipeline, you want to visualize the dependency graph between assets. Which Bruin command should you use?

- `bruin graph`
- `bruin dependencies`
- **`bruin lineage`**
- `bruin show`

---

### Question 7. First-Time Run

You're running a Bruin pipeline for the first time on a new DuckDB database. What flag should you use to ensure tables are created from scratch?

- `--create`
- `--init`
- **`--full-refresh`**
- `--truncate`
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

## Question 3. Counting Records in fct_monthly_zone_revenue
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

