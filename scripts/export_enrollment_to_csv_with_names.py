#!/usr/bin/env python3
"""
Export Enrollment Data to CSV with Specific Plan Names
=======================================================

This script exports enrollment data to a CSV format that includes
specific plan names for more precise VBA macro matching.
"""

import os
import sys
import pandas as pd
import json
from datetime import datetime
import platform

# Get the project root directory (parent of scripts)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

# Change to project root so relative paths work
original_cwd = os.getcwd()
os.chdir(PROJECT_ROOT)

try:
    from enrollment_automation_v6 import (
        CID_TO_TAB,
        load_block_aggregations,
        read_and_prepare_data,
        build_tier_data_from_source,
        load_plan_mappings
    )
finally:
    # Restore original directory
    os.chdir(original_cwd)


def export_enrollment_to_csv():
    """Export enrollment data to CSV format with specific plan names"""
    
    print("\n" + "="*70)
    print("EXPORTING ENROLLMENT DATA TO CSV WITH PLAN NAMES")
    print("="*70)
    
    # Paths - handle both Windows and WSL
    is_windows = platform.system() == 'Windows'
    
    if is_windows:
        source_data_path = os.path.join(PROJECT_ROOT, "data", "input", "source_data.xlsx")
        output_csv_path = os.path.join(PROJECT_ROOT, "enrollment_data_detailed.csv")
    else:
        source_data_path = os.path.join(PROJECT_ROOT, "data", "input", "source_data.xlsx")
        output_csv_path = os.path.join(PROJECT_ROOT, "enrollment_data_detailed.csv")
    
    # Check source exists
    if not os.path.exists(source_data_path):
        print(f"✗ Source data not found: {source_data_path}")
        return 1
    
    print(f"✓ Source data found: {source_data_path}")
    
    # Change to project root for config loading
    original_cwd = os.getcwd()
    os.chdir(PROJECT_ROOT)
    
    try:
        # Load source data
        print("Loading configurations...")
        plan_mappings = load_plan_mappings()
        print(f"  ✓ Plan mappings loaded: {len(plan_mappings)} entries")
        
        block_aggregations = load_block_aggregations()
        print(f"  ✓ Block aggregations loaded: {len(block_aggregations)} tabs")
        
        print("\nLoading source data...")
        df = read_and_prepare_data(source_data_path, plan_mappings)
        print(f"  ✓ Data loaded: {len(df)} rows")
        
        # Build aggregated tier data
        print("\nBuilding tier data...")
        tier_data = build_tier_data_from_source(
            df, 
            block_aggregations,
            False  # allow_ppo
        )
        
        print(f"✓ Processed {len(tier_data)} facilities")
        
    finally:
        # Restore original directory
        os.chdir(original_cwd)
    
    # Create CSV data structure with specific plan names
    csv_rows = []
    
    for client_id, facility_data in tier_data.items():
        if client_id not in CID_TO_TAB:
            continue
        
        tab_name = CID_TO_TAB[client_id]
        
        # Process each plan type (EPO, VALUE)
        for plan_type in ['EPO', 'VALUE']:
            if plan_type in facility_data:
                plan_blocks = facility_data[plan_type]
                
                # Iterate through actual block labels
                for block_label, tier_counts in plan_blocks.items():
                    if isinstance(tier_counts, dict):
                        for tier, value in tier_counts.items():
                            # Handle numeric values
                            if isinstance(value, (int, float)) and value > 0:
                                csv_rows.append({
                                    'Tab': tab_name,
                                    'ClientID': client_id,
                                    'PlanType': plan_type,
                                    'PlanName': block_label,  # Use actual block label
                                    'Tier': tier,
                                    'Value': int(value)
                                })
    
    # Check if we have data
    if not csv_rows:
        print("\n⚠️ No enrollment data found to export")
        print("Debug info:")
        print(f"  - Tier data entries: {len(tier_data)}")
        print(f"  - CID_TO_TAB entries: {len(CID_TO_TAB)}")
        if tier_data:
            sample_cid = list(tier_data.keys())[0]
            print(f"  - Sample tier data for {sample_cid}: {tier_data[sample_cid]}")
        return 1
    
    # Convert to DataFrame and save
    csv_df = pd.DataFrame(csv_rows)
    
    # Sort for consistency
    csv_df = csv_df.sort_values(['Tab', 'ClientID', 'PlanType', 'PlanName', 'Tier'])
    
    # Save to CSV
    csv_df.to_csv(output_csv_path, index=False)
    
    print(f"\n✓ Exported {len(csv_df)} rows to: {output_csv_path}")
    
    # Show summary
    print("\nSummary by Tab:")
    tab_groups = csv_df.groupby('Tab')
    for tab, group in tab_groups:
        facility_count = group['ClientID'].nunique()
        plan_count = group['PlanName'].nunique()
        total = group['Value'].sum()
        print(f"  {tab}: {facility_count} facilities, {plan_count} unique plans, {total:,} total enrollment")
    
    print(f"\nTotal Enrollment: {csv_df['Value'].sum():,}")
    
    # Show unique plan names
    unique_plans = csv_df['PlanName'].dropna().unique()
    print(f"\nUnique Plan Names ({len(unique_plans)}):")
    for plan in sorted(unique_plans)[:10]:  # Show first 10
        print(f"  - {plan}")
    if len(unique_plans) > 10:
        print(f"  ... and {len(unique_plans) - 10} more")
    
    # Show sample rows
    print("\nSample CSV rows:")
    print(csv_df.head(10).to_string(index=False))
    
    print("\n✅ CSV file with detailed plan names ready!")
    
    return 0


if __name__ == "__main__":
    sys.exit(export_enrollment_to_csv())