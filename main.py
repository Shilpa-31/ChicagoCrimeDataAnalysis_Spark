from pyspark.sql import SparkSession
from utils.api_to_s3Bucket import fetch_crime_data_in_batches, upload_csv_to_s3
from spark_jobs.read_from_s3 import read_csv_from_s3
from spark_jobs.load_raw_to_postgres import load_raw_data_to_postgres
from spark_jobs.transform_data import clean_and_validate_data
from spark_jobs.load_processed_data_to_postgres import write_processed_data_to_postgres
from spark_jobs.crime_analysis import CrimeDataAnalysis
from config.aws_config import AWS_ACCESS_KEY, AWS_SECRET_KEY, S3_PATH
import boto3
from pyspark.sql.functions import col
import re

# Function to convert column names to lowercase and snake_case
def convert_column_names(df):
    new_columns = [re.sub(r'([a-z])([A-Z])', r'\1_\2', c).lower() for c in df.columns]
    return df.toDF(*new_columns)

def main():
    # Set up Spark session
    spark = SparkSession.builder \
        .appName("ChicagoCrimeDataPipeline") \
        .config("spark.hadoop.fs.s3a.access.key", AWS_ACCESS_KEY) \
        .config("spark.hadoop.fs.s3a.secret.key", AWS_SECRET_KEY) \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .getOrCreate()

    API_URL = "https://data.cityofchicago.org/resource/ijzp-q8t2.csv"  # Chicago crime API link
    BUCKET_NAME = "x23269791-datauser"         # AWS s3 Bucket name
    S3_KEY = "DataIntensive/chicago_crime_data.csv"   # Path of csv file to store into s3 bucket.

    # Step 1: Fetching chicago crime records from public API
    print("Fetching crime data from API...")
    crime_data = fetch_crime_data_in_batches(API_URL, limit=1000, bucket_name=BUCKET_NAME, s3_key=S3_KEY)

    # Step 2: Uploading chicago crime records into AWS s3
    print("Uploading raw data to AWS S3 bucket...!!")
    upload_csv_to_s3(crime_data, BUCKET_NAME, S3_KEY)

    # Step 3: Read CSV from AWS s3 bucket
    print("Reading data from s3 bucket..!")
    df_raw = read_csv_from_s3(spark)

    # Preview schema to validate data
    df_raw.printSchema()

    # Step 4: Load raw data(pre-processed data) into PostgreSQL
    print("Loading raw data into PostgreSQL..!")
    load_raw_data_to_postgres(df_raw)
    
    # Step 5: Clean and transform the data
    print("Transforming the data records....!")
    df_cleaned = clean_and_validate_data(df_raw)
    
    # Step 6: Load cleaned data to PostgreSQL
    print("Loading processed the data into PostgreSQL....!")
    write_processed_data_to_postgres(df_cleaned)

    print("Running crime data analysis...")
    analysis = CrimeDataAnalysis(spark)
    analysis.run_analysis()

    # Closing spark session
    spark.stop()

    print("Pipeline completed successfully.")


if __name__ == "__main__":
    main()
