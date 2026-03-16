from pyspark.sql.functions import col
from pyspark.sql.types import BooleanType
from pyspark.sql import DataFrame

def clean_and_validate_data(df: DataFrame) -> DataFrame:

    # Drop unwanted columns: x_coordinate, y_coordinate, ward, and year
    df = df.drop("x coordinate", "y coordinate", "ward", "year")

    # Drop critical nulls
    df = df.dropna()

    # Cast columns to appropriate types
    df = df \
        .withColumn("Arrest", col("Arrest").cast(BooleanType())) \
        .withColumn("Domestic", col("Domestic").cast(BooleanType())) \

    return df
