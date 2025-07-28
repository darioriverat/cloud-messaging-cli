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

### Docker Image Tagging

**Tag a local Docker image for registry submission:**
```bash
./artifacts.sh tag-docker-image --local-image myapp:latest --remote-image myapp:v1.0.0 --repository my-repo --location us-east1
```

### Docker Image Pushing

**Push Docker image to registry:**
```bash
./artifacts.sh push-docker-image myapp:v1.0.0 --repository my-repo --location us-central1
```

**Complete workflow example:**
```bash
# 1. Create a repository
./artifacts.sh create-docker-repository my-app-repo --location us-central1

# 2. Build your Docker image locally
docker build -t myapp:latest .

# 3. Tag the image for the registry
./artifacts.sh tag-docker-image --local-image myapp:latest --remote-image myapp:v1.0.0 --repository my-app-repo

# 4. Push to the registry
./artifacts.sh push-docker-image myapp:v1.0.0 --repository my-app-repo --location us-central1
```

## Command Reference

| Command | Description | Example |
|---------|-------------|---------|
| `create-docker-repository <NAME> --location <LOCATION>` | Create a new Docker repository | `./artifacts.sh create-docker-repository my-repo --location us-central1` |
| `tag-docker-image --local-image <LOCAL_IMAGE> --remote-image <REMOTE_IMAGE> --repository <REPOSITORY> [--location <LOCATION>]` | Tag local Docker image for registry submission | `./artifacts.sh tag-docker-image --local-image myapp:latest --remote-image myapp:v1.0.0 --repository my-repo` |
| `push-docker-image <IMAGE_NAME> --repository <REPOSITORY> --location <LOCATION>` | Push Docker image to registry | `./artifacts.sh push-docker-image myapp:v1.0.0 --repository my-repo --location us-central1` |
| `help` or `--help` or `-h` | Show help information | `./artifacts.sh help` |

### Tag Docker Image Options

| Option | Required | Description | Default |
|--------|----------|-------------|---------|
| `--local-image` | Yes | Local Docker image name (e.g., `myapp:latest`) | - |
| `--remote-image` | Yes | Remote image name for registry (e.g., `myapp:v1.0.0`) | - |
| `--repository` | Yes | Repository name | - |
| `--location` | Yes | GCP region (e.g., `us-central1`, `us-east1`) | `us-central1` |

### Push Docker Image Options

| Option | Required | Description | Default |
|--------|----------|-------------|---------|
| `<IMAGE_NAME>` | Yes | Docker image name to push (e.g., `myapp:v1.0.0`) | - |
| `--repository` | Yes | Repository name | - |
| `--location` | Yes | GCP region (e.g., `us-central1`, `us-east1`) | - |

## Notes

- **Project Configuration**: The script automatically sets the GCP project using `gcloud config set core/project` if `GCP_PROJECT_ID` is provided
- **Location Requirement**: The `--location` parameter is required for creating repositories and pushing images, optional for tagging (defaults to `us-central1`)
- **Repository Format**: Currently supports Docker format repositories
- **Image Tagging**: The `tag-docker-image` command automatically constructs the full remote image name using the format: `{location}-docker.pkg.dev/{project-id}/{repository}/{remote-image}`
- **Image Pushing**: The `push-docker-image` command requires the location to construct the registry URL
- **Common GCP Regions**: Available regions include:
  - `us-central1` (default)
  - `us-east1`
  - `europe-west1`
  - `asia-southeast1`
- **Permanent Actions**: Creating repositories is a permanent action that will be billed according to your GCP pricing
- **Permissions**: Ensure your service account has the necessary Artifact Registry permissions
