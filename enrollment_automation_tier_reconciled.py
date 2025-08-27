""" 
=================================================================================
ENROLLMENT AUTOMATION - TIER RECONCILIATION VERSION
=================================================================================

This version includes:
- Control totals harness for exact tier matching
- Waterfall tracking to find where 106 rows go missing
- Fixed tier normalization (no defaulting to EE)
- Comprehensive unknown auditing
- Global integrity assertions

Control Totals (Ground Truth):
- EMP (EE Only): 14,533
- ESP (EE+Spouse): 2,639
- ECH (EE+Child(ren)): 4,413
- FAM (EE+Family): 3,123
TOTAL: 24,708
"""

import pandas as pd
import numpy as np
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
import warnings
import traceback
import os
from difflib import SequenceMatcher
from collections import Counter
warnings.filterwarnings('ignore')

# CONTROL TOTALS - GROUND TRUTH
CONTROL_TOTALS = {
    "EE Only": 14533,
    "EE+Spouse": 2639,
    "EE+Child(ren)": 4413,
    "EE+Family": 3123
}
TIER_ORDER = ["EE Only", "EE+Spouse", "EE+Child(ren)", "EE+Family"]
CONTROL_TOTAL = sum(CONTROL_TOTALS.values())  # 24,708

# Waterfall tracking
waterfall_stages = []
unknown_tiers_tracker = Counter()
removed_rows_samples = {}

def log_stage(stage_name, df, prev_df=None):
    """
    Log a stage in the waterfall with tier counts and row samples
    """
    global waterfall_stages, removed_rows_samples
    
    # Get tier distribution
    tier_counts = {}
    if 'tier' in df.columns:
        tier_dist = df['tier'].value_counts()
        for tier in TIER_ORDER:
            tier_counts[tier] = tier_dist.get(tier, 0)
        tier_counts['UNKNOWN'] = tier_dist.get('UNKNOWN', 0)
        tier_counts['Other'] = len(df) - sum(tier_counts.values())
    else:
        tier_counts = {tier: 0 for tier in TIER_ORDER}
        tier_counts['UNKNOWN'] = 0
        tier_counts['Other'] = len(df)
    
    # Calculate delta to control
    delta = sum(tier_counts.get(tier, 0) for tier in TIER_ORDER) - CONTROL_TOTAL
    
    # Store stage info
    stage_info = {
        'stage': stage_name,
        'total_rows': len(df),
        'tier_counts': tier_counts,
        'delta_to_control': delta
    }
    waterfall_stages.append(stage_info)
    
    # Capture removed rows if prev_df provided
    if prev_df is not None and len(prev_df) > len(df):
        # Find removed rows
        if 'index' in prev_df.columns and 'index' in df.columns:
            removed_idx = set(prev_df['index']) - set(df['index'])
        else:
            # Use other identifying columns
            if all(col in prev_df.columns and col in df.columns for col in ['CLIENT ID', 'EMPLOYEE NAME']):
                prev_keys = set(zip(prev_df['CLIENT ID'], prev_df['EMPLOYEE NAME']))
                curr_keys = set(zip(df['CLIENT ID'], df['EMPLOYEE NAME']))
                removed_keys = prev_keys - curr_keys
                removed_idx = prev_df[prev_df.apply(lambda x: (x['CLIENT ID'], x['EMPLOYEE NAME']) in removed_keys, axis=1)].index
            else:
                removed_idx = []
        
        if len(removed_idx) > 0:
            sample_cols = ['CLIENT ID', 'RELATION', 'STATUS', 'PLAN', 'BEN CODE']
            sample_cols = [col for col in sample_cols if col in prev_df.columns]
            if sample_cols:
                removed_sample = prev_df.loc[list(removed_idx)[:10], sample_cols] if len(removed_idx) <= 10 else prev_df.loc[list(removed_idx)[:10], sample_cols]
                removed_rows_samples[stage_name] = removed_sample
    
    # Print stage summary
    print(f"\n--- Stage: {stage_name} ---")
    print(f"Total rows: {len(df):,}")
    if tier_counts:
        print(f"Tier distribution: EE Only={tier_counts.get('EE Only', 0):,}, "
              f"EE+Spouse={tier_counts.get('EE+Spouse', 0):,}, "
              f"EE+Child(ren)={tier_counts.get('EE+Child(ren)', 0):,}, "
              f"EE+Family={tier_counts.get('EE+Family', 0):,}, "
              f"UNKNOWN={tier_counts.get('UNKNOWN', 0):,}")
    print(f"Delta to control: {delta:+,}")
    
    return df

