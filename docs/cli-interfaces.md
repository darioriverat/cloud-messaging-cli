# CLI Interfaces

The GCP CLI Toolkit provides two unified command-line interfaces for easy access to all tools.

## Overview

The toolkit offers two main CLI interfaces:

1. **`gcpcli.py`** - For Python-based tools (Pub/Sub, BigQuery, Cloud Storage)
2. **`gcpcli.sh`** - For shell-based tools (Artifact Registry) with optional Python support

## Python Scripts Interface (`gcpcli.py`)

The `gcpcli.py` interface is designed specifically for Python-based tools and provides a clean, unified way to access all Python scripts in the `gcptoolkit/` directory.

### Usage

```bash
# Using python command
python gcpcli.py <script_name> [args...]

# Using executable directly (recommended)
./gcpcli.py <script_name> [args...]
```

### Available Scripts

- `pubsub` - Google Cloud Pub/Sub management
- `bigquery` - Google BigQuery management
- `cloud-storage` - Google Cloud Storage management

### Examples

```bash
# Pub/Sub operations
./gcpcli.py pubsub --list-topics
./gcpcli.py pubsub --create-topic mytopic
./gcpcli.py pubsub --publish mytopic "Hello World"

# BigQuery operations
./gcpcli.py bigquery --create-dataset my-dataset
./gcpcli.py bigquery --create-table my-dataset my-table
./gcpcli.py bigquery --query "SELECT * FROM my-dataset.my-table LIMIT 10"

# Cloud Storage operations
./gcpcli.py cloud-storage --list-buckets
./gcpcli.py cloud-storage --create-bucket my-bucket --region us-central1
./gcpcli.py cloud-storage --upload-file my-bucket file.txt
```

### Features

- **Automatic script discovery** - Lists available scripts when no script name is provided
- **Helpful error messages** - Shows available scripts when an invalid script name is used
- **Proper dependency management** - Uses `uv run` to ensure correct Python environment
- **Executable** - Can be run directly with `./gcpcli.py`

### Error Handling

```bash
# No script name provided
$ ./gcpcli.py
Error: No script name provided
Usage: python gcpcli.py <script_name> [args...]
Available scripts:
  bigquery
  cloud-storage
  pubsub

# Invalid script name
$ ./gcpcli.py nonexistent
Error: Python script not found: nonexistent.py in /path/to/gcptoolkit
Available scripts:
  bigquery
  cloud-storage
  pubsub
```

## Shell Scripts Interface (`gcpcli.sh`)

The `gcpcli.sh` interface is designed for shell-based tools and also supports Python scripts with the `--python` flag.

### Usage

```bash
# Shell scripts (default)
./gcpcli.sh <script_name> [args...]

# Python scripts (with --python flag)
./gcpcli.sh --python <script_name> [args...]
```

### Available Scripts

**Shell Scripts:**
- `artifacts` - Google Artifact Registry management

**Python Scripts (with --python flag):**
- `pubsub` - Google Cloud Pub/Sub management
- `bigquery` - Google BigQuery management
- `cloud-storage` - Google Cloud Storage management

### Examples

```bash
# Artifact Registry operations (shell scripts)
./gcpcli.sh artifacts create-docker-repository my-repo --location us-central1
./gcpcli.sh artifacts push-docker-image myapp:v1.0 --repository my-repo --location us-central1

# Python scripts (with --python flag)
./gcpcli.sh --python pubsub --list-topics
./gcpcli.sh pubsub --python --list-topics  # --python can be anywhere
./gcpcli.sh pubsub --list-topics --python  # --python can be at the end
```

### Features

- **Flexible flag placement** - `--python` flag can be placed anywhere in the argument list
- **Backward compatibility** - Maintains support for existing shell script workflows
- **Unified interface** - Single entry point for both shell and Python tools

## Choosing the Right Interface

### Use `gcpcli.py` when:
- Working primarily with Python-based tools (Pub/Sub, BigQuery, Cloud Storage)
- Want the cleanest, most intuitive interface
- Don't need shell script functionality

### Use `gcpcli.sh` when:
- Working with shell-based tools (Artifact Registry)
- Need to mix shell and Python tools in the same workflow
- Want to maintain compatibility with existing shell-based automation

## Migration Guide

If you're migrating from direct script execution to the unified CLI:

### Before (Direct Execution)
```bash
python gcptoolkit/pubsub.py --list-topics
python gcptoolkit/bigquery.py --create-dataset my-dataset
./scripts/artifacts.sh create-docker-repository my-repo --location us-central1
```

### After (Unified CLI)
```bash
./gcpcli.py pubsub --list-topics
./gcpcli.py bigquery --create-dataset my-dataset
./gcpcli.sh artifacts create-docker-repository my-repo --location us-central1
```

## Troubleshooting

### Common Issues

1. **Permission Denied**
   ```bash
   chmod +x gcpcli.py
   chmod +x gcpcli.sh
   ```

2. **uv not found**
   ```bash
   # Install uv: https://docs.astral.sh/uv/
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Script not found**
   - Ensure you're in the correct directory
   - Check that the script exists in `gcptoolkit/` or `scripts/`
   - Verify the script name spelling

### Getting Help

```bash
# List available scripts
./gcpcli.py

# Get help for a specific script
./gcpcli.py pubsub --help
./gcpcli.sh artifacts --help
```