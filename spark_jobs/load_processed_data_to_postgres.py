from config.aws_config import PROCESSED_TABLE_NAME, POSTGRESQL_CONFIG

def write_processed_data_to_postgres(df):
    df.write \
         .format("jdbc") \
         .option("url", POSTGRESQL_CONFIG['url']) \
         .option("dbtable", PROCESSED_TABLE_NAME) \
         .option("user", POSTGRESQL_CONFIG['user']) \
         .option("password", POSTGRESQL_CONFIG['password']) \
         .option("driver", POSTGRESQL_CONFIG['driver']) \
         .mode("append") \
         .save()
