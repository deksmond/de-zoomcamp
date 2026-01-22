import pandas as pd

# Install psycopg to enable a database connection using defined parameters
# !uv add psycopg2-binary
# Install sql alchemy (via command line) and adds it to the pyproject.toml dependency tree 
# !uv add sql alchemy
from sqlalchemy import create_engine
# Install tqdm, a package to monitor progress. Like a progress bar or activity indicator
#!uv add tqdm
# View progress of data ingestion in chunks
from tqdm.auto import tqdm


# Data type definition for all fields to fix dtype error

dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

def run():
    pg_user = 'root'
    pg_pass = 'root'
    pg_host = 'localhost'
    pg_port =  5432
    pg_db =    'ny_taxi'
    
    year = 2021
    month = 1
    
    target_table = 'yellow_taxi_data'
    chunksize = 100000
    
    prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow'
    url = f'{prefix}/yellow_tripdata_{year}-{month:02d}.csv.gz'
    
    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')

    # View the db schema
    #print(pd.io.sql.get_schema(df, name='yellow_taxi_data', con=engine))

    df_iter = pd.read_csv(
        url,
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=chunksize
    )

    first = True
    
    for df_chunk in tqdm(df_iter):
        if first:
            df_chunk.to_sql(
                name = target_table, 
                con = engine, 
                if_exists = 'replace'
                )
            first = False
        
        df_chunk.to_sql(
                name = target_table, 
                con = engine, 
                if_exists = 'append'
                )
        
        
if __name__ == '__main__':
    run()