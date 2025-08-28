#!/usr/bin/env python3
"""
Export Enrollment Data to CSV for VBA Macro
===========================================

This script exports enrollment data to a CSV format that can be
consumed by a VBA macro to update the Excel template.
"""

import os
import sys
import pandas as pd
import json
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from enrollment_automation_v6 import (
    CID_TO_TAB,
    load_block_aggregations,
    read_and_prepare_data,
    build_tier_data_from_source,
    load_plan_mappings
)


def export_enrollment_to_csv():
    """Export enrollment data to CSV format for VBA macro consumption"""
    
    print("\n" + "="*70)
    print("EXPORTING ENROLLMENT DATA TO CSV")
    print("="*70)
    
    # Paths - handle both Windows and WSL
    import platform
    is_windows = platform.system() == 'Windows'
    
    if is_windows:
        source_data_path = r"C:\Users\becas\Prime_EFR\data\input\source_data.xlsx"
        output_csv_path = r"C:\Users\becas\Prime_EFR\enrollment_data.csv"
    else:
        source_data_path = "/mnt/c/Users/becas/Prime_EFR/data/input/source_data.xlsx"
        output_csv_path = "/mnt/c/Users/becas/Prime_EFR/enrollment_data.csv"
    
    # Check source exists
    if not os.path.exists(source_data_path):
        print(f"✗ Source data not found: {source_data_path}")
        return 1
    
    print(f"✓ Source data found: {source_data_path}")
    
    # Load source data
    plan_mappings = load_plan_mappings()
    df = read_and_prepare_data(source_data_path, plan_mappings)
    block_aggregations = load_block_aggregations()
    
    # Build aggregated tier data
    tier_data = build_tier_data_from_source(
        df, 
        block_aggregations,
        False  # allow_ppo
    )
    
    # Create CSV data structure
    csv_rows = []
    
    for client_id, facility_data in tier_data.items():
        if client_id not in CID_TO_TAB:
            continue
        
        tab_name = CID_TO_TAB[client_id]
        
        # Process each plan type (EPO, VALUE)
        for plan_type in ['EPO', 'VALUE']:
            if plan_type in facility_data:
                plan_type_data = facility_data[plan_type]
                
                # Handle nested structure - plan_type_data may contain plan names as keys
                if isinstance(plan_type_data, dict):
                    # Check if it's a nested structure with plan names
                    first_key = next(iter(plan_type_data.keys())) if plan_type_data else None
                    if first_key and isinstance(plan_type_data[first_key], dict):
                        # Nested structure: aggregate all plans of this type
                        tier_totals = {}
                        for plan_name, tiers in plan_type_data.items():
                            for tier, value in tiers.items():
                                if tier not in tier_totals:
                                    tier_totals[tier] = 0
                                tier_totals[tier] += value
                        
                        # Add rows for aggregated tiers
                        for tier, value in tier_totals.items():
                            if value > 0:  # Only include non-zero values
                                csv_rows.append({
                                    'Tab': tab_name,
                                    'ClientID': client_id,
                                    'PlanType': plan_type,
                                    'Tier': tier,
                                    'Value': value
                                })
                    else:
                        # Direct tier structure
                        for tier, value in plan_type_data.items():
                            if value > 0:  # Only include non-zero values
                                csv_rows.append({
                                    'Tab': tab_name,
                                    'ClientID': client_id,
                                    'PlanType': plan_type,
                                    'Tier': tier,
                                    'Value': value
                                })
    
    # Check if we have data
    if not csv_rows:
        print("\n⚠️ No enrollment data found to export")
        print("\nDebugging tier_data structure:")
        for cid in list(tier_data.keys())[:3]:  # Show first 3
            print(f"  {cid}: {tier_data[cid]}")
        return 1
    
    # Convert to DataFrame and save
    csv_df = pd.DataFrame(csv_rows)
    
    # Sort for consistency
    csv_df = csv_df.sort_values(['Tab', 'ClientID', 'PlanType', 'Tier'])
    
    # Save to CSV
    csv_df.to_csv(output_csv_path, index=False)
    
    print(f"\n✓ Exported {len(csv_df)} rows to: {output_csv_path}")
    
    # Show summary
    print("\nSummary by Tab:")
    tab_counts = csv_df.groupby('Tab')['Value'].sum()
    for tab, total in tab_counts.items():
        print(f"  {tab}: {total:,} total enrollment")
    
    print(f"\nTotal Enrollment: {csv_df['Value'].sum():,}")
    
    return 0


if __name__ == "__main__":
    sys.exit(export_enrollment_to_csv())