def print_waterfall_table():
    """
    Print the waterfall table showing row movement through stages
    """
    print("\n" + "="*120)
    print("WATERFALL ANALYSIS - Row Movement Through Pipeline")
    print("="*120)
    
    headers = ['Stage', 'Total', 'EE Only', 'EE+Spouse', 'EE+Child(ren)', 'EE+Family', 'UNKNOWN', 'Delta', 'Row Δ']
    print(f"{headers[0]:<20} {headers[1]:>8} {headers[2]:>8} {headers[3]:>10} {headers[4]:>12} {headers[5]:>10} {headers[6]:>8} {headers[7]:>8} {headers[8]:>8}")
    print("-"*120)
    
    prev_total = 0
    for i, stage in enumerate(waterfall_stages):
        row_delta = stage['total_rows'] - prev_total if i > 0 else 0
        tier_counts = stage['tier_counts']
        
        print(f"{stage['stage']:<20} "
              f"{stage['total_rows']:>8,} "
              f"{tier_counts.get('EE Only', 0):>8,} "
              f"{tier_counts.get('EE+Spouse', 0):>10,} "
              f"{tier_counts.get('EE+Child(ren)', 0):>12,} "
              f"{tier_counts.get('EE+Family', 0):>10,} "
              f"{tier_counts.get('UNKNOWN', 0):>8,} "
              f"{stage['delta_to_control']:>+8,} "
              f"{row_delta:>+8,}")
        
        prev_total = stage['total_rows']
    
    print("="*120)

def clean_key(s):
    """Clean and normalize keys for matching - handles trailing spaces"""
    if pd.isna(s):
        return ''
    # Strip, uppercase, and collapse all whitespace (including internal)
    return ' '.join(str(s).strip().upper().split())

def is_active(status):
    """Flexible active status check - includes A (Active) and C (COBRA/Continued)"""
    if pd.isna(status):
        return False
    s = str(status).strip().upper()
    # Include both A (Active) and C (COBRA/Continued coverage)
    return s in ['A', 'ACTIVE', 'ACT', 'C', 'COBRA', 'CONTINUED'] or s.startswith('A')

def is_subscriber(relation):
    """Flexible subscriber check"""
    if pd.isna(relation):
        return False
    r = str(relation).strip().upper()
    return r in ['SELF', 'EE', 'EMPLOYEE', 'SUBSCRIBER', 'S', 'EMP']

