import os
from google.cloud import storage
from dotenv import load_dotenv
import argparse

os.environ.clear()
load_dotenv()

# Set up argument parser
parser = argparse.ArgumentParser(description='Argument parser for cloud storage.')
parser.add_argument('--create-bucket', type=str, help='Name of the bucket to create')
parser.add_argument('--region', type=str, help='Region for the bucket (e.g., us-central1, europe-west1)')

project_id = os.getenv("GCP_PROJECT_ID")
service_account_file = os.getenv("GCP_SERVICE_ACCOUNT_PATH")

args = parser.parse_args()

# check for --region
region = args.region

# check for arg create_bucket
if args.create_bucket:
    bucket_name = args.create_bucket

    print(f"Creating bucket: {bucket_name}")
    if region:
        print(f"Region: {region}")

    storage_client = storage.Client.from_service_account_json(service_account_file)

    if region:
        # Create bucket with specific region
        bucket = storage_client.create_bucket(bucket_name, location=region)
        print(f"Bucket {bucket.name} created in region {region}")
    else:
        # Create bucket in default location
        bucket = storage_client.create_bucket(bucket_name)
        print(f"Bucket {bucket.name} created in default location")