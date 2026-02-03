--q3
select count(trip_distance)
from green_trip_data
where lpep_pickup_datetime >= '2025-11-01'
and lpep_pickup_datetime <= '2025-12-01'
and trip_distance <= 1;

--q3 answer
--8007

--q4
select lpep_pickup_datetime 
from green_trip_data 
where trip_distance = (select max(trip_distance) from green_trip_data
where trip_distance < 100)

--q4 answer
2025-11-14 15:36:27

--q5 
SELECT pu."Zone",
       SUM(g.total_amount) AS zone_total
FROM green_trip_data g
JOIN taxi_zone pu
  ON g."PULocationID" = pu."LocationID"
WHERE g."lpep_pickup_datetime" >= '2025-11-18'
  AND g."lpep_pickup_datetime" <  '2025-11-19'
GROUP BY pu."Zone"
ORDER BY zone_total DESC
LIMIT 1;

--q5 answer
--East Harlem North

--q6
SELECT dz."Zone" AS dropoff_zone, g.tip_amount
FROM green_trip_data g
JOIN taxi_zone pz  -- pickup zone
  ON g."PULocationID" = pz."LocationID"
JOIN taxi_zone dz  -- dropoff zone
  ON g."DOLocationID" = dz."LocationID"
WHERE pz."Zone" = 'East Harlem North'
  AND g."lpep_pickup_datetime" >= '2025-11-01'
  AND g."lpep_pickup_datetime" <  '2025-12-01'
  AND g.tip_amount = (
      SELECT MAX(g2.tip_amount)
      FROM green_trip_data g2
      JOIN taxi_zone pz2
        ON g2."PULocationID" = pz2."LocationID"
      WHERE pz2."Zone" = 'East Harlem North'
        AND g2."lpep_pickup_datetime" >= '2025-11-01'
        AND g2."lpep_pickup_datetime" <  '2025-12-01'
  );

--q6 answer
--Yorkville West

--q7
--terraform init, terraform apply -auto-approve, terraform destroy
