
"""
Enrollment Data Processing Demo Script
=====================================

This script demonstrates how to use the build_facility_summary function 
to process enrollment data from Excel files with multiple tabs.

Author: Automated Processing System
Date: August 2025
"""

import pandas as pd
import numpy as np
import sys
import os
from typing import Dict, List, Optional, Tuple, Union

# Add parent directory to path to import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.enrollment_data_processing import build_facility_summary, process_all_enrollment_tabs

# STEP 1: Load your mapping data
print("=" * 60)
print("STEP 1: Loading Mapping Data")
print("=" * 60)

# Load facility mapping (adjust path as needed)
try:
    facility_map_df = pd.read_csv('../data/reference/facility_mapping_complete.csv')
    print("Facility mapping loaded successfully:")
    print(facility_map_df.head())
except:
    print("Using sample facility mapping data...")
    facility_map_df = pd.DataFrame({
        'CLIENT ID': ['H3100', 'H3270', 'H3271', 'H3272'],
        'Facility': ['Chino Valley Medical Center', 'Centinela Hospital Medical Center', 
                    'Robotics Outpatient Center', 'Centinela Valley Endoscopy Center'],
        'TPA Code': ['H3100', 'H3270', 'H3271', 'H3272']
    })

# Load plan mapping (adjust path as needed)
try:
    plan_map_df = pd.read_csv('plan_mapping_complete.csv')
    print("\nPlan mapping loaded successfully:")
    print(plan_map_df.head())
except:
    print("Using sample plan mapping data...")
    plan_map_df = pd.DataFrame({
        'PLAN': ['EPO1', 'EPO2', 'PPO1', 'PPO2', 'VAL1', 'VAL2'],
        'EPO-PPO-VALUE': ['EPO', 'EPO', 'PPO', 'PPO', 'VALUE', 'VALUE']
    })

# STEP 2: Process individual sheet example
print("\n" + "=" * 60)
print("STEP 2: Processing Individual Sheet")
print("=" * 60)

# Use sample file if original not found, otherwise use the original
import os
if os.path.exists("Prime Enrollment Funding by Facility for July.xlsx"):
    excel_file_path = "Prime Enrollment Funding by Facility for July.xlsx"
else:
    excel_file_path = "Prime_Enrollment_Sample.xlsx"
    print(f"Using sample file: {excel_file_path}")

# Example: Process just the "Cleaned use this one" sheet
try:
    enriched_data, full_summary, filtered_summary = build_facility_summary(
        excel_path=excel_file_path,
        sheet_name="Cleaned use this one",
        facility_key_col="CLIENT ID",  # Adjust based on your actual column names
        plan_type_col="PLAN",          # Adjust based on your actual column names
        facility_map=facility_map_df,
        plan_map=plan_map_df,
        measure_col=None  # Set to column name if you want to sum a specific measure instead of counting
    )

    print(f"Processing completed!")
    print(f"- Total records processed: {len(enriched_data)}")
    print(f"- Summary records: {len(full_summary)}")
    print(f"- Filtered summary records: {len(filtered_summary)}")

    print("\nFirst 5 rows of summary:")
    print(full_summary.head())

except Exception as e:
    print(f"Error processing individual sheet: {e}")

# STEP 3: Process all tabs at once
print("\n" + "=" * 60)
print("STEP 3: Processing All Tabs")
print("=" * 60)

try:
    # Process all facility tabs
    all_results = process_all_enrollment_tabs(
        excel_path=excel_file_path,
        facility_map=facility_map_df,
        plan_map=plan_map_df,
        facility_key_col="CLIENT ID",
        plan_type_col="PLAN",
        measure_col=None  # or specify a column name to sum instead of counting
    )

    print(f"\nProcessing completed for {len([k for k, v in all_results.items() if v is not None])} sheets!")

    # Display summary for each processed sheet
    for sheet_name, result in all_results.items():
        if result is not None:
            enriched, full_summary, filtered_summary = result
            print(f"\n{sheet_name}:")
            print(f"  - Total records: {len(enriched)}")
            print(f"  - Summary records: {len(full_summary)}")
            print(f"  - Filtered records: {len(filtered_summary)}")
        else:
            print(f"\n{sheet_name}: Failed to process")

except Exception as e:
    print(f"Error processing all tabs: {e}")

# STEP 4: Export results to CSV files
print("\n" + "=" * 60)
print("STEP 4: Exporting Results")
print("=" * 60)

try:
    if 'all_results' in locals():
        # Create consolidated summary across all facilities
        all_summaries = []

        for sheet_name, result in all_results.items():
            if result is not None:
                enriched, full_summary, filtered_summary = result
                # Add sheet identifier
                full_summary['source_sheet'] = sheet_name
                all_summaries.append(full_summary)

        if all_summaries:
            consolidated_summary = pd.concat(all_summaries, ignore_index=True)
            consolidated_summary.to_csv('consolidated_enrollment_summary.csv', index=False)
            print(f"Consolidated summary exported: {len(consolidated_summary)} records")

            # Show top facilities by contract count
            if 'contract_count' in consolidated_summary.columns:
                top_facilities = consolidated_summary.groupby('facility_name')['contract_count'].sum().sort_values(ascending=False).head(10)
                print("\nTop 10 Facilities by Contract Count:")
                print(top_facilities)

except Exception as e:
    print(f"Error exporting results: {e}")

print("\n" + "=" * 60)
print("PROCESSING COMPLETE!")
print("=" * 60)

# STEP 5: Usage instructions
print("""
USAGE INSTRUCTIONS:
==================

1. Ensure your Excel file is accessible at the specified path
2. Update column names in the function calls to match your actual data:
   - facility_key_col: Column containing facility identifiers
   - plan_type_col: Column containing plan type codes
   - measure_col: Column to sum (leave None to count contracts)

3. Update mapping DataFrames with your actual reference data:
   - facility_map_df: Maps facility keys to standardized names and client IDs
   - plan_map_df: Maps plan codes to plan groups (EPO/PPO/VALUE)

4. Customize facility groupings by modifying the facility_group_names and 
   facility_group_client_ids parameters in the function calls.

5. The function returns three DataFrames for each sheet:
   - enriched_data: Original data with added columns and validation flags
   - full_summary: Aggregated summary by facility and plan group
   - filtered_summary: Summary filtered to specific facility group

VALIDATION FEATURES:
===================
- missing_facility_flag: Identifies contracts with no facility mapping
- missing_plan_flag: Identifies contracts with no plan group mapping
- Handles various contract identifier column names
- Filters to subscriber records to avoid double-counting dependents
""")
