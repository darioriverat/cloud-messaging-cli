# GCP CLI Toolkit

A comprehensive command-line toolkit for managing Google Cloud Platform services including Google Cloud Pub/Sub, BigQuery, Cloud Storage, and more.

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd gcp-cli-toolkit
```

2. Create and activate a virtual environment:
```bash
uv venv
source .venv/bin/activate
```

3. Install dependencies:
```bash
uv pip install -e .
```

## Configuration

The following environment variables are required to connect with GCP services:

```
GCP_PROJECT_ID=your-project-id
GCP_SERVICE_ACCOUNT_PATH=path/to/your/service-account.json
```

### GCP Service Account Setup

1. Once you're logged into GCP, go to **IAM & Admin > Service Accounts**.
2. Click **"Create Service Account"**.
3. Enter a name for the service account and click **"Create and Continue"**.
4. In the **Permissions** step, assign the appropriate roles:
   - For Pub/Sub: Select **"Pub/Sub Admin"**
   - For Cloud Storage: Select **"Storage Admin"** or **"Storage Object Admin"**
   - Click **"Continue"**, then **"Done"**.

#### Creating a Service Account Key (JSON):

1. After the service account is created, click the **three vertical dots** next to it and select **"Manage Keys"**.
2. Click **"Add Key"** and choose **"Create new key"**.
3. Select **JSON** as the key type and click **"Create"**.

The key file will be downloaded to your computer. Store it securely, as it contains credentials for accessing your GCP services.

## CLI Interfaces

The toolkit provides two unified CLI interfaces for easy access to all tools:

### Python Scripts Interface (`gcpcli.py`)

For Python-based tools (Pub/Sub, BigQuery, Cloud Storage):

```bash
# Using python command
python gcpcli.py <script_name> [args...]

# Using executable directly
./gcpcli.py <script_name> [args...]
```

### Shell Scripts Interface (`gcpcli.sh`)

For shell-based tools (Artifact Registry):

```bash
# Shell scripts
./gcpcli.sh <script_name> [args...]

# Python scripts (with --python flag)
./gcpcli.sh --python <script_name> [args...]
```

## Available Tools

### [Pub/Sub CLI](docs/pubsub.md)

Manage Google Cloud Pub/Sub topics, subscriptions, and messages.

**Quick Start:**
```bash
# List all topics
./gcpcli.py pubsub --list-topics

# Create a topic
./gcpcli.py pubsub --create-topic mytopic

# Create a subscription
./gcpcli.py pubsub --subscribe mytopic subscription-name

# Publish a message
./gcpcli.py pubsub --publish mytopic "Hello World"

# Receive messages
./gcpcli.py pubsub --receive subscription-name

# Delete a subscription
./gcpcli.py pubsub --delete-subscription subscription-name

# Delete a topic (⚠️ permanent)
./gcpcli.py pubsub --delete-topic mytopic
```

📖 **[Full Pub/Sub Documentation](docs/pubsub.md)**

### [Cloud Storage CLI](docs/cloud-storage.md)

Manage Google Cloud Storage buckets.

**Quick Start:**
```bash
# List all buckets
./gcpcli.py cloud-storage --list-buckets

# Create a bucket in default location
./gcpcli.py cloud-storage --create-bucket my-bucket-name

# Create a bucket in specific region
./gcpcli.py cloud-storage --create-bucket my-bucket-name --region us-central1

# Upload a file to a bucket
./gcpcli.py cloud-storage --upload-file my-bucket-name file.txt

# Download a file from a bucket
./gcpcli.py cloud-storage --download-file my-bucket-name file.txt

# Download a file to a specific destination
./gcpcli.py cloud-storage --download-file my-bucket-name file.txt ./downloaded-file.txt

# Delete a file from a bucket
./gcpcli.py cloud-storage --delete-file my-bucket-name file.txt

# Delete a bucket (⚠️ permanent)
./gcpcli.py cloud-storage --delete-bucket my-bucket-name

# Force delete bucket with all contents (⚠️ permanent)
./gcpcli.py cloud-storage --delete-bucket my-bucket-name --force
```

📖 **[Full Cloud Storage Documentation](docs/cloud-storage.md)**

### [BigQuery CLI](docs/bigquery.md)

Manage Google BigQuery datasets and tables.

**Quick Start:**
```bash
# Create a dataset
./gcpcli.py bigquery --create-dataset my-dataset-name

# Delete a dataset (⚠️ permanent)
./gcpcli.py bigquery --delete-dataset my-dataset-name

# Delete a dataset with force (deletes all tables first)
./gcpcli.py bigquery --delete-dataset my-dataset-name --force

# Create a table in a dataset
./gcpcli.py bigquery --create-table my-dataset-name my-table-name

# Create a table with schema
./gcpcli.py bigquery --create-table my-dataset-name my-table-name --json-schema examples/bigquery/schema_example.json

# Update a table's schema
./gcpcli.py bigquery --update-table my-dataset-name my-table-name --json-schema examples/bigquery/schema_example.json

# Delete a table (⚠️ permanent)
./gcpcli.py bigquery --delete-table my-dataset-name my-table-name

# Load CSV data into a table
./gcpcli.py bigquery --load-csv my-dataset-name my-table-name data.csv

# Load CSV with custom delimiter
./gcpcli.py bigquery --load-csv my-dataset-name my-table-name data.csv --delimiter ";"

# Execute a query from command line
./gcpcli.py bigquery --query "SELECT * FROM my-dataset-name.my-table-name LIMIT 10"

# Execute a query from a file
./gcpcli.py bigquery --query-file query.sql
```

📖 **[Full BigQuery Documentation](docs/bigquery.md)**

### [Artifact Registry CLI](docs/artifacts.md)

Manage Google Artifact Registry repositories.

**Quick Start:**
```bash
# Configure Docker authentication (for pushing images)
./gcpcli.sh artifacts auth-docker-location us-central1

# Create a Docker repository
./gcpcli.sh artifacts create-docker-repository my-repo --location us-central1

# Tag a local Docker image for registry submission
./gcpcli.sh artifacts tag-docker-image --local-image myapp:latest --remote-image myapp:v1.0.0 --repository my-repo --location us-east1

# Push Docker image to registry
./gcpcli.sh artifacts push-docker-image myapp:v1.0.0 --repository my-repo --location us-central1
```

📖 **[Full Artifact Registry Documentation](docs/artifacts.md)**

## Features

- **Unified CLI Interface**: Two clean interfaces for Python and shell scripts
- **Pub/Sub Management**: Create topics, subscriptions, publish and receive messages
- **Message Ordering**: Support for ordered message delivery with ordering keys
- **Cloud Storage**: Create buckets with region specification, upload/download files
- **BigQuery**: Create datasets and tables with complex nested schemas
- **Artifact Registry**: Create Docker repositories with location specification
- **Simple CLI Interface**: Easy-to-use command-line tools
- **Comprehensive Documentation**: Detailed guides for each service
- **Extensible Architecture**: Easy to add new GCP services

## Notes

- All tools require proper GCP service account configuration
- Make sure your service account has the necessary permissions for the services you want to use
- Currently supports Google Cloud Pub/Sub, Cloud Storage, BigQuery, and Artifact Registry
- Extensible architecture allows easy addition of new GCP services
- Comprehensive examples and documentation for each service
