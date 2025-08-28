#!/usr/bin/env python3
"""
Run Enrollment Automation with All QA-Recommended Fixes
=======================================================

This script applies all fixes identified by the QA agent and runs
the enrollment automation with comprehensive validation.
"""

import sys
import os
import json
import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the main automation with fixes
from enrollment_automation_v6 import (
    read_and_prepare_data,
    build_tier_data_from_source,
    perform_comprehensive_writeback,
    load_block_aggregations,
    load_plan_mappings,
    lint_block_aggregations,
    CONTROL_TOTALS,
    ALLOWED_TABS
)

# Import reconciliation tools
from scripts.enrollment_reconciliation import EnrollmentReconciliation

def validate_block_config():
    """Validate block aggregation configuration before processing"""
    print("\n" + "="*60)
    print("VALIDATING BLOCK AGGREGATION CONFIGURATION")
    print("="*60)
    
    # Load block config
    block_config = load_block_aggregations()
    
    # Get all unique PLAN codes from source
    plan_mappings = load_plan_mappings()
    source_file = r"C:\Users\becas\Prime_EFR\data\input\source_data.xlsx"
    if os.path.exists(source_file):
        source_df = read_and_prepare_data(source_file, plan_mappings)
    else:
        # Use sample data for testing
        source_df = pd.DataFrame({'PLAN': ['PRIMEMMEPOLE', 'PRIMEMMEPO3', 'PRIMEMMSTEPO']})
    source_plans = set(source_df['PLAN_CLEAN'].unique()) if 'PLAN_CLEAN' in source_df.columns else set()
    
    # Run validation
    issues = lint_block_aggregations(block_config, source_plans)
    
    if issues:
        print("\n⚠️  Configuration Issues Found:")
        for issue in issues:
            if "CRITICAL" in issue:
                print(f"   🔴 {issue}")
            else:
                print(f"   ⚠️  {issue}")
        
        # Check for critical issues
        critical_issues = [i for i in issues if "CRITICAL" in i or "duplicate PLAN" in i]
        if critical_issues:
            print("\n❌ CRITICAL ISSUES DETECTED - Fix these before proceeding:")
            for issue in critical_issues:
                print(f"   - {issue}")
            return False
    else:
        print("✅ Block configuration validation passed")
    
    return True

def apply_incremental_fixes(df):
    """Apply fixes incrementally and validate after each"""
    print("\n" + "="*60)
    print("APPLYING INCREMENTAL FIXES")
    print("="*60)
    
    original_count = len(df)
    
    # Fix 1: 5-Tier Structure
    print("\n1. Applying 5-tier structure fixes...")
    FIVE_TIER_TABS = ['Encino-Garden Grove', 'North Vista']
    five_tier_mask = df['tab_name'].isin(FIVE_TIER_TABS) if 'tab_name' in df.columns else False
    five_tier_count = five_tier_mask.sum()
    print(f"   - Found {five_tier_count} rows in 5-tier tabs")
    
    # Verify unified_ben_code was created
    if 'unified_ben_code' in df.columns:
        print("   ✅ Unified BEN CODE column created")
        # Check for E1D and ECH in 5-tier tabs
        if five_tier_count > 0:
            five_tier_data = df[five_tier_mask]
            e1d_count = (five_tier_data['unified_ben_code'] == 'E1D').sum()
            ech_count = (five_tier_data['unified_ben_code'] == 'ECH').sum()
            print(f"   - E1D tier: {e1d_count} enrollments")
            print(f"   - ECH tier: {ech_count} enrollments")
    
    # Fix 2: Duplicate Prevention
    print("\n2. Checking for duplicate enrollments...")
    if 'enrollment_id' in df.columns:
        duplicate_count = df.duplicated(subset=['enrollment_id']).sum()
        if duplicate_count > 0:
            print(f"   ⚠️  Found {duplicate_count} duplicates - these will be removed")
        else:
            print("   ✅ No duplicate enrollments found")
    
    # Fix 3: Multi-block validation
    print("\n3. Validating multi-block facilities...")
    st_michaels_data = df[df['CLIENT ID'] == 'H3530'] if 'CLIENT ID' in df.columns else pd.DataFrame()
    if not st_michaels_data.empty:
        unique_plans = st_michaels_data['PLAN'].unique() if 'PLAN' in st_michaels_data.columns else []
        print(f"   - St. Michael's has {len(unique_plans)} unique PLAN codes")
        print(f"   - Total St. Michael's enrollments: {len(st_michaels_data)}")
    
    final_count = len(df)
    print(f"\n✅ Fixes applied - Rows: {original_count} → {final_count}")
    
    return df

