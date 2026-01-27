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