def normalize_tier_strict(raw_tier):
    """
    Strictly normalize raw tier text - NEVER default to EE
    Returns one of: 'EE Only', 'EE+Spouse', 'EE+Child(ren)', 'EE+Family', or 'UNKNOWN'
    """
    global unknown_tiers_tracker
    
    if pd.isna(raw_tier):
        unknown_tiers_tracker['<NaN>'] += 1
        return 'UNKNOWN'
    
    # Clean the input thoroughly - handle trailing spaces
    tier_str = str(raw_tier).strip().upper()
    
    # Normalize separators consistently
    for sep in ['&', '+', '/', ' AND ', '  ']:
        tier_str = tier_str.replace(sep, ' ')
    
    # Collapse multiple spaces to single space
    tier_str = ' '.join(tier_str.split())
    
    # Employee Only variants (expanded)
    ee_only_variants = [
        'EMP', 'EE', 'EMPLOYEE ONLY', 'EE ONLY', 'EMPLOYEE', 'E',
        'SELF ONLY', 'SELF', 'SUBSCRIBER ONLY', 'SUBSCRIBER',
        'EMP ONLY', 'E ONLY', 'EMPLOYEE'
    ]
    if tier_str in ee_only_variants:
        return 'EE Only'
    
    # Employee + Spouse variants (expanded)
    spouse_variants = [
        'ESP', 'EE SPOUSE', 'EMPLOYEE SPOUSE', 'EE SPOUSE',
        'EMPLOYEE SPOUSE', 'ES', 'E S', 'E SPOUSE',
        'EMP SPOUSE', 'EMP SP', 'EMPLOYEE SP', 'EE SP'
    ]
    if tier_str in spouse_variants:
        return 'EE+Spouse'
    
    # Employee + Child(ren) variants (expanded to handle both)
    child_variants = [
        'ECH', 'E1D', 'EE CHILD', 'EMPLOYEE CHILD', 'EE CHILDREN',
        'EMPLOYEE CHILDREN', 'EE CHILD', 'EE 1 CHILD', 'EE 1 DEPENDENT',
        'EC', 'E C', 'E CHILD', 'E CHILDREN', 'EMP CHILD', 'EMP CHILDREN',
        'CHILD', 'CHILDREN', 'EE CHILD REN', 'CHILD REN', 'E1C', 'E2C',
        'EE 1 DEP', 'EE DEP', 'EE DEPS', 'EMPLOYEE CHILDREN',
        'EE 1', 'EE 2'  # Sometimes just numbers after EE
    ]
    if tier_str in child_variants:
        return 'EE+Child(ren)'
    
    # Employee + Family variants (expanded)
    family_variants = [
        'FAM', 'FAMILY', 'EE FAMILY', 'EMPLOYEE FAMILY',
        'EF', 'E F', 'E FAMILY', 'EMP FAMILY', 'EMP FAM',
        'EMPLOYEE FAM', 'EE FAM'
    ]
    if tier_str in family_variants:
        return 'EE+Family'
    
    # Track unknown tier
    unknown_tiers_tracker[tier_str] += 1
    return 'UNKNOWN'

def fuzzy_match_score(s1, s2):
    """Calculate fuzzy match score between two strings"""
    if pd.isna(s1) or pd.isna(s2):
        return 0.0
    
    str1 = str(s1).lower().strip()
    str2 = str(s2).lower().strip()
    
    # Handle the specific "a" vs "at" case
    str1 = str1.replace(" a st.", " at st.")
    str2 = str2.replace(" a st.", " at st.")
    
    # Remove punctuation
    for char in ".,'-&":
        str1 = str1.replace(char, " ")
        str2 = str2.replace(char, " ")
    
    str1 = " ".join(str1.split())
    str2 = " ".join(str2.split())
    
    return SequenceMatcher(None, str1, str2).ratio()

