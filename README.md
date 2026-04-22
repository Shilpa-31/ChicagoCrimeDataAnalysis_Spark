# Chicago Crime Data Analysis with Apache Spark

## Overview
This project implements a **data engineering pipeline using Apache Spark** to ingest, process, and analyze Chicago crime data obtained from the **Chicago Open Data API** (https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-Present/ijzp-q8t2/about_data).

The pipeline performs the following operations:
- Data ingestion from a public API: https://data.cityofchicago.org/resource/ijzp-q8t2.json
- Raw data storage in **AWS S3**
- Distributed data processing using **PySpark**
- Data transformation and cleaning
- Data persistence to **PostgreSQL**
- Interactive dashboard generation for crime analytics

The system demonstrates a **scalable Spark-based data processing workflow** integrating **cloud object storage (S3)** and a **relational analytics layer (PostgreSQL)**.

---

# Technology Stack

| Layer | Technology |
|------|-------------|
| Programming Language | Python |
| Distributed Processing | Apache Spark (PySpark) |
| Data Storage | AWS S3 |
| Database | PostgreSQL |
| Data Source | Chicago Open Data API |
| Data Access | Spark JDBC |
| Visualization | Python Dashboard |

---

# Project Structure
```
  CHICAGOCRIMEDATAANALYSIS_SPARK
  │
  ├── config
  │   └── aws_config.py
  │
  ├── jars
  │   └── postgresql-42.7.5.jar  // Compatible version
  │
  ├── spark_jobs
  │   ├── crime_analysis.py
  │   ├── load_processed_data_to_postgres.py
  │   ├── load_raw_to_postgres.py
  │   ├── read_from_s3.py
  │   └── transform_data.py
  │
  ├── utils
  │   └── api_to_s3Bucket.py
  │
  ├── dashboard.py
  ├── main.py
  ├── requirements.txt
  └── README.md
```
---

# System Architecture
```
      +----------------------------+
      | Chicago Open Data API     |
      +------------+--------------+
                   |
                   v
        +-------------------+
        | Data Ingestion    |
        | Python API Client |
        +---------+---------+
                  |
                  v
        +-------------------+
        | AWS S3 Data Lake  |
        | Raw Crime Data    |
        +---------+---------+
                  |
                  v
        +-------------------+
        | Apache Spark      |
        | Data Processing   |
        +---------+---------+
                  |
                  v
        +-------------------+
        | Data Transformation|
        | Cleaning & Schema |
        +---------+---------+
                  |
                  v
        +-------------------+
        | PostgreSQL        |
        | Analytical Layer  |
        +---------+---------+
                  |
                  v
        +-------------------+
        | Visualization     |
        | Crime Dashboard   |
        +-------------------+
```        
---

# Data Pipeline
The pipeline consists of several modular Spark jobs responsible for different stages of data processing.

---

## 1. Data Ingestion
Crime records are fetched from the **Chicago Open Data API** and stored as raw data in an **AWS S3 bucket**.
`utils/api_to_s3Bucket.py`

- Fetch crime data using API requests
- Handle pagination for large datasets
- Convert JSON responses
- Upload raw data to AWS S3

---

## 2. Data Retrieval from S3
Raw crime data is retrieved from the S3 bucket using **Spark**.
`spark_jobs/read_from_s3.py`

Spark loads the dataset into a distributed DataFrame for processing.

---

## 3. Data Transformation and Cleaning
Data preprocessing is performed using **Spark DataFrame transformations**.
`spark_jobs/transform_data.py`

Processing tasks include:
- Handling missing values
- Filtering invalid records
- Standardizing schema
- Data type conversion
- Feature selection

---

## 4. Crime Data Analysis
The `crime_analysis.py` module performs analytical processing on cleaned Chicago crime datasets stored in **PostgreSQL**.


### Processing Steps
- Read processed crime dataset from PostgreSQL using Spark JDBC
- Apply date filtering using SQL predicate pushdown
- Convert raw date strings into Spark timestamps
- Generate analytics-ready dataset
- Persist results back into PostgreSQL

### Data Loading Stages
Raw data loading: `spark_jobs/load_raw_to_postgres.py`
Processed data loading: `spark_jobs/load_processed_data_to_postgres.py`

---

## 5. Dashboard
A Python dashboard `dashboard.py` visualizes crime patterns derived from the processed dataset.

---

# Data Lake Design
The AWS S3 bucket follows a **layered data lake architecture** commonly used in modern data engineering pipelines.
```
s3://chicago-crime-data/

├── raw/
│ └── chicago_crime_api_data.json
│
├── processed/
│ └── cleaned_crime_data.parquet
│
└── analytics/
  └── aggregated_crime_metrics.parquet 
```

### Raw Layer
Stores unprocessed data fetched directly from the API.

### Processed Layer
Contains cleaned and structured datasets after Spark transformations.

### Analytics Layer
Contains aggregated datasets used for reporting and dashboard analysis.

---

# Pipeline Execution
The pipeline execution is orchestrated through `main.py`

---

# Installation
- Clone the repository: https://github.com/Shilpa-31/ChicagoCrimeDataAnalysis_Spark
- Navigate to the project directory: cd ChicagoCrimeDataAnalysis_Spark
- Install dependencies: pip install -r `requirements.txt`

---

# Future Improvements
Potential enhancements include:
- Implement **Spark Structured Streaming** for real-time crime ingestion
- Introduce workflow orchestration using **Apache Airflow or Dagster**
- Implement **partitioned data storage in S3**
- Add **geospatial crime hotspot analysis**
- Deploy the pipeline on a **Spark cluster (EMR / Databricks)**
