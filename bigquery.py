import os
from google.cloud import bigquery
from dotenv import load_dotenv
import argparse

os.environ.clear()
load_dotenv()

# Set up argument parser
parser = argparse.ArgumentParser(description='Argument parser for big query.')
parser.add_argument('--create-dataset', type=str, help='Name of the dataset to create')
parser.add_argument('--create-table', nargs=2, metavar=('DATASET_NAME', 'TABLE_NAME'), help='Name of the table to create')

project_id = os.getenv("GCP_PROJECT_ID")
service_account_file = os.getenv("GCP_SERVICE_ACCOUNT_PATH")

args = parser.parse_args()

# check for arg create_dataset
if args.create_dataset:
    dataset_name = args.create_dataset

    print(f"Creating dataset: {dataset_name}")

    bigquery_client = bigquery.Client.from_service_account_json(service_account_file)

    dataset_id = f"{bigquery_client.project}.{dataset_name}"
    dataset = bigquery.Dataset(dataset_id)
    bigquery_client.create_dataset(dataset)

    print(f"Dataset {dataset_name} created")

# check for arg create_table
elif args.create_table:
    dataset_name, table_name = args.create_table

    print(f"Creating table: {table_name} in dataset: {dataset_name}")

    bigquery_client = bigquery.Client.from_service_account_json(service_account_file)

    table_id = f"{bigquery_client.project}.{dataset_name}.{table_name}"

    table = bigquery.Table(table_id)
    table = bigquery_client.create_table(table)

    print(f"Table {table_name} created in dataset {dataset_name}")

else:
    print(parser.format_help())
