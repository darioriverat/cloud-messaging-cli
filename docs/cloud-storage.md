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

**List all buckets in the project:**
```bash
python cloud-storage.py --list-buckets
```

### File Operations

**Upload a file to a bucket:**
```bash
python cloud-storage.py --upload-file my-bucket-name /path/to/file.txt
```

**Upload a file with relative path:**
```bash
python cloud-storage.py --upload-file my-bucket-name ./file.txt
```

**Download a file from a bucket (preserves original path):**
```bash
python cloud-storage.py --download-file my-bucket-name /path/to/file.txt
```

**Download a file to a specific destination:**
```bash
python cloud-storage.py --download-file my-bucket-name /path/to/file.txt ./downloaded-file.txt
```

**Download a file to a different directory:**
```bash
python cloud-storage.py --download-file my-bucket-name file.txt /home/user/downloads/new-file.txt
```

**Delete a file from a bucket:**
```bash
python cloud-storage.py --delete-file my-bucket-name /path/to/file.txt
```

**Delete a file with relative path:**
```bash
python cloud-storage.py --delete-file my-bucket-name ./file.txt
```

> **Important Note**: When uploading files, GCP will create the underlying "path" structure in Cloud Storage based on the file path you provide. For example:
> - If you upload `~/hello.txt`, GCP will store it as `/Users/youruser/hello.txt`
> - If you upload `./file.txt`, GCP will store it as `./file.txt` using `./` as the folder name.
> - If you upload `/absolute/path/file.txt`, GCP will store it as `/absolute/path/file.txt`
>
> Consider using simple filenames or organizing your uploads with specific paths to avoid unexpected storage structures.
>
> **Download Note**: When downloading files, if no destination path is specified, the file will be downloaded with the same path structure as stored in Cloud Storage. Use the optional third parameter to specify a custom destination path.
>
> **Delete Note**: When deleting files, make sure to specify the exact path as stored in Cloud Storage. The deletion is permanent and cannot be undone.

## Command Reference

| Command | Description | Example |
|---------|-------------|---------|
| `--create-bucket <name>` | Create a new bucket | `python cloud-storage.py --create-bucket my-bucket` |
| `--list-buckets` | List all buckets in the project | `python cloud-storage.py --list-buckets` |
| `--upload-file <bucket> <file>` | Upload a file to a bucket | `python cloud-storage.py --upload-file my-bucket file.txt` |
| `--download-file <bucket> <file> [dest]` | Download a file from a bucket (optional destination) | `python cloud-storage.py --download-file my-bucket file.txt ./local-file.txt` |
| `--delete-file <bucket> <file>` | Delete a file from a bucket | `python cloud-storage.py --delete-file my-bucket file.txt` |
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
- The `--list-buckets` command shows bucket names, locations, and location types for all buckets in your project
- When uploading files, the file path you provide will be preserved in the Cloud Storage object name
- Ensure the file exists and is accessible before uploading
- Uploaded files maintain their original filename and path structure in Cloud Storage