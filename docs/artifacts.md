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

### Docker Authentication

**Configure Docker authentication for a location:**
```bash
./gcpcli.sh artifacts auth-docker-location us-central1
```

### Repository Management

**Create a Docker repository:**
```bash
./gcpcli.sh artifacts create-docker-repository my-repo --location us-central1
```

### Docker Image Operations

**Tag a local Docker image for registry submission:**
```bash
./gcpcli.sh artifacts tag-docker-image --local-image myapp:latest --remote-image myapp:v1.0.0 --repository my-repo --location us-east1
```

**Push Docker image to registry:**
```bash
./gcpcli.sh artifacts push-docker-image myapp:v1.0.0 --repository my-repo --location us-central1
```

**List Docker images in a repository:**
```bash
./gcpcli.sh artifacts list-docker-images --repository my-repo --location us-central1
```

**List repositories in project:**
```bash
./gcpcli.sh artifacts list-repositories
./gcpcli.sh artifacts list-repositories --location us-central1
```

### Docker Configuration

**Display Docker configuration:**
```bash
./gcpcli.sh artifacts docker config
```

### Google Cloud Authentication

**Login to Google Cloud:**
```bash
./gcpcli.sh artifacts gcloud-auth-login
```

**Logout from current account:**
```bash
./gcpcli.sh artifacts gcloud-auth-logout
```

**Check authentication status:**
```bash
./gcpcli.sh artifacts gcloud-auth-status
```

**Complete workflow example:**
```bash
# 1. Configure Docker authentication
./gcpcli.sh artifacts auth-docker-location us-central1

# 2. Create a repository
./gcpcli.sh artifacts create-docker-repository my-app-repo --location us-central1

# 3. Build your Docker image locally
docker build -t myapp:latest .

# 4. Tag the image for the registry
./gcpcli.sh artifacts tag-docker-image --local-image myapp:latest --remote-image myapp:v1.0.0 --repository my-app-repo

# 5. Push to the registry
./gcpcli.sh artifacts push-docker-image myapp:v1.0.0 --repository my-app-repo --location us-central1

# 6. List images in the repository
./gcpcli.sh artifacts list-docker-images --repository my-app-repo --location us-central1

# 7. List all repositories in project
./gcpcli.sh artifacts list-repositories

# 8. Check Docker configuration
./gcpcli.sh artifacts docker config

# 9. Check authentication status
./gcpcli.sh artifacts gcloud-auth-status
```

## Command Reference

| Command | Description | Example |
|---------|-------------|---------|
| `auth-docker-location <LOCATION>` | Configure Docker authentication for the specified location | `./gcpcli.sh artifacts auth-docker-location us-central1` |
| `create-docker-repository <NAME> --location <LOCATION>` | Create a new Docker repository | `./gcpcli.sh artifacts create-docker-repository my-repo --location us-central1` |
| `tag-docker-image --local-image <LOCAL_IMAGE> --remote-image <REMOTE_IMAGE> --repository <REPOSITORY> [--location <LOCATION>]` | Tag local Docker image for registry submission | `./gcpcli.sh artifacts tag-docker-image --local-image myapp:latest --remote-image myapp:v1.0.0 --repository my-repo` |
| `push-docker-image <IMAGE_NAME> --repository <REPOSITORY> --location <LOCATION>` | Push Docker image to registry | `./gcpcli.sh artifacts push-docker-image myapp:v1.0.0 --repository my-repo --location us-central1` |
| `list-docker-images --repository <REPOSITORY> --location <LOCATION>` | List Docker images in repository | `./gcpcli.sh artifacts list-docker-images --repository my-repo --location us-central1` |
| `list-repositories [--location <LOCATION>]` | List repositories in project | `./gcpcli.sh artifacts list-repositories` |
| `gcloud-auth-login` | Authenticate with Google Cloud | `./gcpcli.sh artifacts gcloud-auth-login` |
| `gcloud-auth-logout` | Logout from current account | `./gcpcli.sh artifacts gcloud-auth-logout` |
| `gcloud-auth-status` | Check current authentication status | `./gcpcli.sh artifacts gcloud-auth-status` |
| `docker config` | Display Docker configuration | `./gcpcli.sh artifacts docker config` |
| `help` or `--help` or `-h` | Show help information | `./gcpcli.sh artifacts help` |

