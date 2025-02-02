import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

# Initialize Glue context
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)

# Get job parameters
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'input_bucket', 'output_bucket'])
job.init(args['JOB_NAME'], args)

# Read raw data from S3
input_path = f"s3://{args['input_bucket']}/new-data/raw_weather_data.csv"
raw_data = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={"paths": [input_path]},
    format="csv",
    format_options={"withHeader": True}
)

# Convert to Spark DataFrame for transformations
df = raw_data.toDF()

# Example transformations
# 1. Handle missing values
df = df.na.fill({"Temperature": 0, "Humidity": 0})

# 2. Convert temperature from Fahrenheit to Celsius
df = df.withColumn("Temperature", (df["Temperature"] - 32) * 5 / 9)

# 3. Filter out invalid rows
df = df.filter(df["Temperature"].isNotNull() & df["Humidity"].isNotNull())

# Save processed data to S3
output_path = f"s3://{args['output_bucket']}/processed-data/"
df.write.mode("overwrite").parquet(output_path)

# Commit the job
job.commit()