# Copy all the facility mappings from the reconciled version
TPA_TO_FACILITY = {
    'H3100': 'Chino Valley Medical Center',
    'H3105': 'Glendora Community Hospital',
    'H3110': 'Prime Management',
    'H3115': 'Premiere Healthcare Staffing, LLC',
    'H3120': 'Hospital Business Service',
    'H3130': 'Bio Med Services',
    'H3140': 'Desert Valley Hospital',
    'H3150': 'Desert Valley Medical Group',
    'H3160': 'Montclair',
    'H3170': 'San Dimas',
    'H3180': 'Sherman Oaks',
    'H3190': 'Sherman Oaks Med. Group',
    'H3200': 'La Palma',
    'H3210': 'Huntington Beach',
    'H3220': 'West Anaheim',
    'H3230': 'Paradise Valley',
    'H3240': 'Paradise Valley Medical Grp',
    'H3250': 'Encino Hospital',
    'H3260': 'Garden Grove',
    'H3270': 'Centinela',
    'H3271': 'Robotics Outpatient Center',
    'H3272': 'Centinela Valley Endoscopy Center',
    'H3275': 'St. Francis Medical Center',
    'H3276': 'Shoreline Surgery Center',
    'H3277': "Physician's Surgery Center Downey",
    'H3280': 'Shasta Regional Medical Center',
    'H3285': 'Shasta Medical Group',
    'H3290': 'Hospitality',
    'H3300': "Chino RN's",
    'H3310': 'Alvarado Hospital',
    'H3320': 'Pampa',
    'H3325': 'Roxborough',
    'H3330': 'Lower Bucks',
    'H3335': 'Dallas Medical Center',
    'H3337': 'Dallas Regional Medical Center',
    'H3338': 'Riverview Regional Medical Center',
    'H3339': 'Gadsden Physicians Management',
    'H3340': 'Providence Medical Center',
    'H3345': 'St. John Hospital',
    'H3350': 'Providence Place, Inc.',
    'H3355': 'Knapp Medical Center',
    'H3360': 'Knapp Medical Group',
    'H3365': 'Knapp Ambulatory Surgery Center',
    'H3370': 'Harlingen Medical Center',
    'H3375': 'Garden City Hospital',
    'H3380': 'United Home Health Services',
    'H3381': 'Lake Huron Medical Center',
    'H3382': 'Lake Huron Medical Group',
    'H3385': 'Prime Garden City Medical Group',
    'H3390': 'Rehabilitation Hospital of Rhode Island',
    'H3392': 'Landmark Medical Center',
    'H3394': "Summit Surgery Center at St. Mary's Galena",
    'H3395': "St. Mary's Regional Medical Center",
    'H3396': "St. Mary's Medical Group",
    'H3397': 'Monroe Hospital',
    'H3398': 'North Vista Hospital',
    'H3399': 'North Vista Medical Group',
    'H3400': "St. Mary's Fitness Center",
    'H3500': "St Clare's Health System",
    'H3505': "Saint Mary's General Hospital",
    'H3510': 'Southern Medical Regional Center',
    'H3520': 'Lehigh Regional Medical Center',
    'H3530': "St. Michael's Medical Center",
    'H3540': 'Mission Regional Medical Center',
    'H3560': "St. Mary's Medical Center",
    'H3561': 'St. Joseph Medical Center',
    'H3562': 'South Kansas City Surgi Center',
    'H3563': 'CHCS Home Health Care',
    'H3564': 'CPCN Physicians Service',
    'H3565': 'CPCN Physicians Service (32) STJ',
    'H3566': "St. Mary's Surgical Center",
    'H3591': 'Coshocton County Memorial Hospital',
    'H3592': 'East Liverpool City Hospital',
    'H3593': 'Ohio Valley Home Health Care',
    'H3594': 'Ohio Valley Home Health Services',
    'H3595': 'River Valley Physicians',
    'H3598': 'Suburban Community Hospital',
    'H3599': 'Suburban Medical Group',
    'H3600': 'Reddy Development LLC',
    'H3605': 'Mercy Medical Center - Aurora LLC',
    'H3615': 'Resurrection Medical Center - Chicago LLC',
    'H3625': 'Saint Francis Hospital - Evanston LLC',
    'H3630': 'Saint Joseph Hospital - Elgin LLC',
    'H3635': 'Saint Joseph Hospital - Joliet LLC',
    'H3645': "St. Mary's Hospital - Kankakee, LLC",
    'H3655': 'Saint Mary of Nazareth Hospital - Chicago, LLC',
    'H3660': 'Holy Family Medical Center - Des Plaines LLC',
    'H3665': 'MedSpace Services, LLC',
    'H3670': 'Prime Healthcare Illinois Medical Group, LLC',
    'H3675': 'Prime Healthcare Home Care and Hospice',
    'H3680': 'Prime Healthcare Senior Living'
}

