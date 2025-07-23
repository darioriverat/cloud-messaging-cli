# Google BigQuery CLI

A command-line tool for managing Google BigQuery datasets and tables.

## Configuration

The following environment variables are required to connect with the BigQuery service:

```
GCP_PROJECT_ID=your-project-id
GCP_SERVICE_ACCOUNT_PATH=path/to/your/service-account.json
```

## Usage

### Dataset Management

**Create a dataset:**
```bash
python bigquery.py --create-dataset my-dataset-name
```

## Command Reference

| Command | Description | Example |
|---------|-------------|---------|
| `--create-dataset <name>` | Create a new dataset | `python bigquery.py --create-dataset my-dataset` |

## Common BigQuery Locations

Here are some commonly used BigQuery locations for dataset creation:

- `US` (United States)
- `EU` (European Union)
- `asia-northeast1` (Tokyo)
- `asia-southeast1` (Singapore)
- `australia-southeast1` (Sydney)
- `europe-west1` (Belgium)
- `europe-west2` (London)
- `us-central1` (Iowa)
- `us-east1` (South Carolina)
- `us-west1` (Oregon)

## Notes

- Dataset names must be unique within your project
- Dataset names can only contain letters, numbers, and underscores
- Dataset names must start with a letter or underscore
- If no location is specified, the dataset will be created in the default location (usually `US`)
- Make sure your service account has the necessary BigQuery permissions
- Dataset creation is an idempotent operation - if the dataset already exists, the command will succeed
- Datasets are containers for tables and views in BigQuery
- Each dataset belongs to a specific project and location