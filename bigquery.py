import os
from google.cloud import bigquery
from dotenv import load_dotenv
import argparse
import json

os.environ.clear()
load_dotenv()

def create_schema_field(field_data):
    """Recursively create SchemaField objects, handling nested RECORD fields."""
    if field_data['field_type'] == 'RECORD' and 'fields' in field_data:
        # Handle nested RECORD fields
        nested_fields = []
        for nested_field in field_data['fields']:
            nested_fields.append(create_schema_field(nested_field))

        return bigquery.SchemaField(
            field_data['name'],
            field_data['field_type'],
            mode=field_data.get('mode', 'NULLABLE'),
            fields=nested_fields
        )
    else:
        # Handle simple fields
        return bigquery.SchemaField(
            field_data['name'],
            field_data['field_type'],
            mode=field_data.get('mode', 'NULLABLE')
        )

# Set up argument parser
parser = argparse.ArgumentParser(description='Argument parser for big query.')
parser.add_argument('--create-dataset', type=str, help='Name of the dataset to create')
parser.add_argument('--delete-dataset', type=str, help='Name of the dataset to delete')
parser.add_argument('--create-table', nargs=2, metavar=('DATASET_NAME', 'TABLE_NAME'), help='Name of the table to create')
parser.add_argument('--delete-table', nargs=2, metavar=('DATASET_NAME', 'TABLE_NAME'), help='Name of the table to delete')
parser.add_argument('--update-table', nargs=2, metavar=('DATASET_NAME', 'TABLE_NAME'), help='Name of the table to update')
parser.add_argument('--load-csv', nargs=3, metavar=('DATASET_NAME', 'TABLE_NAME', 'CSV_FILE_PATH'), help='Name of the table to load from a csv file')

# optional arguments
parser.add_argument('--json-schema', type=str, help='JSON schema string for the table')
parser.add_argument('--force', action='store_true', help='Force the operation to run without confirmation')

project_id = os.getenv("GCP_PROJECT_ID")
service_account_file = os.getenv("GCP_SERVICE_ACCOUNT_PATH")

args = parser.parse_args()

# check for arg json_schema
json_schema = args.json_schema

# check for arg create_dataset
if args.create_dataset:
    dataset_name = args.create_dataset

    print(f"Creating dataset: {dataset_name}")

    bigquery_client = bigquery.Client.from_service_account_json(service_account_file)

    dataset_id = f"{project_id}.{dataset_name}"
    dataset = bigquery.Dataset(dataset_id)
    bigquery_client.create_dataset(dataset)

    print(f"Dataset {dataset_name} created")

# check for arg delete_dataset
elif args.delete_dataset:
    dataset_name = args.delete_dataset

    print(f"Deleting dataset: {dataset_name}")

    bigquery_client = bigquery.Client.from_service_account_json(service_account_file)

    dataset_id = f"{project_id}.{dataset_name}"

    if args.force:
        bigquery_client.delete_dataset(dataset_id, delete_contents=True)
    else:
        bigquery_client.delete_dataset(dataset_id)

    print(f"Dataset {dataset_name} deleted")

# check for arg delete_table
elif args.delete_table:
    dataset_name, table_name = args.delete_table

    print(f"Deleting table: {table_name} in dataset: {dataset_name}")

    bigquery_client = bigquery.Client.from_service_account_json(service_account_file)

    table_id = f"{project_id}.{dataset_name}.{table_name}"
    bigquery_client.delete_table(table_id)

    print(f"Table {table_name} deleted from dataset {dataset_name}")

# check for arg create_table
elif args.create_table:
    dataset_name, table_name = args.create_table

    if json_schema:
        print(f"Using json schema: {json_schema}")
        with open(json_schema, 'r') as file:
            json_schema_file = file.read()

        # validate json_schema is a valid json
        try:
            json_schema_object = json.loads(json_schema_file)
        except json.JSONDecodeError:
            print("Error: --json-schema is not a valid json")
            exit(1)

        # Create schema fields using the recursive function
        schema_fields = []
        for field in json_schema_object['schema_fields']:
            schema_fields.append(create_schema_field(field))

    print(f"Creating table: {table_name} in dataset: {dataset_name}")

    bigquery_client = bigquery.Client.from_service_account_json(service_account_file)

    table_id = f"{project_id}.{dataset_name}.{table_name}"

    if (json_schema):
        table = bigquery.Table(table_id, schema_fields)
        table.schema = schema_fields
    else:
        table = bigquery.Table(table_id)

    table = bigquery_client.create_table(table)

    print(f"Table {table_name} created in dataset {dataset_name}")

# check for arg update_table
elif args.update_table:
    dataset_name, table_name = args.update_table

    if (not json_schema):
        print("Error: --json-schema is required for --update-table")
        exit(1)

    print(f"Updating table: {table_name} in dataset: {dataset_name}")

    bigquery_client = bigquery.Client.from_service_account_json(service_account_file)
    data_set = bigquery_client.dataset(dataset_name)
    table = data_set.table(table_name)

    # get contents from json_schema
    with open(json_schema, 'r') as file:
        json_schema_file = file.read()

    # validate json_schema is a valid json
    try:
        json_schema_object = json.loads(json_schema_file)
    except json.JSONDecodeError:
        print("Error: --json-schema is not a valid json")
        exit(1)

    # Create schema fields using the recursive function
    schema_fields = []
    for field in json_schema_object['schema_fields']:
        schema_fields.append(create_schema_field(field))

    # create a Table object from the json_schema
    table = bigquery.Table(table, schema_fields)
    table.schema = schema_fields

    # get field names from schema_fields
    fields = [field.name for field in schema_fields]

    # update the table
    bigquery_client.update_table(table, ["schema"])

    print(f"Table {table_name} updated in dataset {dataset_name}")

# check for arg load_csv
elif args.load_csv:
    dataset_name, table_name, csv_file_path = args.load_csv

    print(f"Loading csv file: {csv_file_path} into table: {table_name} in dataset: {dataset_name}")

    bigquery_client = bigquery.Client.from_service_account_json(service_account_file)

    table_id = f"{project_id}.{dataset_name}.{table_name}"

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
    )

    with open(csv_file_path, 'rb') as source_file:
        job = bigquery_client.load_table_from_file(source_file, table_id, job_config=job_config)

    job.result()

    print(f"CSV file {csv_file_path} loaded into table {table_name} in dataset {dataset_name}")

else:
    print(parser.format_help())
