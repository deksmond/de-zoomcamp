# NYC Green Taxi Data Ingestion

This guide provides instructions for setting up the environment and ingesting NYC Green Taxi trip data and taxi zone data into a PostgreSQL database.

## Prerequisites

Ensure you have the following installed on your machine:

- Docker
- Python (with necessary libraries installed, e.g., `psycopg2`, `pandas`)

## Steps

### 1. Run Docker Compose

Start the PostgreSQL database using Docker Compose:

```bash
docker compose up
```

### 2. Ingest Green Taxi Trip Data

Download and ingest the Green Taxi trip data (for November 2025) into the PostgreSQL database.

Install dependencies:

```bash
pip install sqlalchemy pandas psycopg2-binary
```

Ingest data:

```bash
URL="https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet"
python ingest_data.py \
  --user=postgres \
  --password=postgres \
  --host=localhost \
  --port=5433 \
  --db=ny_taxi \
  --table_name=green_taxi_trips \
  --url=${URL}
```

### 3. Ingest Green Taxi Zone Data

Download and ingest the green taxi zone lookup data into the database:

```bash
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv"
python ingest_data.py \
  --user=postgres \
  --password=postgres \
  --host=localhost \
  --port=5433 \
  --db=ny_taxi \
  --table_name=green_taxi_zones \
  --url=${URL}
```

## SQL Queries

### Question 1: Understanding Docker Images

Run docker with the `python:3.13` image. Use an entrypoint bash to interact with the container.

**What's the version of pip in the image?**

```bash
docker run -it --entrypoint bash python:3.13
```

Once inside the container, check the pip version:

```bash
pip --version
```

### Question 3: Counting Short Trips

For trips in November 2025 with trip distance of less than or equal to 1 mile.

**Query:**

```sql
SELECT COUNT(*) as trip_count
FROM public."Green_taxi"
WHERE DATE_PART('year', lpep_pickup_datetime) = 2025
  AND DATE_PART('month', lpep_pickup_datetime) = 11
  AND trip_distance <= 1;
```

### Question 4: Longest Trip for Each Day

The pick up day with the longest trip distance (only considering trips in the trip_distance column < 100 miles to exclude data errors).

**Query:**

```sql
SELECT 
  DATE(lpep_pickup_datetime) as pickup_day,
  trip_distance,
  ROW_NUMBER() OVER (ORDER BY trip_distance DESC) as rank
FROM public."Green_taxi"
WHERE trip_distance < 100
ORDER BY trip_distance DESC
LIMIT 1;
```

### Question 5: Biggest Pickup Zone

The pickup zone with the largest total_amount (sum of all trips) on November 18th, 2025.

**Query:**

```sql
SELECT 
  z."Zone",
  SUM(g."total_amount") AS total_revenue
FROM public."Green_taxi" g
JOIN zones z ON g."PULocationID" = z."LocationID"
WHERE DATE(g."lpep_pickup_datetime") = '2025-11-18'
GROUP BY z."Zone"
ORDER BY total_revenue DESC
LIMIT 1;
```

### Question 6: Largest Tip

The drop off zone that had the largest tip for the passengers picked up in the zone named "East Harlem North" in November 2025.

**Query:**

```sql
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
```