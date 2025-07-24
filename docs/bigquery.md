# Google BigQuery CLI

A command-line tool for managing Google BigQuery datasets and tables.

## Configuration

The following environment variables are required to connect with the BigQuery service:

```
GCP_PROJECT_ID=your-project-id
GCP_SERVICE_ACCOUNT_PATH=path/to/your/service-account.json
```

## Usage

### Dataset Management

**Create a dataset:**
```bash
python bigquery.py --create-dataset my-dataset-name
```

### Table Management

**Create a table in a dataset:**
```bash
python bigquery.py --create-table my-dataset-name my-table-name
```

**Update a table's schema:**
```bash
python bigquery.py --update-table my-dataset-name my-table-name --json-schema schema.json
```

## JSON Schema Format

The JSON schema file should contain the complete table schema in the following format:

```json
{
  "schema_fields": [
    {
      "name": "field_name",
      "field_type": "STRING",
      "mode": "NULLABLE"
    },
    {
      "name": "another_field",
      "field_type": "INTEGER",
      "mode": "REQUIRED"
    }
  ]
}
```

> **Example**: See `examples/bigquery/schema_example.json` for a comprehensive example that demonstrates all supported field types and modes, including nested RECORD structures.

### Supported Field Types:
- `STRING`, `INTEGER`, `FLOAT`, `BOOLEAN`, `TIMESTAMP`, `DATE`, `DATETIME`, `NUMERIC`, `BIGNUMERIC`, `BYTES`, `RECORD`, `GEOGRAPHY`

> **Reference**: For a complete list of supported field types, see the [BigQuery REST API documentation](https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#TableFieldSchema.FIELDS.type).

### Supported Modes:
- `NULLABLE` (default) - Field can contain NULL values
- `REQUIRED` - Field must have a value
- `REPEATED` - Field can contain multiple values (array)

## Command Reference

| Command | Description | Example |
|---------|-------------|---------|
| `--create-dataset <name>` | Create a new dataset | `python bigquery.py --create-dataset my-dataset` |
| `--create-table <dataset> <table>` | Create a new table in a dataset | `python bigquery.py --create-table my-dataset my-table` |
| `--update-table <dataset> <table>` | Update a table's schema | `python bigquery.py --update-table my-dataset my-table --json-schema schema.json` |
| `--json-schema <file>` | JSON schema file for table creation/update | `python bigquery.py --update-table my-dataset my-table --json-schema schema.json` |

## Common BigQuery Locations

Here are some commonly used BigQuery locations for dataset creation:

- `US` (United States)
- `EU` (European Union)
- `asia-northeast1` (Tokyo)
- `asia-southeast1` (Singapore)
- `australia-southeast1` (Sydney)
- `europe-west1` (Belgium)
- `europe-west2` (London)
- `us-central1` (Iowa)
- `us-east1` (South Carolina)
- `us-west1` (Oregon)

## Notes

- Dataset names must be unique within your project
- Dataset names can only contain letters, numbers, and underscores
- Dataset names must start with a letter or underscore
- If no location is specified, the dataset will be created in the default location (usually `US`)
- Make sure your service account has the necessary BigQuery permissions
- Dataset creation is an idempotent operation - if the dataset already exists, the command will succeed
- Datasets are containers for tables and views in BigQuery
- Each dataset belongs to a specific project and location

## Important Schema Update Limitations

### ⚠️ Critical BigQuery Schema Update Rules

When updating existing tables, BigQuery has strict limitations that you must be aware of:

#### 1. **Complete Schema Definition Required**
When updating an existing table, you must define **ALL** fields in your JSON schema, including existing ones. If you omit any existing field, you'll get an error like:
```
Provided Schema does not match Table. Field 'age' is missing in new schema
```

**Solution**: Always include all existing fields in your schema update, even if you're not changing them.

#### 2. **No Adding Required Fields to Existing Tables**
You cannot add new fields as `REQUIRED` to existing tables. You'll get an error like:
```
Cannot add required fields to an existing schema
```

**Solution**: Add new fields as `NULLABLE` first, then update them to `REQUIRED` in a separate operation.

#### 4. **Example Schema Update Workflow**

**Step 1**: Get current schema
```bash
# You'll need to check the current table schema first
# This helps you include all existing fields
```

**Step 2**: Create updated schema JSON
```json
{
  "schema_fields": [
    {"name": "existing_field_1", "field_type": "STRING", "mode": "NULLABLE"},
    {"name": "existing_field_2", "field_type": "INTEGER", "mode": "REQUIRED"},
    {"name": "new_field", "field_type": "STRING", "mode": "NULLABLE"}
  ]
}
```

**Step 3**: Update table
```bash
python bigquery.py --update-table my-dataset my-table --json-schema updated_schema.json
```

#### 5. **Common Error Scenarios**

| Error | Cause | Solution |
|-------|-------|----------|
| `Field 'X' is missing in new schema` | Omitted existing field | Include all existing fields |
| `Cannot add required fields` | Added new field as REQUIRED | Use NULLABLE for new fields |
| `Invalid JSON` | Malformed schema file | Check JSON syntax |
| `File not found` | Wrong schema file path | Verify file location |

#### 6. **Recommended Approach**

1. **For New Tables**: Design your complete schema upfront
2. **For Existing Tables**:
   - Export current schema first
   - Modify schema to include all existing fields
   - Add new fields as NULLABLE
   - Update in stages if needed