### Auth Docker Location Options

| Option | Required | Description | Default |
|--------|----------|-------------|---------|
| `<LOCATION>` | Yes | GCP region (e.g., `us-central1`, `us-east1`) | - |

### Tag Docker Image Options

| Option | Required | Description | Default |
|--------|----------|-------------|---------|
| `--local-image` | Yes | Local Docker image name (e.g., `myapp:latest`) | - |
| `--remote-image` | Yes | Remote image name for registry (e.g., `myapp:v1.0.0`) | - |
| `--repository` | Yes | Repository name | - |
| `--location` | No | GCP region (e.g., `us-central1`, `us-east1`) | `us-central1` |

### Push Docker Image Options

| Option | Required | Description | Default |
|--------|----------|-------------|---------|
| `<IMAGE_NAME>` | Yes | Docker image name to push (e.g., `myapp:v1.0.0`) | - |
| `--repository` | Yes | Repository name | - |
| `--location` | Yes | GCP region (e.g., `us-central1`, `us-east1`) | - |

### List Docker Images Options

| Option | Required | Description | Default |
|--------|----------|-------------|---------|
| `--repository` | Yes | Repository name | - |
| `--location` | Yes | GCP region (e.g., `us-central1`, `us-east1`) | - |

### List Repositories Options

| Option | Required | Description | Default |
|--------|----------|-------------|---------|
| `--location` | No | Filter repositories by location (e.g., `us-central1`, `us-east1`) | Lists all repositories |

### Google Cloud Authentication Options

| Command | Options | Description |
|---------|---------|-------------|
| `gcloud-auth-login` | None | No options required |
| `gcloud-auth-logout` | None | No options required (automatically logs out current account) |
| `gcloud-auth-status` | None | No options required |

### Docker Config Options

| Option | Required | Description | Default |
|--------|----------|-------------|---------|
| `config` | Yes | Subcommand to display Docker configuration | - |

## Notes

- **Project Configuration**: The script automatically checks and sets the GCP project using `gcloud config set core/project` if `GCP_PROJECT_ID` is provided. It will only update the project if it's different from the current setting or not set at all.
- **Docker Authentication**: The `auth-docker-location` command configures Docker to authenticate with Google Cloud Artifact Registry for the specified location
- **Location Requirement**: The `--location` parameter is required for creating repositories, pushing images, and listing images. It's optional for tagging (defaults to `us-central1`)
- **Repository Format**: Currently supports Docker format repositories
- **Image Tagging**: The `tag-docker-image` command automatically constructs the full remote image name using the format: `{location}-docker.pkg.dev/{project-id}/{repository}/{remote-image}`
- **Image Pushing**: The `push-docker-image` command requires the location to construct the registry URL
- **Image Listing**: The `list-docker-images` command uses `gcloud artifacts docker images list` to display all images in a repository
- **Repository Listing**: The `list-repositories` command uses `gcloud artifacts repositories list` to display all repositories in the project, with optional location filtering
- **Docker Configuration**: The `docker config` command displays the contents of `~/.docker/config.json` using `jq` for formatted output
- **Google Cloud Authentication**:
  - `gcloud-auth-login`: Authenticates with Google Cloud using `gcloud auth login`
  - `gcloud-auth-logout`: Automatically logs out the current account using `gcloud auth revoke`
  - `gcloud-auth-status`: Shows current account, project, and authentication status
- **Common GCP Regions**: Available regions include:
  - `us-central1` (default)
  - `us-east1`
  - `europe-west1`
  - `asia-southeast1`
- **Permanent Actions**: Creating repositories is a permanent action that will be billed according to your GCP pricing
- **Permissions**: Ensure your service account has the necessary Artifact Registry permissions
- **Dependencies**: The `docker config` command requires `jq` to be installed for JSON formatting
