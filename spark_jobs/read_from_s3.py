from pyspark.sql import SparkSession
from config import aws_config

def read_csv_from_s3(spark):
    # Read full data from S3 using the passed Spark session
    df = spark.read.csv(aws_config.S3_PATH, header=True, inferSchema=True)

    return df
