#!/usr/bin/env python3
"""
Analyze Legacy Tab Output
=========================

This script analyzes what the Legacy tab outputs based on the 
enrollment data and configuration.
"""

import sys
import os
import pandas as pd
import json
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from enrollment_automation_v6 import (
    read_and_prepare_data,
    build_tier_data_from_source,
    load_block_aggregations,
    load_plan_mappings,
    CID_TO_TAB
)

def analyze_legacy_facilities():
    """Analyze all facilities that map to Legacy tab"""
    
    # Get all Legacy facilities from CID_TO_TAB
    legacy_facilities = {cid: tab for cid, tab in CID_TO_TAB.items() if tab == 'Legacy'}
    
    print("="*70)
    print("LEGACY TAB ANALYSIS")
    print("="*70)
    
    print(f"\nTotal facilities mapping to Legacy tab: {len(legacy_facilities)}")
    print("\nFacility IDs in Legacy tab:")
    for cid in sorted(legacy_facilities.keys()):
        print(f"  - {cid}")
    
    return legacy_facilities

def get_legacy_enrollment_data():
    """Get enrollment data for Legacy facilities"""
    
    # Load source data
    plan_mappings = load_plan_mappings()
    source_file = r"C:\Users\becas\Prime_EFR\data\input\source_data.xlsx"
    
    if not os.path.exists(source_file):
        print(f"\n⚠️  Source file not found: {source_file}")
        # Create sample data for demonstration
        sample_data = pd.DataFrame({
            'CLIENT ID': ['H3100', 'H3110', 'H3170', 'H3180', 'H3180'],
            'PLAN': ['PRIMEMMEPOLE', 'PRIMEMMVALUE', 'PRIMEMMEPOLE', 'PRIMEMMEPOLE', 'PRIMEMMEPOLE2'],
            'BEN CODE': ['EMP', 'ESP', 'ECH', 'FAM', 'EMP'],
            'tier': ['EE Only', 'EE+Spouse', 'EE+Child(ren)', 'EE+Family', 'EE Only']
        })
        return sample_data
    
    # Load and filter for Legacy facilities
    df = read_and_prepare_data(source_file, plan_mappings)
    
    # Filter for Legacy facilities
    legacy_facilities = {cid for cid, tab in CID_TO_TAB.items() if tab == 'Legacy'}
    legacy_df = df[df['CLIENT ID'].isin(legacy_facilities)] if 'CLIENT ID' in df.columns else pd.DataFrame()
    
    return legacy_df

def analyze_legacy_blocks():
    """Analyze block configuration for Legacy facilities"""
    
    print("\n" + "="*70)
    print("LEGACY BLOCK CONFIGURATION")
    print("="*70)
    
    # Load block config
    block_config = load_block_aggregations()
    
    if 'Legacy' not in block_config:
        print("\n⚠️  No Legacy configuration found in block_aggregations.json")
        return {}
    
    legacy_config = block_config['Legacy']
    
    print(f"\nConfigured Legacy facilities in blocks: {len(legacy_config)}")
    
    for client_id, config in legacy_config.items():
        if client_id.startswith('_'):
            continue
            
        print(f"\n{client_id}:")
        
        if '_comment' in config:
            print(f"  Comment: {config['_comment']}")
        
        for plan_type in ['EPO', 'VALUE']:
            if plan_type in config:
                print(f"  {plan_type}:")
                for block_label, block_def in config[plan_type].items():
                    if 'sum_of' in block_def:
                        print(f"    - {block_label}: {block_def['sum_of']}")
        
        if '_children_policy' in config:
            print(f"  Children Policy: {config['_children_policy']}")
    
    return legacy_config