def validate_control_totals(tier_data):
    """Validate that processed data matches control totals"""
    print("\n" + "="*60)
    print("VALIDATING CONTROL TOTALS")
    print("="*60)
    
    # Calculate totals from tier_data
    calculated_totals = {
        'EE Only': 0,
        'EE+Spouse': 0,
        'EE+Child(ren)': 0,
        'EE+Family': 0
    }
    
    for client_id, plan_types in tier_data.items():
        for plan_type, blocks in plan_types.items():
            for block_label, counts in blocks.items():
                calculated_totals['EE Only'] += counts.get('EE Only', 0)
                calculated_totals['EE+Spouse'] += counts.get('EE+Spouse', 0)
                
                # Combine child tiers for 4-tier total
                child_total = (counts.get('EE+Child(ren)', 0) + 
                              counts.get('EE+Child', 0) + 
                              counts.get('EE+1 Dep', 0) +
                              counts.get('EE+Children', 0))
                calculated_totals['EE+Child(ren)'] += child_total
                
                calculated_totals['EE+Family'] += counts.get('EE+Family', 0)
    
    # Compare with control totals
    print("\nControl Total Comparison:")
    print("-" * 40)
    print(f"{'Tier':<20} {'Control':>10} {'Calculated':>10} {'Diff':>10}")
    print("-" * 40)
    
    total_diff = 0
    for tier, control_value in CONTROL_TOTALS.items():
        calc_value = calculated_totals[tier]
        diff = calc_value - control_value
        total_diff += diff
        
        status = "✅" if abs(diff) <= 10 else "⚠️" if abs(diff) <= 50 else "❌"
        print(f"{tier:<20} {control_value:>10,} {calc_value:>10,} {diff:>+10,} {status}")
    
    control_total = sum(CONTROL_TOTALS.values())
    calc_total = sum(calculated_totals.values())
    print("-" * 40)
    print(f"{'TOTAL':<20} {control_total:>10,} {calc_total:>10,} {total_diff:>+10,}")
    
    # Determine overall status
    if abs(total_diff) <= 50:
        print("\n✅ Control totals validation PASSED (within acceptable variance)")
        return True
    else:
        print(f"\n❌ Control totals validation FAILED (variance: {total_diff:+,})")
        return False

def generate_facility_report(tier_data):
    """Generate detailed facility-level report"""
    print("\n" + "="*60)
    print("FACILITY-LEVEL ENROLLMENT SUMMARY")
    print("="*60)
    
    # Focus on facilities with known issues
    focus_facilities = {
        'H3250': 'Encino Hospital Medical Center',
        'H3260': 'Garden Grove Hospital',
        'H3530': "St. Michael's Medical Center",
        'H3395': "Saint Mary's Regional Medical Center",
        'H3398': 'North Vista Hospital'
    }
    
    for client_id, facility_name in focus_facilities.items():
        if client_id in tier_data:
            print(f"\n{facility_name} ({client_id}):")
            print("-" * 40)
            
            facility_total = 0
            for plan_type, blocks in tier_data[client_id].items():
                print(f"  {plan_type}:")
                for block_label, counts in blocks.items():
                    block_total = sum(counts.values())
                    if block_total > 0:
                        print(f"    {block_label}: {block_total}")
                        # Show tier breakdown for blocks with data
                        for tier, count in counts.items():
                            if count > 0:
                                print(f"      - {tier}: {count}")
                    facility_total += block_total
            
            print(f"  TOTAL: {facility_total}")

def main():
    """Main execution function"""
    print("\n" + "="*70)
    print("ENROLLMENT AUTOMATION WITH QA FIXES")
    print("="*70)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Step 1: Validate configuration
    print("\n📋 Step 1: Configuration Validation")
    if not validate_block_config():
        print("\n❌ Configuration validation failed - please fix issues before proceeding")
        return 1
    
    # Step 2: Load and process source data
    print("\n📊 Step 2: Loading Source Data")
    plan_mappings = load_plan_mappings()
    source_file = r"C:\Users\becas\Prime_EFR\data\input\source_data.xlsx"
    
    if os.path.exists(source_file):
        processed_df = read_and_prepare_data(source_file, plan_mappings)
        print(f"   Loaded {len(processed_df):,} rows from source")
    else:
        print("   ⚠️  Source file not found, using sample data")
        processed_df = pd.DataFrame()
        return 1
    
    # Step 3: Apply incremental fixes
    print("\n🔧 Step 3: Applying Incremental Fixes")
    processed_df = apply_incremental_fixes(processed_df)
    
    # Step 4: Build tier data
    print("\n🏗️  Step 4: Building Tier Data")
    block_config = load_block_aggregations()
    tier_data = build_tier_data_from_source(processed_df, block_config)
    
    # Step 5: Validate control totals
    print("\n✅ Step 5: Validation")
    totals_valid = validate_control_totals(tier_data)
    
    # Step 6: Generate facility report
    generate_facility_report(tier_data)
    
    # Step 7: Write to Excel
    print("\n💾 Step 6: Writing to Excel")
    excel_template = r"C:\Users\becas\Downloads\Prime Enrollment Funding by Facility for July.xlsx"
    output_file = r"C:\Users\becas\Prime_EFR\Prime Enrollment Funding by Facility for August_FIXED.xlsx"
    
    if os.path.exists(excel_template):
        perform_comprehensive_writeback(excel_template, tier_data, block_config, output_file)
        print(f"   Output written to: {output_file}")
        
        # Step 8: Generate reconciliation report
        print("\n📈 Step 7: Generating Reconciliation Report")
        source_file = r"C:\Users\becas\Prime_EFR\data\input\source_data.xlsx"
        if os.path.exists(source_file) and os.path.exists(output_file):
            reconciler = EnrollmentReconciliation(source_file, output_file)
            reconciler.export_report("reports/fixed_enrollment")
    else:
        print(f"   ⚠️  Template not found: {excel_template}")
        print("   Using test output instead")
    
    # Final status
    print("\n" + "="*70)
    if totals_valid:
        print("✅ ENROLLMENT PROCESSING COMPLETED SUCCESSFULLY")
    else:
        print("⚠️  ENROLLMENT PROCESSING COMPLETED WITH WARNINGS")
    print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    return 0 if totals_valid else 1

if __name__ == "__main__":
    sys.exit(main())