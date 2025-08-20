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
```

## Available Tools

- 📖 **[Pub/Sub](docs/pubsub.md)**
- 📖 **[Cloud Storage](docs/cloud-storage.md)**
- 📖 **[BigQuery](docs/bigquery.md)**
- 📖 **[Artifact Registry](docs/artifacts.md)**

## Notes

- All tools require proper GCP service account configuration
- Make sure your service account has the necessary permissions for the services you want to use
- Currently supports Google Cloud Pub/Sub, Cloud Storage, BigQuery, and Artifact Registry
- Extensible architecture allows easy addition of new GCP services
- Comprehensive examples and documentation for each service
