# End-to-End Data Pipeline with AWS Glue, Redshift, Apache Airflow, and Glue Crawler

This project demonstrates a **scalable data pipeline** that:
1. Ingests raw data from S3.
2. Infers schema and creates metadata using AWS Glue Crawler.
3. Processes the data using AWS Glue.
4. Loads the processed data into Amazon Redshift.
5. Archives raw and processed data.
6. Orchestrates the workflow using Apache Airflow.

---

## **Architecture Overview**

![Architecture Diagram](weather_data_pipeline/images/AWS_ETL_PIPELINE.png)

1. **Raw Data Ingestion**:
   - Raw data is stored in an S3 bucket (`s3://raw-bucket/new-data/`).

2. **Schema Inference and Metadata Creation**:
   - AWS Glue Crawler scans the raw data and creates metadata in the Glue Data Catalog.

3. **Data Processing**:
   - AWS Glue processes the raw data, cleans it, and writes the processed data to another S3 bucket (`s3://processed-bucket/processed-data/`).

4. **Data Loading**:
   - The processed data is loaded into Amazon Redshift for analytics.

5. **Data Archiving**:
   - Raw and processed data are moved to archive folders in their respective S3 buckets after processing.

6. **Orchestration**:
   - Apache Airflow orchestrates the entire pipeline, including:
     - Running the Glue Crawler.
     - Triggering the Glue Job.
     - Loading data into Redshift.
     - Archiving raw and processed data.
