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

![Architecture Diagram](https://github.com/pranavbawa8/weather_data_pipeline/blob/main/weather_data_pipeline/Images/architecure_diagram.png)

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


## **Getting Started**

### **Prerequisites**
To set up and run this pipeline, you need:
- An **AWS Account** with access to **S3, Glue, Redshift, and IAM**.
- **Apache Airflow** installed (or use AWS Managed Workflows for Apache Airflow).
- **Python 3.x** and the required libraries installed.

---

### **Setup Instructions**

#### **1. Clone the Repository**
First, clone this repository to your local environment:
git clone https://github.com/pranavbawa8/weather_data_pipeline.git

cd data-pipeline

#### **2. Upload Raw Data to S3**
Before running the pipeline, you need to upload your raw dataset to the S3 bucket:

aws s3 cp weather_data_raw.csv s3://raw-bucket/new-data/

Ensure that:
Your AWS CLI is configured with appropriate credentials.

The bucket exists and is accessible.

**3. Configure AWS Glue Crawler**
Open the AWS Glue Console.

Create a Glue Crawler to scan the raw data in s3://raw-bucket/new-data/.

Set it to update the Glue Data Catalog.

**4. Configure AWS Glue Job**
In AWS Glue, create a new ETL Job.

Use the provided script: glue_jobs/glue_etl_job.py.

Configure it to process data and write output to s3://processed-bucket/processed-data/.


**5. Set Up Amazon Redshift**
Create a Redshift Cluster (or use an existing one).

Create a Table in Redshift with a schema matching your processed data.

**Load Data from S3 into Redshift:**

COPY public.weather_data

FROM 's3://processed-bucket/processed-data/'

IAM_ROLE 'arn:aws:iam::your-account-id:role/RedshiftRole'

FORMAT AS PARQUET;

Ensure that IAM roles and S3 permissions are set up correctly.

**6. Configure Apache Airflow**
Install Airflow locally or use AWS Managed Workflows for Apache Airflow.

Add AWS and Redshift connections in Airflow UI.

Copy the DAG script airflow/dags/data_pipeline_dag.py into your Airflow DAGs folder.

**7. Run the Pipeline**
Trigger the Airflow DAG to execute the full pipeline:

airflow dags trigger data_pipeline_dag

Monitor the pipeline execution using Airflow UI.

**Project Structure**

weather_data-pipeline/

│── airflow/

│   ├── dags/

│   │   ├── data_pipeline_dag.py       # Airflow DAG for orchestration

│── glue_jobs/

│   ├── glue_etl_job.py                # AWS Glue ETL job script

│── images/

│   ├── architecture_diagram.png        # Architecture visualization

│── README.md


**Contributing**
Contributions are welcome! Feel free to open an issue or submit a pull request.

Contact
For inquiries, reach out at:
📧 Email: pranav.bawa08@gmail.com
🔗 LinkedIn: https://www.linkedin.com/in/pranavbawa/