def calculate_legacy_totals(df):
    """Calculate enrollment totals for Legacy tab"""
    
    print("\n" + "="*70)
    print("LEGACY ENROLLMENT TOTALS")
    print("="*70)
    
    if df.empty:
        print("\nNo Legacy enrollment data available")
        return {}
    
    # Group by tier
    if 'tier' in df.columns:
        tier_counts = df.groupby('tier').size()
        
        print("\nEnrollment by Tier:")
        total = 0
        for tier in ['EE Only', 'EE+Spouse', 'EE+Child(ren)', 'EE+Family']:
            count = tier_counts.get(tier, 0)
            total += count
            print(f"  {tier:<20}: {count:>6,}")
        
        print(f"  {'TOTAL':<20}: {total:>6,}")
        
        return tier_counts.to_dict()
    
    # Fallback to BEN CODE
    if 'BEN CODE' in df.columns:
        ben_counts = df.groupby('BEN CODE').size()
        
        print("\nEnrollment by BEN CODE:")
        total = 0
        for code in ['EMP', 'ESP', 'ECH', 'E1D', 'FAM']:
            count = ben_counts.get(code, 0)
            total += count
            if count > 0:
                print(f"  {code:<20}: {count:>6,}")
        
        print(f"  {'TOTAL':<20}: {total:>6,}")
        
        # Convert to tier format
        tier_totals = {
            'EE Only': ben_counts.get('EMP', 0),
            'EE+Spouse': ben_counts.get('ESP', 0),
            'EE+Child(ren)': ben_counts.get('ECH', 0) + ben_counts.get('E1D', 0),
            'EE+Family': ben_counts.get('FAM', 0)
        }
        
        return tier_totals
    
    return {}

def analyze_legacy_plans(df):
    """Analyze PLAN distribution in Legacy data"""
    
    print("\n" + "="*70)
    print("LEGACY PLAN DISTRIBUTION")
    print("="*70)
    
    if df.empty or 'PLAN' not in df.columns:
        print("\nNo PLAN data available")
        return
    
    # Get unique plans
    plan_counts = df.groupby('PLAN').size().sort_values(ascending=False)
    
    print(f"\nUnique PLAN codes: {len(plan_counts)}")
    print("\nTop PLAN codes:")
    for plan, count in plan_counts.head(10).items():
        print(f"  {plan:<30}: {count:>6,}")
    
    # Check for configured vs unconfigured plans
    block_config = load_block_aggregations()
    configured_plans = set()
    
    if 'Legacy' in block_config:
        for client_config in block_config['Legacy'].values():
            if isinstance(client_config, dict):
                for plan_type in ['EPO', 'VALUE']:
                    if plan_type in client_config:
                        for block in client_config[plan_type].values():
                            if 'sum_of' in block:
                                configured_plans.update(block['sum_of'])
    
    all_plans = set(plan_counts.index)
    unconfigured = all_plans - configured_plans
    
    if unconfigured:
        print(f"\n⚠️  Unconfigured PLAN codes found: {len(unconfigured)}")
        for plan in list(unconfigured)[:5]:
            count = plan_counts.get(plan, 0)
            print(f"    - {plan}: {count} enrollments")

def main():
    """Main analysis function"""
    
    print("\n" + "="*70)
    print("LEGACY TAB OUTPUT ANALYSIS")
    print("="*70)
    print("\nAnalyzing what the Legacy tab outputs...")
    
    # Step 1: Identify Legacy facilities
    legacy_facilities = analyze_legacy_facilities()
    
    # Step 2: Analyze block configuration
    legacy_blocks = analyze_legacy_blocks()
    
    # Step 3: Get enrollment data
    legacy_df = get_legacy_enrollment_data()
    
    if not legacy_df.empty:
        print(f"\nTotal Legacy enrollment records: {len(legacy_df):,}")
        
        # Step 4: Calculate totals
        tier_totals = calculate_legacy_totals(legacy_df)
        
        # Step 5: Analyze plan distribution
        analyze_legacy_plans(legacy_df)
        
        # Expected vs Actual
        print("\n" + "="*70)
        print("EXPECTED OUTPUT FOR LEGACY TAB")
        print("="*70)
        print("\nBased on the QA analysis, Legacy should output:")
        print("  EMP (EE Only)      : 3,659")
        print("  ESP (EE+Spouse)    :   611")
        print("  ECH (EE+Child(ren)): 1,006")
        print("  FAM (EE+Family)    :   757")
        print("  TOTAL              : 6,033")
        
        if tier_totals:
            print("\nCalculated from current data:")
            calc_total = sum(tier_totals.values())
            print(f"  TOTAL              : {calc_total:,}")
            
    else:
        print("\n⚠️  No Legacy enrollment data found")
        print("\nNote: The Legacy tab aggregates data from multiple facilities")
        print("including H3100-H3240 and others, but only H3170 and H3180")
        print("have explicit block configurations.")
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print("\nThe Legacy tab aggregates enrollment from ~20 facilities")
    print("but only 2 facilities (H3170, H3180) have block configurations.")
    print("This may indicate:")
    print("  1. Other Legacy facilities use default aggregation")
    print("  2. Block config may be incomplete") 
    print("  3. Some facilities may not have enrollment data")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())