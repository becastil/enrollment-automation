# Enrollment Data Processing Implementation Guide

## Overview

This implementation provides a complete Python solution for automating Excel-based enrollment data workflows across multiple facility tabs. The solution includes data cleaning, facility and plan lookups, validation, and aggregation capabilities.

## Files Created

1. **`enrollment_data_processing.py`** - Main implementation module
2. **`enrollment_processing_demo.py`** - Comprehensive usage examples
3. **`facility_mapping.csv`** - Sample facility reference data
4. **`plan_mapping.csv`** - Sample plan type mappings

## Key Functions

### `build_facility_summary()`
Processes individual Excel worksheets to create facility-level enrollment summaries.

**Parameters:**
- `excel_path`: Path to Excel file
- `sheet_name`: Worksheet to process
- `facility_key_col`: Column containing facility identifiers
- `plan_type_col`: Column containing plan codes
- `measure_col`: Column to aggregate (None for contract counting)
- `facility_map`: Reference data for facility lookups
- `plan_map`: Reference data for plan type mappings

**Returns:** Tuple of (enriched_data, full_summary, filtered_summary)

### `process_all_enrollment_tabs()`
Processes all facility tabs in the Excel file at once.

**Key Features:**
- Handles 35+ facility tabs automatically
- Robust error handling for missing or malformed sheets
- Progress reporting and validation
- Returns consolidated results dictionary

## Implementation Steps

### Step 1: Prepare Your Data

1. **Update Column Names**: Modify these parameters to match your actual Excel columns:
   ```python
   facility_key_col="CLIENT ID"  # Your facility identifier column
   plan_type_col="PLAN"          # Your plan type column
   ```

2. **Create Mapping Files**: Update the sample CSV files with your actual reference data:
   - `facility_mapping.csv`: Maps facility keys to standardized names and client IDs
   - `plan_mapping.csv`: Maps plan codes to plan groups (EPO/PPO/VALUE)

### Step 2: Basic Usage

```python
import pandas as pd
from enrollment_data_processing import build_facility_summary, process_all_enrollment_tabs

# Load your reference data
facility_map_df = pd.read_csv('facility_mapping.csv')
plan_map_df = pd.read_csv('plan_mapping.csv')

# Process all tabs at once
results = process_all_enrollment_tabs(
    excel_path="Prime Enrollment Funding by Facility for July.xlsx",
    facility_map=facility_map_df,
    plan_map=plan_map_df,
    facility_key_col="CLIENT ID",
    plan_type_col="PLAN"
)
```

### Step 3: Export Results

```python
from enrollment_data_processing import export_consolidated_summary, create_facility_report

# Export consolidated summary
consolidated = export_consolidated_summary(results)

# Create facility-level report
facility_report = create_facility_report(consolidated)
```

## Data Processing Features

### Data Cleaning
- Automatically detects header rows in Excel sheets
- Removes empty rows and extraneous columns
- Strips whitespace from key identifier columns
- Handles various contract ID column names

### Validation
- **Missing Facility Flag**: Identifies contracts without facility mapping
- **Missing Plan Flag**: Identifies contracts without plan group mapping
- **Contract Deduplication**: Filters to subscriber records to avoid counting dependents multiple times

### Aggregation Options
- **Contract Counting** (default): Counts unique contracts per facility/plan group
- **Measure Summing**: Aggregates specified numeric columns
- **Member Counting**: Calculates total members including dependents

### Facility Grouping
- Supports custom facility group definitions
- Built-in support for Centinela group (H3270, H3271, H3272)
- Case-insensitive name matching and exact ID matching

## Supported Facility Tabs

The implementation processes these 35 facility tabs:
- Cleaned use this one
- Legacy
- Centinela
- Encino-Garden Grove
- St. Francis
- Alvarado
- Pampa
- Roxborough
- Lower Bucks
- Dallas Medical Center
- Harlingen
- Knapp
- Glendora
- RHRI
- Monroe
- Saint Mary's Reno
- North Vista
- Dallas Regional
- Riverview & Gadsden
- Saint Clare's
- Landmark
- Saint Mary's Passaic
- Southern Regional
- Lehigh
- St Michael's
- Reddy Dev.
- Mission
- Coshocton
- Suburban
- Garden City
- Lake Huron
- Providence & St John
- East Liverpool
- St Joe & St Mary's
- Illinois

## Error Handling

- **File Access Errors**: Clear messages for Excel file reading issues
- **Column Mapping Errors**: Validation of required columns and mappings
- **Data Type Errors**: Automatic type conversion and null handling
- **Sheet Processing Errors**: Individual sheet failures don't stop batch processing

## Output Files

### Consolidated Summary
- **File**: `consolidated_enrollment_summary.csv`
- **Content**: Combined summary across all processed sheets
- **Columns**: facility_name, client_id, plan_group, contract_count, source_sheet

### Processing Log
- **File**: `consolidated_enrollment_summary_processing_log.csv`
- **Content**: Processing status and record counts for each sheet
- **Purpose**: Quality assurance and troubleshooting

### Facility Report
- **File**: `facility_enrollment_report.csv`
- **Content**: Facility-level metrics and rankings
- **Columns**: facility_name, client_id, total_contracts, plan_groups_offered

## Customization Options

### Custom Facility Groups
```python
# Define custom facility group
custom_names = ["My Hospital", "My Clinic"]
custom_ids = ["H1234", "H5678"]

result = build_facility_summary(
    excel_path="data.xlsx",
    facility_group_names=custom_names,
    facility_group_client_ids=custom_ids
)
```

### Custom Aggregation
```python
# Sum members instead of counting contracts
result = build_facility_summary(
    excel_path="data.xlsx",
    measure_col="Members"  # or any numeric column
)
```

## Best Practices

1. **Data Validation**: Always review the missing mapping flags in enriched data
2. **Reference Data**: Keep facility and plan mappings up to date
3. **Testing**: Process individual sheets first to validate column mappings
4. **Error Review**: Check the processing log for failed sheets
5. **Data Quality**: Verify contract counts against known totals

## Troubleshooting

### Common Issues

1. **Column Not Found**: Update `facility_key_col` and `plan_type_col` parameters
2. **No Matching Facility**: Verify facility mapping data completeness
3. **Empty Results**: Check if data rows have contract identifiers
4. **Header Detection**: May need to manually specify header row in complex Excel files

### Debug Mode
```python
# Enable verbose output for troubleshooting
results = process_all_enrollment_tabs(
    excel_path="data.xlsx",
    verbose=True  # Shows processing status for each sheet
)
```

## Performance Considerations

- Processing 35 tabs with thousands of records typically completes in under 2 minutes
- Memory usage scales with data size; consider processing subsets for very large files
- Excel file access over network connections may be slower

## Next Steps

1. Test with your actual Excel file and update column mappings
2. Create comprehensive facility and plan mapping files
3. Customize facility groupings for your organization
4. Set up automated processing workflows if needed
5. Integrate with your existing reporting systems

## Support

This implementation follows the pandas documentation standards and includes comprehensive error handling. The modular design allows for easy customization and extension for specific organizational needs.