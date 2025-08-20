# Google Cloud Storage CLI

A command-line tool for managing Google Cloud Storage buckets and files as part of the GCP CLI Toolkit.

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
./gcpcli.py cloud-storage --create-bucket my-bucket-name
```

**Create a bucket in a specific region:**
```bash
./gcpcli.py cloud-storage --create-bucket my-bucket-name --region us-central1
```

**List all buckets in the project:**
```bash
./gcpcli.py cloud-storage --list-buckets
```

**Delete a bucket:**
```bash
./gcpcli.py cloud-storage --delete-bucket my-bucket-name
```

> **Note**: Trying to delete a non-empty bucket will trigger an error. Use the flag `--force` to force the deletion of all contents first.

**Force delete a bucket (delete all objects first):**
```bash
./gcpcli.py cloud-storage --delete-bucket my-bucket-name --force
```

### File Operations

**Upload a file to a bucket:**
```bash
./gcpcli.py cloud-storage --upload-file my-bucket-name /path/to/file.txt
```

**Upload a file with relative path:**
```bash
./gcpcli.py cloud-storage --upload-file my-bucket-name ./file.txt
```

> **Note**: Submitting `./file.txt` is different from sumbitting `file.txt`, as GCP will create a folder called `./` which is distinct from the root folder.


**Download a file from a bucket (preserves original path):**
```bash
./gcpcli.py cloud-storage --download-file my-bucket-name /path/to/file.txt
```

> **Note**: When downloading files from Cloud Storage we must ensure the cloud folder structure match the host file system structure. If we download `/path/folder/file.txt` the directory `/path/folder/` must exists in the host machine.

**Download a file to a specific destination:**
```bash
./gcpcli.py cloud-storage --download-file my-bucket-name /path/to/file.txt ~/downloaded-file.txt
```

**Delete a file from a bucket:**
```bash
./gcpcli.py cloud-storage --delete-file my-bucket-name /path/to/file.txt
```

> **Important Note**: When uploading files, GCP will create the underlying "path" structure in Cloud Storage based on the file path you provide. For example:
> - If you upload `~/hello.txt`, GCP will store it as `/Users/youruser/hello.txt`
> - If you upload `./file.txt`, GCP will store it as `./file.txt` using `./` as the folder name.
> - If you upload `/absolute/path/file.txt`, GCP will store it as `/absolute/path/file.txt`
>
> *The same rules apply when downloading and deleting files.*
>
> Consider using simple filenames or organizing your uploads with specific paths to avoid unexpected storage structures.

## Command Reference

| Command | Description | Example |
|---------|-------------|---------|
| `--create-bucket <name>` | Create a new bucket | `./gcpcli.py cloud-storage --create-bucket my-bucket` |
| `--list-buckets` | List all buckets in the project | `./gcpcli.py cloud-storage --list-buckets` |
| `--upload-file <bucket> <file>` | Upload a file to a bucket | `./gcpcli.py cloud-storage --upload-file my-bucket file.txt` |
| `--download-file <bucket> <file> [dest]` | Download a file from a bucket (optional destination) | `./gcpcli.py cloud-storage --download-file my-bucket file.txt ./local-file.txt` |
| `--delete-file <bucket> <file>` | Delete a file from a bucket | `./gcpcli.py cloud-storage --delete-file my-bucket file.txt` |
| `--delete-bucket <name> [--force]` | Delete a bucket (use --force for non-empty buckets) | `./gcpcli.py cloud-storage --delete-bucket my-bucket --force` |
| `--force` | Force delete bucket (delete all objects first) | `./gcpcli.py cloud-storage --delete-bucket my-bucket --force` |
| `--region <region>` | Specify the region for bucket creation | `./gcpcli.py cloud-storage --create-bucket my-bucket --region us-central1` |

## Notes

- Bucket names must be globally unique across all of Google Cloud Storage
- Bucket names can only contain lowercase letters, numbers, hyphens, and underscores
- Bucket names must start and end with a letter or number
- If no region is specified, the bucket will be created in the default location (usually `us-central1`)
- Make sure your service account has the necessary Storage permissions
- When uploading files, the file path you provide will be preserved in the Cloud Storage object name
- Uploaded files maintain their original filename and path structure in Cloud Storage