# Simplified FACILITY_MAPPING - we'll focus on processing all facilities
FACILITY_MAPPING = {
    'All': TPA_TO_FACILITY  # Process all facilities together for tier reconciliation
}

# Keep the plan mappings
PLAN_TO_TYPE = {
    'PRIMESFSE': 'EPO', 'PRIMESFUN': 'EPO', 'PRIMEMSFE': 'EPO',
    'PRIMEMMLMRI': 'VALUE', 'PRIMEMMCV': 'EPO', 'PRIMEMMGLN': 'EPO',
    'PRIMEMMEPOLE2': 'EPO', 'PRIMEMMWA': 'EPO', 'PRIMEMMCC': 'EPO',
    'PRIMEMMDAL': 'EPO', 'PRIMEMMEL': 'EPO', 'PRIMEMMELPOS': 'PPO',
    # ... (include all plan mappings from original)
}

def infer_plan_group_and_variant(plan_raw, mapping=PLAN_TO_TYPE):
    """
    Infer plan group and variant
    """
    if pd.isna(plan_raw):
        return 'UNKNOWN', 'UNKNOWN'
    
    plan_clean = clean_key(plan_raw)
    
    # Try mapping first
    if plan_clean in mapping:
        return mapping[plan_clean], plan_clean
    
    # Heuristic fallback
    if 'PPO' in plan_clean:
        return 'PPO', plan_clean
    elif 'EPO' in plan_clean:
        return 'EPO', plan_clean
    elif 'VAL' in plan_clean or 'VALUE' in plan_clean:
        return 'VALUE', plan_clean
    
    return 'UNKNOWN', plan_clean

def read_and_prepare_data_with_waterfall(file_path):
    """
    Read source data with waterfall tracking
    """
    # Stage 1: Read raw
    df = pd.read_excel(file_path, sheet_name=0)
    df['original_index'] = df.index  # Track original rows
    df = log_stage('read_raw', df)
    
    # Stage 2: Clean keys
    if 'CLIENT ID' in df.columns:
        df['CLIENT ID'] = df['CLIENT ID'].apply(clean_key)
    if 'BEN CODE' in df.columns:
        # Clean BEN CODE to handle trailing spaces
        df['BEN CODE'] = df['BEN CODE'].apply(clean_key)
    df = log_stage('clean_keys', df)
    
    # Stage 3: Status filter (flexible)
    prev_df = df.copy()
    if 'STATUS' in df.columns:
        df['is_active'] = df['STATUS'].apply(is_active)
        df = df[df['is_active']].copy()
    df = log_stage('status_filter', df, prev_df)
    
    # Stage 4: Relation filter (flexible)
    prev_df = df.copy()
    if 'RELATION' in df.columns:
        df['is_subscriber'] = df['RELATION'].apply(is_subscriber)
        df = df[df['is_subscriber']].copy()
    df = log_stage('relation_filter', df, prev_df)
    
    # Stage 5: Facility mapping (keep unknowns)
    if 'CLIENT ID' in df.columns:
        df['facility_id'] = df['CLIENT ID']
        df['facility_name'] = df['facility_id'].map(TPA_TO_FACILITY)
        df['facility_name'] = df['facility_name'].fillna('UNKNOWN')
    df = log_stage('facility_map', df)
    
    # Stage 6: Tier normalization (strict)
    if 'BEN CODE' in df.columns:
        df['tier'] = df['BEN CODE'].apply(normalize_tier_strict)
    else:
        df['tier'] = 'UNKNOWN'
    df = log_stage('tier_normalized', df)
    
    # Stage 7: Plan grouping
    if 'PLAN' in df.columns:
        df[['plan_group', 'plan_variant']] = df['PLAN'].apply(
            lambda x: pd.Series(infer_plan_group_and_variant(x))
        )
    else:
        df['plan_group'] = 'UNKNOWN'
        df['plan_variant'] = 'UNKNOWN'
    df = log_stage('plan_grouped', df)
    
    # Stage 8: Pre-pivot
    df = log_stage('pre_pivot', df)
    
    return df

