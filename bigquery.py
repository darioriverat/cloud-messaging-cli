import os
from google.cloud import bigquery
from dotenv import load_dotenv
import argparse

os.environ.clear()
load_dotenv()

# Set up argument parser
parser = argparse.ArgumentParser(description='Argument parser for big query.')
parser.add_argument('--create-dataset', type=str, help='Name of the dataset to create')

project_id = os.getenv("GCP_PROJECT_ID")
service_account_file = os.getenv("GCP_SERVICE_ACCOUNT_PATH")

args = parser.parse_args()

# check for arg create_dataset
if args.create_dataset:
    dataset_name = args.create_dataset

    print(f"Creating dataset: {dataset_name}")

    bigquery_client = bigquery.Client.from_service_account_json(service_account_file)

    dataset = bigquery_client.create_dataset(dataset_name)

    print(f"Dataset {dataset_name} created")

else:
    print(parser.format_help())
