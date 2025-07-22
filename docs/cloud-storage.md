# Google Cloud Storage CLI

A command-line tool for managing Google Cloud Storage buckets.

## Configuration

The following environment variables are required to connect with the Cloud Storage service:

```
GCP_PROJECT_ID=your-project-id
GCP_SERVICE_ACCOUNT_PATH=path/to/your/service-account.json
```

## Usage

### Bucket Management

**Create a bucket in the default location:**
```bash
python cloud-storage.py --create-bucket my-bucket-name
```

**Create a bucket in a specific region:**
```bash
python cloud-storage.py --create-bucket my-bucket-name --region us-central1
```

## Command Reference

| Command | Description | Example |
|---------|-------------|---------|
| `--create-bucket <name>` | Create a new bucket | `python cloud-storage.py --create-bucket my-bucket` |
| `--region <region>` | Specify the region for bucket creation | `python cloud-storage.py --create-bucket my-bucket --region us-central1` |

## Common GCP Regions

Here are some commonly used GCP regions for bucket creation:

- `us-central1` (Iowa)
- `us-east1` (South Carolina)
- `us-west1` (Oregon)
- `us-west2` (Los Angeles)
- `europe-west1` (Belgium)
- `europe-west2` (London)
- `asia-east1` (Taiwan)
- `asia-southeast1` (Singapore)
- `australia-southeast1` (Sydney)

## Notes

- Bucket names must be globally unique across all of Google Cloud Storage
- Bucket names can only contain lowercase letters, numbers, hyphens, and underscores
- Bucket names must start and end with a letter or number
- If no region is specified, the bucket will be created in the default location (usually `us-central1`)
- Make sure your service account has the necessary Storage permissions
- Bucket creation is an idempotent operation - if the bucket already exists, the command will succeed