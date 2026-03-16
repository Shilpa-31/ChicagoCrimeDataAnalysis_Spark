from pyspark.sql.functions import col, to_timestamp
from config.aws_config import RAW_TABLE_NAME, POSTGRESQL_CONFIG

# Mapping original column names to PostgreSQL-friendly column names
COLUMN_RENAME_MAPPING = {
    "ID": "id",
    "Case Number": "case_number",
    "Date": "date",
    "Block": "block",
    "IUCR": "iucr",
    "Primary Type": "primary_type",
    "Description": "description",
    "Location Description": "location_description",
    "Arrest": "arrest",
    "Domestic": "domestic",
    "Beat": "beat",
    "District": "district",
    "Ward": "ward",
    "Community Area": "community_area",
    "FBI Code": "fbi_code",
    "X Coordinate": "x_coordinate",
    "Y Coordinate": "y_coordinate",
    "Year": "year",
    "Updated On": "updated_on",
    "Latitude": "latitude",
    "Longitude": "longitude",
    "Location": "location"
}

def load_raw_data_to_postgres(df):
    # Rename columns based on the mapping
    for original, new in COLUMN_RENAME_MAPPING.items():
        df = df.withColumnRenamed(original, new)

    # Cast columns to the appropriate data types
    df = df.withColumn("id", col("id").cast("string")) \
           .withColumn("year", col("year").cast("integer")) \
           .withColumn("latitude", col("latitude").cast("double")) \
           .withColumn("longitude", col("longitude").cast("double")) \
           .withColumn("x_coordinate", col("x_coordinate").cast("double")) \
           .withColumn("y_coordinate", col("y_coordinate").cast("double"))

    # Convert 'date' and 'updated_on' to timestamp (handle possible date format)
    df = df.withColumn("date", to_timestamp(col("date"), "MM/dd/yyyy hh:mm:ss a")) \
           .withColumn("updated_on", to_timestamp(col("updated_on"), "MM/dd/yyyy hh:mm:ss a"))

    # Optional: Check schema to verify the column names and types
    df.printSchema()

    # Write to PostgreSQL
    df.write \
         .format("jdbc") \
         .option("url", POSTGRESQL_CONFIG['url']) \
         .option("dbtable", RAW_TABLE_NAME) \
         .option("user", POSTGRESQL_CONFIG['user']) \
         .option("password", POSTGRESQL_CONFIG['password']) \
         .option("driver", POSTGRESQL_CONFIG['driver']) \
         .mode("append") \
         .save()

    print("Data loaded successfully into PostgreSQL.")
