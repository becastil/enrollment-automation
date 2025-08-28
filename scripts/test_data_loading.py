#!/usr/bin/env python3
"""Test data loading to debug CSV export"""

import os
import sys
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from enrollment_automation_v6 import (
    CID_TO_TAB,
    load_block_aggregations,
    read_and_prepare_data,
    build_tier_data_from_source,
    load_plan_mappings
)

# Load source data
source_path = "/mnt/c/Users/becas/Prime_EFR/data/input/source_data.xlsx"
print(f"Loading from: {source_path}")

# Check if file exists
if not os.path.exists(source_path):
    print(f"File not found: {source_path}")
    sys.exit(1)

# Load data
plan_mappings = load_plan_mappings()
print(f"Plan mappings loaded: {len(plan_mappings)} entries")

df = read_and_prepare_data(source_path, plan_mappings)
print(f"Data loaded: {len(df)} rows")
print(f"Columns: {list(df.columns)}")

# Show first few rows
if len(df) > 0:
    print("\nFirst 3 rows:")
    print(df.head(3))
    
    # Check for CLIENT ID column
    if 'CLIENT ID' in df.columns:
        unique_clients = df['CLIENT ID'].unique()
        print(f"\nUnique Client IDs: {len(unique_clients)}")
        print(f"First 5: {list(unique_clients[:5])}")
    else:
        print("\n⚠️ No 'CLIENT ID' column found")
        print("Available columns:", list(df.columns))

# Load block aggregations
block_aggregations = load_block_aggregations()
print(f"\nBlock aggregations loaded: {len(block_aggregations)} tabs")

# Try to build tier data
print("\nBuilding tier data...")
tier_data = build_tier_data_from_source(df, block_aggregations, False)
print(f"Tier data built: {len(tier_data)} facilities")

if tier_data:
    # Show sample
    for cid in list(tier_data.keys())[:3]:
        print(f"\n{cid}:")
        print(f"  Data: {tier_data[cid]}")
else:
    print("\n⚠️ No tier data generated")
    print("This likely means the data structure doesn't match expected format")