def print_unknown_audit():
    """
    Print audit of unknown tiers
    """
    print("\n" + "="*80)
    print("UNKNOWN TIERS AUDIT")
    print("="*80)
    
    if unknown_tiers_tracker:
        print(f"\nTotal unique unknown tier values: {len(unknown_tiers_tracker)}")
        print(f"Total unknown tier rows: {sum(unknown_tiers_tracker.values())}")
        print("\nTop 20 unknown tier values:")
        for tier_val, count in unknown_tiers_tracker.most_common(20):
            print(f"  '{tier_val}': {count}")
    else:
        print("No unknown tiers found!")
    
    print("="*80)

def assert_control_totals(df):
    """
    Assert that final totals match control exactly
    """
    print("\n" + "="*80)
    print("CONTROL TOTALS ASSERTION")
    print("="*80)
    
    # Get actual totals
    actual = {}
    if 'tier' in df.columns:
        tier_counts = df['tier'].value_counts()
        for tier in TIER_ORDER:
            actual[tier] = tier_counts.get(tier, 0)
    
    # Compare to control
    print("\n{:<20} {:>10} {:>10} {:>10}".format("Tier", "Control", "Actual", "Delta"))
    print("-"*60)
    
    all_match = True
    for tier in TIER_ORDER:
        control = CONTROL_TOTALS[tier]
        actual_count = actual.get(tier, 0)
        delta = actual_count - control
        status = "✓" if delta == 0 else "✗"
        print(f"{tier:<20} {control:>10,} {actual_count:>10,} {delta:>+10,} {status}")
        if delta != 0:
            all_match = False
    
    print("-"*60)
    total_control = sum(CONTROL_TOTALS.values())
    total_actual = sum(actual.get(tier, 0) for tier in TIER_ORDER)
    total_delta = total_actual - total_control
    status = "✓" if total_delta == 0 else "✗"
    print(f"{'TOTAL':<20} {total_control:>10,} {total_actual:>10,} {total_delta:>+10,} {status}")
    
    # Check for unknowns
    unknown_count = tier_counts.get('UNKNOWN', 0) if 'tier' in df.columns else 0
    if unknown_count > 0:
        print(f"\n⚠️ WARNING: {unknown_count} rows with UNKNOWN tier!")
    
    if all_match and unknown_count == 0:
        print("\n✓ Control tie-out PASS: 14533 / 2639 / 4413 / 3123. Global delta resolved (Δ=0).")
    else:
        print(f"\n✗ Control tie-out FAILED: Delta = {total_delta:+,}")
        if unknown_count > 0:
            print(f"   {unknown_count} UNKNOWN tiers need to be resolved")
    
    return all_match

def print_facility_comparison(df, facility_id, facility_name):
    """
    Print before/after comparison for a specific facility
    """
    if 'CLIENT ID' not in df.columns or 'tier' not in df.columns:
        return
    
    facility_data = df[df['CLIENT ID'] == facility_id]
    if facility_data.empty:
        print(f"\n{facility_name} ({facility_id}): No data found")
        return
    
    tier_counts = facility_data['tier'].value_counts()
    print(f"\n{facility_name} ({facility_id}):")
    for tier in TIER_ORDER:
        count = tier_counts.get(tier, 0)
        if count > 0:
            print(f"  {tier}: {count}")
    unknown = tier_counts.get('UNKNOWN', 0)
    if unknown > 0:
        print(f"  UNKNOWN: {unknown}")

