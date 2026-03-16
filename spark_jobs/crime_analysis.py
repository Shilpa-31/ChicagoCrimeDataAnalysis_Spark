from pyspark.sql.functions import to_timestamp, col
from config.aws_config import get_postgres_connection_properties

class CrimeDataAnalysis:
    def __init__(self, spark):
        self.spark = spark
        self.postgres_props = get_postgres_connection_properties()
        self.jdbc_url = self.postgres_props['url']

    def read_data_from_postgres(self):
        # Use correct SQL query depending on 'Date' column type (assuming it's TEXT/VARCHAR here)
        query = """
            (SELECT * FROM processed_chicago_crime_data 
             WHERE to_timestamp("Date", 'MM/DD/YYYY HH12:MI:SS AM') >= TIMESTAMP '2021-01-01 00:00:00') AS subquery
        """
        df = self.spark.read.format("jdbc") \
            .option("url", self.jdbc_url) \
            .option("dbtable", query) \
            .option("user", self.postgres_props["user"]) \
            .option("password", self.postgres_props["password"]) \
            .option("driver", "org.postgresql.Driver") \
            .load()
        return df

    def transform_date_column(self, df):
        # Parse "Date" string into proper timestamp format
        df = df.withColumn("ParsedDate", to_timestamp(col("Date"), "MM/dd/yyyy hh:mm:ss a"))
        return df

    def save_to_postgres(self, df):
        df.write.mode("overwrite").jdbc(
            url=self.jdbc_url,
            table="analysed_chicago_crime_data",
            properties=self.postgres_props
        )

    def run_analysis(self):
        print("Reading filtered data from PostgreSQL...")
        df = self.read_data_from_postgres()
        
        count = df.count()
        print(f"Rows fetched for analysis: {count}")
        if count == 0:
            print("⚠️ No data returned from query! Check date format and column type.")
            return

        print("Converting date column to timestamp...")
        df = self.transform_date_column(df)

        print("Writing analysed data to PostgreSQL...")
        self.save_to_postgres(df)

        print("Crime analysis completed.")