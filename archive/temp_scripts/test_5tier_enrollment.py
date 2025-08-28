#!/usr/bin/env python3
"""
Test script to validate the 5-tier enrollment automation
"""

import pandas as pd
import sys
import os

# Import the updated enrollment_automation_v6
sys.path.insert(0, '/mnt/c/Users/becas/Prime_EFR')
from enrollment_automation_v6 import (
    read_and_prepare_data,
    build_tier_data_from_source,
    load_block_aggregations,
    load_plan_mappings,
    normalize_tier_strict
)

def test_5tier_processing():
    """Test the 5-tier processing for Encino-Garden Grove"""
    
    print("="*70)
    print("Testing 5-Tier Enrollment Processing")
    print("="*70)
    
    # Load source data for initial checks
    source_file = '/mnt/c/Users/becas/Prime_EFR/data/input/source_data.xlsx'
    df_raw = pd.read_excel(source_file)
    
    print(f"\nLoaded {len(df_raw)} rows from source_data.xlsx")
    
    # Check that we have both BEN CODE and CALCULATED BEN CODE columns
    assert 'BEN CODE' in df_raw.columns, "Missing BEN CODE column"
    assert 'CALCULATED BEN CODE' in df_raw.columns, "Missing CALCULATED BEN CODE column"
    
    print("\n✓ Both BEN CODE and CALCULATED BEN CODE columns present")
    
    # Check E1D values exist in CALCULATED BEN CODE
    e1d_count = (df_raw['CALCULATED BEN CODE'] == 'E1D').sum()
    print(f"✓ Found {e1d_count} rows with E1D in CALCULATED BEN CODE")
    
    # Test tier normalization for 5-tier tabs
    print("\n" + "-"*40)
    print("Testing Tier Normalization")
    print("-"*40)
    
    # Test 4-tier normalization
    assert normalize_tier_strict('EMP', use_five_tier=False) == 'EE Only'
    assert normalize_tier_strict('ESP', use_five_tier=False) == 'EE+Spouse'
    assert normalize_tier_strict('E1D', use_five_tier=False) == 'EE+Child(ren)'
    assert normalize_tier_strict('ECH', use_five_tier=False) == 'EE+Child(ren)'
    assert normalize_tier_strict('FAM', use_five_tier=False) == 'EE+Family'
    print("✓ 4-tier normalization working correctly")
    
    # Test 5-tier normalization
    assert normalize_tier_strict('EMP', use_five_tier=True) == 'EE Only'
    assert normalize_tier_strict('ESP', use_five_tier=True) == 'EE+Spouse'
    assert normalize_tier_strict('E1D', use_five_tier=True) == 'EE+1 Dep'
    assert normalize_tier_strict('ECH', use_five_tier=True) == 'EE+Child'
    assert normalize_tier_strict('FAM', use_five_tier=True) == 'EE+Family'
    print("✓ 5-tier normalization working correctly")
    
    # Filter for Encino-Garden Grove data
    print("\n" + "-"*40)
    print("Testing Encino-Garden Grove Data")
    print("-"*40)
    
    encino_df = df_raw[df_raw['CLIENT ID'].isin(['H3250', 'H3260'])]
    print(f"\nFound {len(encino_df)} rows for H3250/H3260")
    
    # Check distribution of CALCULATED BEN CODE for Encino
    calc_dist = encino_df['CALCULATED BEN CODE'].value_counts()
    print("\nCALCULATED BEN CODE distribution for H3250/H3260:")
    for code, count in calc_dist.items():
        print(f"  {code}: {count}")
    
    # Check that E1D exists
    assert 'E1D' in calc_dist.index, "E1D not found in CALCULATED BEN CODE for H3250/H3260"
    print(f"\n✓ E1D present with {calc_dist.get('E1D', 0)} occurrences")
    
    # Process data through the pipeline
    print("\n" + "-"*40)
    print("Testing Full Pipeline Processing")
    print("-"*40)
    
    # Load configurations
    plan_mappings = load_plan_mappings()
    block_aggregations = load_block_aggregations()
    
    # Process the source data using the proper function
    processed_df = read_and_prepare_data(source_file, plan_mappings)
    print(f"\nProcessed data has {len(processed_df)} rows after filtering")
    
    # Build tier data
    tier_data = build_tier_data_from_source(processed_df, block_aggregations)
    
    # Check H3250 tier data
    if 'H3250' in tier_data:
        print("\nH3250 Tier Data:")
        for plan_type in tier_data['H3250']:
            print(f"\n  {plan_type}:")
            for block in tier_data['H3250'][plan_type]:
                print(f"    {block}:")
                for tier, count in tier_data['H3250'][plan_type][block].items():
                    if count > 0:
                        print(f"      {tier}: {count}")
    
    # Check H3260 tier data
    if 'H3260' in tier_data:
        print("\nH3260 Tier Data:")
        for plan_type in tier_data['H3260']:
            print(f"\n  {plan_type}:")
            for block in tier_data['H3260'][plan_type]:
                print(f"    {block}:")
                for tier, count in tier_data['H3260'][plan_type][block].items():
                    if count > 0:
                        print(f"      {tier}: {count}")
    
    print("\n" + "="*70)
    print("5-Tier Processing Test Complete!")
    print("="*70)

if __name__ == "__main__":
    test_5tier_processing()