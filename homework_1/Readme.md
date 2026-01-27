NYC Green Taxi Data Ingestion for Homework 1

This is a guide to set up the environment and ingest NYC green taxi and taxi zone datasets into Postgres database. 

Prerequisites

- Docker: ensure you have this using docker --version on the terminal
- Python (with necessary libraries installed, e.g., psycopg2, pandas)

Steps

1. Docker Compose
Start the PostgreSQL database using Docker Compose

docker compose up

2. Ingest the Green Taxi Trip data 
Download and ingest the Green Taxi trip data (for November 2025) into the PostgreSQL database

install dependencies: sqlalchemy and pandas
pip install sqlalchemy pandas psycopg2-binary

URL="https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet"
python ingest_data.py \
  --user=postgres \
  --password=postgres \
  --host=db \
  --port=5432 \
  --db=ny_taxi \
  --table_name=green_taxi_trips \
  --url=${URL}

3. Ingest the Green Taxi Zone data
Download and ingest the Green Taxi zone data into the PostgreSQL database

URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv"
python ingest_data.py \
  --user=postgres \
  --password=postgres \
  --host=localhost \
  --port=5433 \
  --db=ny_taxi \
  --table_name=green_taxi_zones \
  --url=${URL}


Question 1. Understanding Docker images

Run docker with the python:3.13 image. Use an entrypoint bash to interact with the container.

What's the version of pip in the image?
Answer: 
cd into the right directory

Run 
docker run -it --entrypoint bash python:3.13

Once inside the container check the version inside the container
pip --version 


Question 3. Counting short trips
For trips in November 2025 with trip trip_distance of less than or equal to 1 mile

SELECT COUNT(*) as trip_count
FROM public."Green_taxi"
WHERE DATE_PART('year', lpep_pickup_datetime) = 2025
  AND DATE_PART('month', lpep_pickup_datetime) = 11
  AND trip_distance <= 1;


Question 4. Longest trip for each day
The pick up day with the logest trip distance (only considering trips in the trip_distance column < 100 miles to exclude data errors)

SELECT 
  DATE(lpep_pickup_datetime) as pickup_day,
  trip_distance,
  ROW_NUMBER() OVER (ORDER BY trip_distance DESC) as rank
FROM public."Green_taxi"
WHERE trip_distance < 100
ORDER BY trip_distance DESC
LIMIT 1;


Question 5. Biggest pickup zone
The pickup zone with the largest total_amount (sum of all trips) on November 18th, 2025.

SELECT 
  z."Zone",
  SUM(g."total_amount") AS total_revenue
FROM public."Green_taxi" g
JOIN zones z ON g."PULocationID" = z."LocationID"
WHERE DATE(g."lpep_pickup_datetime") = '2025-11-18'
GROUP BY z."Zone"
ORDER BY total_revenue DESC
LIMIT 1;


Question 6. Largest tip
The drop off zone that had the largest tip for the passengers picked up in the zone named "East Harlem North" in November 2025.

SELECT 
  z."Zone" as dropoff_zone,
  g."tip_amount"
FROM public."Green_taxi" g
JOIN zones z ON g."DOLocationID" = z."LocationID"
JOIN zones pz ON g."PULocationID" = pz."LocationID"
WHERE pz."Zone" = 'East Harlem North'
  AND EXTRACT(YEAR FROM g."lpep_pickup_datetime") = 2025
  AND EXTRACT(MONTH FROM g."lpep_pickup_datetime") = 11
ORDER BY g."tip_amount" DESC
LIMIT 1;