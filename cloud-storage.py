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
parser.add_argument('--upload-file', nargs=2, metavar=('BUCKET_NAME', 'FILE_PATH'), help='Upload a file to a bucket')
parser.add_argument('--download-file', nargs='+', metavar='ARG', help='Download a file from a bucket: <bucket_name> <file_path> [destination_path]')
parser.add_argument('--delete-file', nargs=2, metavar=('BUCKET_NAME', 'FILE_PATH'), help='Delete a file from a bucket')

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

# check for arg upload_file
elif args.upload_file:
    bucket_name, file_path = args.upload_file

    print(f"Uploading file: {file_path} to bucket: {bucket_name}")

    storage_client = storage.Client.from_service_account_json(service_account_file)

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_path)
    blob.upload_from_filename(file_path)

    print(f"File {file_path} uploaded to bucket {bucket_name}")

# check for arg download_file
elif args.download_file:
    if len(args.download_file) < 2:
        print("Error: --download-file requires at least bucket name and file path.")
        print("Usage: --download-file <bucket_name> <file_path> [destination_path]")
        exit(1)

    bucket_name = args.download_file[0]
    file_path = args.download_file[1]

    # Check if destination path is provided
    if len(args.download_file) > 2:
        destination_path = args.download_file[2]
        print(f"Downloading file: {file_path} from bucket: {bucket_name}")
        print(f"Destination: {destination_path}")
    else:
        destination_path = file_path
        print(f"Downloading file: {file_path} from bucket: {bucket_name}")

    storage_client = storage.Client.from_service_account_json(service_account_file)

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_path)
    blob.download_to_filename(destination_path)

    print(f"File downloaded to: {destination_path}")

# check for arg delete_file
elif args.delete_file:
    bucket_name, file_path = args.delete_file

    print(f"Deleting file: {file_path} from bucket: {bucket_name}")

    storage_client = storage.Client.from_service_account_json(service_account_file)

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_path)
    blob.delete()

    print(f"File {file_path} deleted from bucket {bucket_name}")

else:
    print(parser.format_help())
