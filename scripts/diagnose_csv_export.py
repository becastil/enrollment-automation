#!/usr/bin/env python3
"""
Diagnose CSV Export Issues on Windows
======================================
"""

import os
import sys
import platform

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("="*70)
print("DIAGNOSTICS FOR CSV EXPORT")
print("="*70)

# Check platform
print(f"\nPlatform: {platform.system()}")
print(f"Python: {sys.version}")
print(f"Working directory: {os.getcwd()}")

# Check if we can import the modules
try:
    from enrollment_automation_v6 import CID_TO_TAB
    print(f"\n✓ Successfully imported enrollment_automation_v6")
    print(f"  CID_TO_TAB has {len(CID_TO_TAB)} entries")
    # Show a few entries
    for cid in list(CID_TO_TAB.keys())[:5]:
        print(f"    {cid}: {CID_TO_TAB[cid]}")
except ImportError as e:
    print(f"\n✗ Failed to import enrollment_automation_v6: {e}")
    sys.exit(1)

# Check for configuration files
config_files = [
    "config/plan_mappings.json",
    "config/block_aggregations.json",
    "config/legacy_client_config.json"
]

print("\nChecking configuration files:")
for config_file in config_files:
    full_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), config_file)
    if os.path.exists(full_path):
        size = os.path.getsize(full_path)
        print(f"  ✓ {config_file} exists ({size} bytes)")
    else:
        print(f"  ✗ {config_file} NOT FOUND at {full_path}")

# Try loading the functions
try:
    from enrollment_automation_v6 import (
        load_plan_mappings,
        load_block_aggregations,
        read_and_prepare_data,
        build_tier_data_from_source
    )
    print("\n✓ All functions imported successfully")
    
    # Try loading configurations
    print("\nLoading configurations:")
    
    plan_mappings = load_plan_mappings()
    print(f"  ✓ Plan mappings loaded: {len(plan_mappings)} entries")
    
    block_aggregations = load_block_aggregations()
    print(f"  ✓ Block aggregations loaded: {len(block_aggregations)} tabs")
    for tab in list(block_aggregations.keys())[:3]:
        print(f"    {tab}: {len(block_aggregations[tab])} facilities")
    
except Exception as e:
    print(f"\n✗ Error loading functions: {e}")
    import traceback
    traceback.print_exc()

# Check source data file - handle both platforms
is_windows = platform.system() == 'Windows'
if is_windows:
    source_path = r"C:\Users\becas\Prime_EFR\data\input\source_data.xlsx"
else:
    source_path = "/mnt/c/Users/becas/Prime_EFR/data/input/source_data.xlsx"

if os.path.exists(source_path):
    print(f"\n✓ Source data exists: {source_path}")
    print(f"  Size: {os.path.getsize(source_path):,} bytes")
else:
    print(f"\n✗ Source data NOT FOUND: {source_path}")

# Try to load and process data
try:
    print("\nAttempting to load and process data:")
    
    df = read_and_prepare_data(source_path, plan_mappings)
    print(f"  ✓ Data loaded: {len(df)} rows")
    
    if len(df) > 0:
        print(f"  Columns: {list(df.columns)[:5]}...")
        print(f"  Unique Client IDs: {df['CLIENT ID'].nunique()}")
        
        # Show first few client IDs
        unique_clients = df['CLIENT ID'].unique()[:5]
        print(f"  Sample Client IDs: {list(unique_clients)}")
    
    # Try building tier data
    print("\n  Building tier data...")
    tier_data = build_tier_data_from_source(df, block_aggregations, False)
    print(f"  ✓ Tier data built: {len(tier_data)} facilities")
    
    if tier_data:
        # Show first entry
        first_cid = list(tier_data.keys())[0]
        print(f"\n  Sample tier data for {first_cid}:")
        print(f"    {tier_data[first_cid]}")
    else:
        print("\n  ⚠️ Tier data is empty!")
        print("  This might be because:")
        print("    1. Block aggregations aren't loading properly")
        print("    2. Client IDs in data don't match CID_TO_TAB")
        print("    3. Data filtering is too restrictive")
        
        # Debug: Check if client IDs match
        print("\n  Checking Client ID matching:")
        data_cids = set(df['CLIENT ID'].unique())
        mapping_cids = set(CID_TO_TAB.keys())
        
        common_cids = data_cids & mapping_cids
        print(f"    Client IDs in data: {len(data_cids)}")
        print(f"    Client IDs in CID_TO_TAB: {len(mapping_cids)}")
        print(f"    Common Client IDs: {len(common_cids)}")
        
        if len(common_cids) > 0:
            print(f"    Sample common CIDs: {list(common_cids)[:5]}")
        
        data_only = data_cids - mapping_cids
        if data_only:
            print(f"    CIDs in data but not in mapping: {list(data_only)[:5]}")
        
except Exception as e:
    print(f"\n✗ Error processing data: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70)
print("END DIAGNOSTICS")
print("="*70)