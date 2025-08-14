# Google BigQuery CLI

A command-line tool for managing Google BigQuery datasets and tables as part of the GCP CLI Toolkit.

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
./gcpcli.py bigquery --create-dataset my-dataset-name
```

**Delete a dataset:**
```bash
./gcpcli.py bigquery --delete-dataset my-dataset-name
```

**Delete a dataset with force (deletes all tables first):**
```bash
./gcpcli.py bigquery --delete-dataset my-dataset-name --force
```

> **Important Note**: Deleting a dataset will permanently remove it and all its tables and data. This action cannot be undone. The `--force` option will delete all tables in the dataset before deleting the dataset itself.

### Table Management

**Create a table in a dataset:**
```bash
./gcpcli.py bigquery --create-table my-dataset-name my-table-name
```

**Create a table with schema:**
```bash
./gcpcli.py bigquery --create-table my-dataset-name my-table-name --json-schema schema.json
```

**Update a table's schema:**
```bash
./gcpcli.py bigquery --update-table my-dataset-name my-table-name --json-schema schema.json
```

**Delete a table:**
```bash
./gcpcli.py bigquery --delete-table my-dataset-name my-table-name
```

**Load CSV data into a table:**
```bash
./gcpcli.py bigquery --load-csv my-dataset-name my-table-name path/to/data.csv
```

**Load CSV with header row:**
```bash
./gcpcli.py bigquery --load-csv my-dataset-name my-table-name path/to/data.csv --skip-rows 1
```

**Execute a query from command line:**
```bash
./gcpcli.py bigquery --query "SELECT * FROM my-dataset-name.my-table-name LIMIT 10"
```

**Execute a query from a file:**
```bash
./gcpcli.py bigquery --query-file path/to/query.sql
```

**Execute a direct query:**
```bash
./gcpcli.py bigquery --query "SELECT COUNT(*) FROM my-dataset.my-table"
```

> **Important Note**: Deleting a table will permanently remove it and all its data. This action cannot be undone. Make sure you have backed up any important data before deletion.

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

## CSV Loading Considerations

When loading CSV data into BigQuery tables, consider the following:

### **File Format Requirements:**
- **Encoding**: UTF-8 is recommended
- **Delimiters**: Comma (default), semicolon, tab, or custom
- **Headers**: Can be skipped using `--skip-rows`
- **File Size**: Large files are automatically handled by BigQuery

### **Data Type Considerations:**
- **Auto-detection**: BigQuery will attempt to auto-detect data types
- **Schema Mismatch**: If table has a defined schema, data must match it
- **Date/Time**: Use standard formats (YYYY-MM-DD, YYYY-MM-DD HH:MM:SS)
- **Numbers**: Use standard decimal notation (no currency symbols)

### **Performance Tips:**
- **Large Files**: BigQuery handles large files efficiently
- **Parallel Loading**: Multiple files can be loaded simultaneously
- **Error Handling**: Check job status for any loading errors

### **Common Use Cases:**
```bash
# Load standard CSV
./gcpcli.py bigquery --load-csv my-dataset my-table data.csv

# Load into table with defined schema
./gcpcli.py bigquery --create-table my-dataset my-table --json-schema schema.json
./gcpcli.py bigquery --load-csv my-dataset my-table data.csv
```

## Query Execution

BigQuery provides powerful SQL querying capabilities. The CLI supports multiple ways to execute queries:

### **Query Types:**

1. **Command line queries** (`--query`): Execute SQL directly from command line
2. **File-based queries** (`--query-file`): Load SQL from a file

### **Query File Format:**
- **Encoding**: UTF-8 recommended
- **File Extension**: `.sql` (conventional)
- **Content**: Standard BigQuery SQL syntax
- **Size**: No practical limit for query files

### **Query Considerations:**
- **Project Context**: Queries run in the context of your GCP project
- **Dataset References**: Use `project.dataset.table` or `dataset.table` format
- **Cost Management**: Monitor query costs in BigQuery console
- **Result Limits**: Large result sets are handled automatically
- **Error Handling**: SQL syntax errors are reported clearly

### **Common Query Patterns:**
```bash
# Simple SELECT from command line
./gcpcli.py bigquery --query "SELECT * FROM my-dataset.my-table LIMIT 10"

# Aggregation from command line
./gcpcli.py bigquery --query "SELECT COUNT(*) FROM my-dataset.my-table"

# Complex query from file
./gcpcli.py bigquery --query-file complex_analysis.sql

# Parameterized-like query from command line
./gcpcli.py bigquery --query "SELECT * FROM my-dataset.my-table WHERE date >= '2024-01-01'"
```

### **Query File Example (`queries/employee_analysis.sql`):**
```sql
SELECT
    department,
    COUNT(*) as employee_count,
    AVG(salary) as avg_salary,
    MAX(salary) as max_salary
FROM my-dataset.employees
WHERE active = true
GROUP BY department
ORDER BY avg_salary DESC
```

## Command Reference

| Command | Description | Example |
|---------|-------------|---------|
| `--create-dataset <name>` | Create a new dataset | `./gcpcli.py bigquery --create-dataset my-dataset` |
| `--delete-dataset <name> [--force]` | Delete a dataset (--force deletes all tables first) | `./gcpcli.py bigquery --delete-dataset my-dataset --force` |
| `--create-table <dataset> <table> [--json-schema <file>]` | Create a new table in a dataset (optional schema) | `./gcpcli.py bigquery --create-table my-dataset my-table --json-schema schema.json` |
| `--update-table <dataset> <table> --json-schema <file>` | Update a table's schema | `./gcpcli.py bigquery --update-table my-dataset my-table --json-schema schema.json` |
| `--delete-table <dataset> <table>` | Delete a table | `./gcpcli.py bigquery --delete-table my-dataset my-table` |
| `--load-csv <dataset> <table> <file>` | Load CSV data into a table | `./gcpcli.py bigquery --load-csv my-dataset my-table data.csv` |
| `--query <sql>` | Execute SQL query from command line | `./gcpcli.py bigquery --query "SELECT * FROM my-dataset.my-table"` |
| `--query-file <file>` | Execute SQL query from file | `./gcpcli.py bigquery --query-file query.sql` |
| `--json-schema <file>` | JSON schema file for table creation/update | `./gcpcli.py bigquery --create-table my-dataset my-table --json-schema schema.json` |
| `--force` | Force deletion (deletes all contained objects first) | `./gcpcli.py bigquery --delete-dataset my-dataset --force` |

## Common BigQuery Locations

Here are some commonly used BigQuery locations for dataset creation:

- `