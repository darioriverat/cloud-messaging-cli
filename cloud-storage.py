import os
from google.cloud import storage
from dotenv import load_dotenv
import argparse
from tabulate import tabulate

os.environ.clear()
load_dotenv()

# Set up argument parser
parser = argparse.ArgumentParser(description='Argument parser for cloud storage.')
parser.add_argument('--create-bucket', type=str, help='Name of the bucket to create')
parser.add_argument('--list-buckets', action='store_true', help='List all buckets in the project')
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

# check for arg list_buckets
elif args.list_buckets:
    print("Listing all buckets...")

    storage_client = storage.Client.from_service_account_json(service_account_file)

    # List all buckets in the project
    buckets = list(storage_client.list_buckets())

    if buckets:
        print(f"Found {len(buckets)} bucket(s):")

        # Prepare data for table
        table_data = []
        for bucket in buckets:
            table_data.append([
                bucket.name,
                bucket.location or "N/A",
                bucket.location_type or "N/A"
            ])

        # Create table with headers
        headers = ["Bucket Name", "Location", "Location Type"]
        table = tabulate(table_data, headers=headers, tablefmt="pretty", colalign=("left", "left", "left"))
        print(table)
    else:
        print("No buckets found in the project.")

else:
    print("No action specified. Use --create-bucket <bucket_name> [--region <region>] to create a bucket, or --list-buckets to list all buckets.")