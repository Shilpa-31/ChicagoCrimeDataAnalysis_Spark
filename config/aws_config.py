# AWS and PostgreSQL config values

AWS_ACCESS_KEY = "AKIAZJVZ3F5IJ47X2E5F"
AWS_SECRET_KEY = "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"
S3_BUCKET = "x23269791-datauser"
S3_PATH = "s3a://x23269791-datauser/DataIntensive/Chicago_crime_data.csv"
AWS_REGION = 'eu-west-1'

# PostgreSQL Configuration
POSTGRESQL_CONFIG = {
    "url": "jdbc:postgresql://localhost:5433/myDatabase",
    "user": "{YOUR-USER NAME}",
    "password": "{YOUR PASSWORD}",
    "driver": "org.postgresql.Driver"
}

# Table name
RAW_TABLE_NAME = "raw_chicago_crime_data"
PROCESSED_TABLE_NAME = "processed_chicago_crime_data"

def get_postgres_connection_properties():
    return {
        "url": "jdbc:postgresql://localhost:5433/myDatabase",
        "user": "{YOUR-USER NAME}",
        "password": "{YOUR PASSWORD}",
        "driver": "org.postgresql.Driver"
    }