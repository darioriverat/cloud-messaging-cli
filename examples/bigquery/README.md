# BigQuery Schema Examples

This folder contains BigQuery-specific example files for use with the GCP CLI Toolkit.

## Schema Examples

### `schema_example.json`

A comprehensive example of a BigQuery table schema that demonstrates:

- **All supported field types**: STRING, INTEGER, FLOAT, BOOLEAN, TIMESTAMP, DATE, DATETIME, NUMERIC, BIGNUMERIC, BYTES, RECORD, GEOGRAPHY
- **All field modes**: NULLABLE, REQUIRED, REPEATED
- **Nested structures**: RECORD type with nested fields
- **Real-world scenarios**: User profile data with various data types

### `complex_schema_example.json`

A complex example demonstrating multiple nested RECORD fields at different levels:

- **Multiple top-level RECORD fields**: personal_info, employment, preferences
- **Deep nesting**: Up to 4 levels of nested RECORD structures
- **Complex organizational data**: Employee information with department and manager hierarchies
- **Realistic business scenarios**: Contact information, employment details, user preferences

#### Nested Structure Examples:

**Level 1**: `personal_info` (RECORD)
- **Level 2**: `contact` (RECORD)
  - **Level 3**: `emergency_contact` (RECORD)
    - **Level 4**: name, phone, relationship (simple fields)

**Level 1**: `employment` (RECORD)
- **Level 2**: `department` (RECORD)
  - **Level 3**: `manager` (RECORD)
    - **Level 4**: manager_id, manager_name, manager_level (simple fields)

**Level 1**: `employment` (RECORD)
- **Level 2**: `salary_info` (RECORD)
  - **Level 3**: `benefits` (RECORD)
    - **Level 4**: health_insurance, dental_insurance, etc. (simple fields)

### Usage

```bash
# Create a dataset
python bigquery.py --create-dataset my-dataset

# Delete a dataset (⚠️ permanent)
python bigquery.py --delete-dataset my-dataset

# Delete a dataset with force (deletes all tables first)
python bigquery.py --delete-dataset my-dataset --force

# Create a table in the dataset
python bigquery.py --create-table my-dataset employees

# Create a table with the basic example schema
python bigquery.py --create-table my-dataset users --json-schema examples/bigquery/schema_example.json

# Create a table with the complex nested schema
python bigquery.py --create-table my-dataset employees --json-schema examples/bigquery/complex_schema_example.json

# Create a table without schema (empty table)
python bigquery.py --create-table my-dataset empty-table

# Update an existing table with the complex schema
python bigquery.py --update-table my-dataset employees --json-schema examples/bigquery/complex_schema_example.json

# Delete a table (⚠️ permanent)
python bigquery.py --delete-table my-dataset employees

# Load CSV data into a table
python bigquery.py --load-csv my-dataset employees data/employees.csv

# Execute a query from command line
python bigquery.py --query "SELECT COUNT(*) FROM my-dataset.employees"

# Execute a query from a file
python bigquery.py --query-file queries/employee_count.sql

# Execute a complex query from command line
python bigquery.py --query "SELECT name, department FROM my-dataset.employees WHERE salary > 50000"


### Schema Structure

The examples include:

1. **Basic Fields**: Simple data types like strings, integers, booleans
2. **Date/Time Fields**: TIMESTAMP, DATE, DATETIME for temporal data
3. **Numeric Fields**: NUMERIC and BIGNUMERIC for precise calculations
4. **Binary Data**: BYTES for storing binary content
5. **Arrays**: REPEATED fields for storing multiple values
6. **Nested Records**: RECORD type with nested address structure
7. **Geographic Data**: GEOGRAPHY for location information

### Field Types Demonstrated

| Field Type | Example | Use Case |
|------------|---------|----------|
| STRING | user_id, email | Text data, identifiers |
| INTEGER | age, scores | Whole numbers |
| FLOAT | score | Decimal numbers |
| BOOLEAN | is_active | True/false values |
| TIMESTAMP | created_at | Precise time with timezone |
| DATE | birth_date | Calendar dates |
| DATETIME | last_login | Date and time without timezone |
| NUMERIC | balance | Decimal with fixed precision |
| BIGNUMERIC | precise_balance | High-precision decimal |
| BYTES | profile_image | Binary data |
| RECORD | address | Nested structure |
| GEOGRAPHY | location | Geographic coordinates |

### Field Modes Demonstrated

| Mode | Example | Description |
|------|---------|-------------|
| REQUIRED | user_id, created_at | Field must have a value |
| NULLABLE | email, age | Field can be null (default) |
| REPEATED | tags, scores | Field can contain multiple values |

### Customizing the Schema

1. **Copy the example**: `cp examples/bigquery/schema_example.json my_schema.json`
2. **Modify fields**: Edit the JSON to match your data structure
3. **Remove unused fields**: Delete fields you don't need
4. **Add new fields**: Follow the same structure for new fields
5. **Test the schema**: Use with `--create-table` to test

### Important Notes

- **REQUIRED fields**: Can only be used for new tables, not when adding to existing tables
- **RECORD fields**: Must include a `fields` array with nested field definitions
- **REPEATED fields**: Cannot be nested inside RECORD fields
- **GEOGRAPHY fields**: Store geographic data in Well-Known Text (WKT) format
- **Nested RECORD fields**: Can be nested up to 15 levels deep in BigQuery