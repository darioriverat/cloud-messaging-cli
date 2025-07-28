# Google Artifact Registry CLI

A command-line tool for managing Google Artifact Registry repositories as part of the GCP CLI Toolkit.

## Configuration

The following environment variables are required to connect with the Artifact Registry service:

```
GCP_PROJECT_ID=your-project-id
```

You can set these variables in a `.env` file in the project root:

```bash
# .env file
GCP_PROJECT_ID=your-gcp-project-id
```

## Usage

### Repository Management

**Create a Docker repository:**
```bash
./artifacts.sh create-docker-repository my-repo --location us-central1
```

## Command Reference

| Command | Description | Example |
|---------|-------------|---------|
| `create-docker-repository <NAME> --location <LOCATION>` | Create a new Docker repository | `./artifacts.sh create-docker-repository my-repo --location us-central1` |
| `help` or `--help` or `-h` | Show help information | `./artifacts.sh help` |


## Notes

- **Project Configuration**: The script automatically sets the GCP project using `gcloud config set core/project` if `GCP_PROJECT_ID` is provided
- **Location Requirement**: The `--location` parameter is required for creating Artifact Registry repositories
- **Repository Format**: Currently supports Docker format repositories
- **Permanent Actions**: Creating repositories is a permanent action that will be billed according to your GCP pricing
- **Permissions**: Ensure your service account has the necessary Artifact Registry permissions
