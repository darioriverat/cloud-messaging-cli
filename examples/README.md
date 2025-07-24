# GCP Assistant Examples

This folder contains example files for use with the GCP Assistant CLI tools, organized by service.

## Available Examples

### BigQuery Examples

BigQuery schema examples for table creation and updates.

**Location**: `examples/bigquery/`

**Files**:
- `schema_example.json` - Basic schema with all field types and modes
- `complex_schema_example.json` - Complex nested RECORD structures
- `README.md` - Detailed documentation and usage examples

**Usage**:
```bash
# Basic schema example
python bigquery.py --create-table my-dataset users --json-schema examples/bigquery/schema_example.json

# Complex nested schema example
python bigquery.py --create-table my-dataset employees --json-schema examples/bigquery/complex_schema_example.json
```

📖 **[BigQuery Examples Documentation](bigquery/README.md)**

## Future Examples

This structure allows for easy addition of examples for other GCP services:

- `examples/pubsub/` - Pub/Sub topic and subscription examples
- `examples/cloud-storage/` - Cloud Storage bucket and file examples
- `examples/compute/` - Compute Engine instance examples
- `examples/functions/` - Cloud Functions examples

## Organization Benefits

- **Service-specific examples**: Each service has its own subfolder
- **Easy navigation**: Clear structure for finding relevant examples
- **Scalable**: Easy to add new services and examples
- **Consistent**: Uniform structure across all services