def main():
    """
    Main execution with tier reconciliation
    """
    # FILE PATHS
    source_file = r"C:\Users\becas\Prime_EFR\data\input\source_data.xlsx"
    destination_file = r"C:\Users\becas\Prime_EFR\data\input\Prime Enrollment Funding by Facility for August.xlsx"
    
    try:
        print("="*80)
        print("ENROLLMENT AUTOMATION - TIER RECONCILIATION")
        print("Finding and fixing 106-row discrepancy")
        print("="*80)
        
        print("\nCONTROL TOTALS (Ground Truth):")
        for tier in TIER_ORDER:
            print(f"  {tier}: {CONTROL_TOTALS[tier]:,}")
        print(f"  TOTAL: {CONTROL_TOTAL:,}")
        
        # Process with waterfall tracking
        print("\n" + "="*80)
        print("PROCESSING WITH WATERFALL TRACKING")
        print("="*80)
        
        df = read_and_prepare_data_with_waterfall(source_file)
        
        # Print waterfall analysis
        print_waterfall_table()
        
        # Print removed rows samples
        if removed_rows_samples:
            print("\n" + "="*80)
            print("REMOVED ROWS SAMPLES")
            print("="*80)
            for stage, sample in removed_rows_samples.items():
                print(f"\n{stage} - Sample of removed rows:")
                print(sample.to_string())
        
        # Print unknown audit
        print_unknown_audit()
        
        # Print facility comparisons
        print("\n" + "="*80)
        print("FACILITY SPOT CHECKS")
        print("="*80)
        print_facility_comparison(df, 'H3170', 'San Dimas')
        print_facility_comparison(df, 'H3220', 'West Anaheim')
        
        # Assert control totals
        all_match = assert_control_totals(df)
        
        # Final summary
        print("\n" + "="*80)
        print("FINAL SUMMARY")
        print("="*80)
        
        if all_match:
            print("✅ SUCCESS: All 106 missing rows identified and recovered!")
            print("✅ Tier totals now match control exactly")
            print("✅ Control tie-out PASS: 14533 / 2639 / 4413 / 3123. Global delta resolved (Δ=0).")
        else:
            print("⚠️ RECONCILIATION IN PROGRESS")
            print("Review the waterfall and unknown audit to identify remaining issues")
        
        # Save diagnostic output
        output_file = r"C:\Users\becas\Prime_EFR\output\tier_reconciliation_report.csv"
        df.to_csv(output_file, index=False)
        print(f"\nDiagnostic data saved to: {output_file}")
        
        # Create summary pivot for destination file
        print(f"\nCreating enrollment summary...")
        summary_pivot = df.pivot_table(
            index=['facility_name', 'plan_group'],
            columns='tier',
            values='original_index',
            aggfunc='count',
            fill_value=0
        ).reset_index()
        
        # Add total column
        tier_cols = [col for col in summary_pivot.columns if col in TIER_ORDER]
        if tier_cols:
            summary_pivot['Total'] = summary_pivot[tier_cols].sum(axis=1)
        
        # Save to destination Excel file (overwrite)
        print(f"Writing to destination file: {destination_file}")
        with pd.ExcelWriter(destination_file, engine='openpyxl', mode='w') as writer:
            # Write main summary
            summary_pivot.to_excel(writer, sheet_name='Enrollment Summary', index=False)
            
            # Write detailed data
            df.to_excel(writer, sheet_name='Detailed Data', index=False)
            
            # Write control totals validation
            control_df = pd.DataFrame({
                'Tier': TIER_ORDER,
                'Control Total': [CONTROL_TOTALS[tier] for tier in TIER_ORDER],
                'Actual Total': [len(df[df['tier'] == tier]) for tier in TIER_ORDER]
            })
            control_df['Match'] = control_df['Control Total'] == control_df['Actual Total']
            control_df.to_excel(writer, sheet_name='Control Validation', index=False)
        
        print(f"✅ Destination file successfully overwritten: {destination_file}")
        
    except FileNotFoundError as e:
        print(f"\n❌ ERROR: File not found - {e}")
        print(f"Please ensure source file exists: {source_file}")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()