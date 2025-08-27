""" 
=================================================================================
ENROLLMENT AUTOMATION SCRIPT - Fixed Version for Tier Normalization
=================================================================================

This version fixes the tier collapse bug and adds proper normalization.
Key changes:
- Direct tier normalization from raw BEN CODE data
- Plan variant tracking
- Integrity checks
- Two pivot outputs (variant-level and grouped)
"""

import pandas as pd
import numpy as np
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
import warnings
import traceback
import os
warnings.filterwarnings('ignore')

# FACILITY MAPPINGS (keeping existing)
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
    'H3394': "Summit Surgery Center a St. Mary's Galena",
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

# PLAN TYPE MAPPING (keeping existing)
PLAN_TO_TYPE = {
    'PRIMESFSE': 'EPO',
    'PRIMESFUN': 'EPO',
    'PRIMEMSFE': 'EPO',
    'PRIMEMMLMRI': 'VALUE',
    'PRIMEMMCV': 'EPO',
    'PRIMEMMGLN': 'EPO',
    'PRIMEMMEPOLE2': 'EPO',
    'PRIMEMMWA': 'EPO',
    'PRIMEMMCC': 'EPO',
    'PRIMEMMDAL': 'EPO',
    'PRIMEMMEL': 'EPO',
    'PRIMEMMELPOS': 'PPO',
    'PRIMEMMEPOCEN': 'EPO',
    'PRIMEMMEPOEA': 'EPO',
    'PRIMEMMEPOES': 'EPO',
    'PRIMEMMEPOLE': 'EPO',
    'PRIMEMMEPOPA': 'EPO',
    'PRIMEMMEPOROX': 'EPO',
    'PRIMEMMEPOUEE': 'EPO',
    'PRIMEMMGCH': 'EPO',
    'PRIMEMMHAR': 'EPO',
    'PRIMEMMKN': 'EPO',
    'PRIMEMMKNVAL': 'VALUE',
    'PRIMEMMKS': 'EPO',
    'PRIMEMMLB': 'EPO',
    'PRIMEMMLKEP1': 'EPO',
    'PRIMEMMLKEP2': 'EPO',
    'PRIMEMMLM': 'EPO',
    'PRIMEMMLR': 'EPO',
    'PRIMEMMMH': 'EPO',
    'PRIMEMMMR': 'EPO',
    'PRIMEMMNV': 'EPO',
    'PRIMEMMPLT': 'EPO',
    'PRIMEMMPMC': 'EPO',
    'PRIMEMMPPOEN': 'PPO',
    'PRIMEMMPPOLAP': 'PPO',
    'PRIMEMMPPOLHCEN': 'PPO',
    'PRIMEMMPPOLLCEN': 'PPO',
    'PRIMEMMPPOUH': 'PPO',
    'PRIMEMMPPOLH': 'PPO',
    'PRIMEMMPPOUL': 'PPO',
    'PRIMEMMRHRI': 'EPO',
    'PRIMEMMRV': 'EPO',
    'PRIMEMMSB': 'EPO',
    'PRIMEMMSBPLT': 'EPO',
    'PRIMEMMSJH': 'EPO',
    'PRIMEMMSM': 'EPO',
    'PRIMEMMSMMSMRMC': 'EPO',
    'PRIMEMMSMMSMRMCP': 'PPO',
    'PRIMEMMSR': 'EPO',
    'PRIMEMMSTCL': 'EPO',
    'PRIMEMMST': 'EPO',
    'PRIMEMMSTPPO': 'PPO',
    'PRIMEMMVAL': 'VALUE',
    'PRIMEMMSMECN': 'EPO',
    'PRIMEMMSMECW': 'EPO',
    'PRIMEMMCIR': 'EPO',
    'PRIMEMMIUOE': 'EPO',
    'PRIMEMMJNESO': 'EPO',
    'PRIMELBH': 'EPO',
    'PRIMEMMEPO3': 'EPO',
    'PRIMEMMEPOESU': 'EPO',
    'PRIMEMMEPOLEUN': 'EPO',
    'PRIMEMMEPPLUS': 'EPO',
    'PRIMEMMVALUE': 'VALUE',
    'PRIMEPOPRE21': 'EPO',
    'PRIMESFMCVAL': 'VALUE',
    'PRIMEASCIL': 'EPO',
    'PRIMEASCILEPO': 'EPO',
    'PRIMEMMIL': 'VALUE',
    'PRIMEMMILVALUE': 'VALUE',
    'PRIMEINAIL': 'EPO',
    'PRIMEINAILVALUE': 'VALUE',
    'PRIMEMMSMEPLUS': 'EPO',
    'PRIMEMMSMUN': 'EPO'
}

# NEW: Tier normalization function
def normalize_tier(raw_tier):
    """
    Normalize raw tier text to exactly: EE Only, EE+Spouse, EE+Child(ren), EE+Family
    Returns UNKNOWN for unmapped values
    """
    if pd.isna(raw_tier):
        return 'UNKNOWN'
    
    # Clean the input
    tier_str = str(raw_tier).strip().upper()
    # Normalize separators
    tier_str = tier_str.replace('&', '+').replace(' AND ', '+').replace('/', '+')
    # Remove extra spaces
    tier_str = ' '.join(tier_str.split())
    
    # Employee Only variants
    if tier_str in ['EMP', 'EE', 'EMPLOYEE ONLY', 'EE ONLY', 'EMPLOYEE', 'E']:
        return 'EE Only'
    
    # Employee + Spouse variants
    if tier_str in ['ESP', 'EE+SPOUSE', 'EE + SPOUSE', 'EMPLOYEE+SPOUSE', 'EE SPOUSE', 
                    'EMPLOYEE SPOUSE', 'ES', 'E+S']:
        return 'EE+Spouse'
    
    # Employee + Child(ren) variants - combining single and multiple children
    if tier_str in ['E1D', 'ECH', 'EE+CHILD', 'EE + CHILD', 'EE+CHILDREN', 'EE + CHILDREN',
                    'EMPLOYEE+CHILD', 'EMPLOYEE+CHILDREN', 'EE CHILD', 'EE CHILDREN',
                    'EC', 'E+C', 'EE+CHILD(REN)', 'CHILD(REN)']:
        return 'EE+Child(ren)'
    
    # Employee + Family variants
    if tier_str in ['FAM', 'FAMILY', 'EE+FAMILY', 'EE + FAMILY', 'EMPLOYEE+FAMILY',
                    'EE FAMILY', 'EF', 'E+F']:
        return 'EE+Family'
    
    # Unknown
    return 'UNKNOWN'

def normalize_plan_group_and_variant(raw_plan, plan_mapping):
    """
    Normalize plan to group (EPO/PPO/VALUE) and keep variant info
    Returns tuple: (plan_group, plan_variant)
    """
    if pd.isna(raw_plan):
        return ('UNKNOWN', 'UNKNOWN')
    
    plan_str = str(raw_plan).strip().upper()
    
    # Check mapping first
    if plan_str in plan_mapping:
        plan_group = plan_mapping[plan_str]
        return (plan_group, plan_str)  # Keep original as variant
    
    # Infer from keywords if not in mapping
    if 'PPO' in plan_str:
        return ('PPO', plan_str)
    elif 'EPO' in plan_str:
        return ('EPO', plan_str)
    elif 'VAL' in plan_str or 'VALUE' in plan_str:
        return ('VALUE', plan_str)
    else:
        return ('UNKNOWN', plan_str)

def read_and_prepare_data(file_path):
    """
    Read source data and prepare for processing
    """
    # Read Excel file
    df = pd.read_excel(file_path, sheet_name=0)
    
    # Filter to active only
    if 'STATUS' in df.columns:
        original_count = len(df)
        df = df[df['STATUS'].astype(str).str.upper() == 'A'].copy()
        print(f"Filtered to {len(df)} active rows (STATUS='A') from {original_count} total")
    
    # Add facility info
    if 'CLIENT ID' in df.columns:
        df['facility_id'] = df['CLIENT ID'].str.strip().str.upper()
        df['facility_name'] = df['facility_id'].map(TPA_TO_FACILITY)
        print(f"Mapped {df['facility_name'].notna().sum()} facilities")
    else:
        print("WARNING: No CLIENT ID column found!")
        df['facility_id'] = 'UNKNOWN'
        df['facility_name'] = 'UNKNOWN'
    
    return df

def process_enrollment_with_integrity(df):
    """
    Process enrollment data with tier normalization and integrity checks
    """
    # Filter to subscribers only
    if 'RELATION' in df.columns:
        subscribers = df[df['RELATION'].str.upper() == 'SELF'].copy()
        print(f"Filtered to {len(subscribers)} subscribers (RELATION='SELF')")
    else:
        print("WARNING: No RELATION column - processing all rows as subscribers")
        subscribers = df.copy()
    
    # Normalize tiers
    if 'BEN CODE' in df.columns:
        print("Using BEN CODE column for tier information")
        subscribers['tier_normalized'] = subscribers['BEN CODE'].apply(normalize_tier)
    else:
        print("WARNING: No BEN CODE column found - defaulting to UNKNOWN")
        subscribers['tier_normalized'] = 'UNKNOWN'
    
    # Normalize plans
    if 'PLAN' in df.columns:
        plan_info = subscribers['PLAN'].apply(lambda x: normalize_plan_group_and_variant(x, PLAN_TO_TYPE))
        subscribers['plan_group'] = plan_info.apply(lambda x: x[0])
        subscribers['plan_variant'] = plan_info.apply(lambda x: x[1])
    else:
        print("WARNING: No PLAN column found - defaulting to UNKNOWN")
        subscribers['plan_group'] = 'UNKNOWN'
        subscribers['plan_variant'] = 'UNKNOWN'
    
    # Audit unknowns
    print("\n=== UNKNOWN AUDIT ===")
    
    # Unknown tiers
    unknown_tiers = subscribers[subscribers['tier_normalized'] == 'UNKNOWN']
    if len(unknown_tiers) > 0 and 'BEN CODE' in df.columns:
        print(f"\nFound {len(unknown_tiers)} UNKNOWN tiers")
        print("Top 10 unmapped tier values:")
        print(unknown_tiers['BEN CODE'].value_counts().head(10))
    
    # Unknown plans
    unknown_plans = subscribers[subscribers['plan_group'] == 'UNKNOWN']
    if len(unknown_plans) > 0 and 'PLAN' in df.columns:
        print(f"\nFound {len(unknown_plans)} UNKNOWN plans")
        print("Top 10 unmapped plan values:")
        print(unknown_plans['PLAN'].value_counts().head(10))
    
    return subscribers

def create_pivots_with_integrity(subscribers):
    """
    Create variant-level and grouped pivots with integrity checks
    """
    # Define tier columns in order
    tier_columns = ['EE Only', 'EE+Spouse', 'EE+Child(ren)', 'EE+Family']
    
    # VARIANT-LEVEL PIVOT
    print("\n=== CREATING VARIANT-LEVEL PIVOT ===")
    pivot_variants = subscribers.groupby(
        ['facility_id', 'plan_group', 'plan_variant', 'tier_normalized']
    ).size().reset_index(name='count')
    
    # Pivot to wide format
    pivot_variants = pivot_variants.pivot_table(
        index=['facility_id', 'plan_group', 'plan_variant'],
        columns='tier_normalized',
        values='count',
        fill_value=0
    )
    
    # Ensure all tier columns exist
    for col in tier_columns:
        if col not in pivot_variants.columns:
            pivot_variants[col] = 0
    
    # Reorder columns and add total
    pivot_variants = pivot_variants[tier_columns]
    pivot_variants['Total'] = pivot_variants[tier_columns].sum(axis=1)
    
    # GROUPED PIVOT (sum variants)
    print("\n=== CREATING GROUPED PIVOT ===")
    pivot_grouped = pivot_variants.reset_index()
    pivot_grouped = pivot_grouped.groupby(['facility_id', 'plan_group'])[tier_columns + ['Total']].sum()
    
    # INTEGRITY CHECKS
    print("\n=== INTEGRITY CHECKS ===")
    
    # Check variant level
    for idx, row in pivot_variants.iterrows():
        facility_id, plan_group, plan_variant = idx
        tier_sum = row[tier_columns].sum()
        total = row['Total']
        
        if abs(tier_sum - total) > 0.01:  # Allow small floating point differences
            print(f"ERROR: Tier sum mismatch for {facility_id}/{plan_group}/{plan_variant}")
            print(f"  Tier sum: {tier_sum}, Total: {total}")
            raise AssertionError(f"Integrity check failed for {idx}")
    
    # Check grouped level
    for idx, row in pivot_grouped.iterrows():
        facility_id, plan_group = idx
        tier_sum = row[tier_columns].sum()
        total = row['Total']
        
        if abs(tier_sum - total) > 0.01:
            print(f"ERROR: Tier sum mismatch for {facility_id}/{plan_group}")
            print(f"  Tier sum: {tier_sum}, Total: {total}")
            raise AssertionError(f"Integrity check failed for {idx}")
    
    print("✓ All integrity checks passed!")
    
    return pivot_variants, pivot_grouped

def validate_acceptance_criteria(pivot_variants, pivot_grouped):
    """
    Validate the specific acceptance criteria
    """
    print("\n=== ACCEPTANCE CRITERIA VALIDATION ===")
    
    # Test 1: San Dimas (H3170) - should have proper tier distribution
    print("\n1. San Dimas (H3170) tier distribution:")
    if 'H3170' in pivot_grouped.index.get_level_values('facility_id'):
        san_dimas = pivot_grouped.xs('H3170', level='facility_id')
        print(san_dimas)
        
        # Check that it's not all in one tier
        for _, row in san_dimas.iterrows():
            non_zero_tiers = (row[['EE Only', 'EE+Spouse', 'EE+Child(ren)', 'EE+Family']] > 0).sum()
            if non_zero_tiers > 1:
                print("✓ PASS: San Dimas has distribution across multiple tiers")
            else:
                print("✗ FAIL: San Dimas collapsed into single tier")
    else:
        print("- San Dimas (H3170) not found in data")
    
    # Test 2: Lower Bucks (H3330) - should have multiple EPO variants
    print("\n2. Lower Bucks (H3330) EPO variants:")
    if 'H3330' in pivot_variants.index.get_level_values('facility_id'):
        lower_bucks_epo = pivot_variants.xs(('H3330', 'EPO'), level=['facility_id', 'plan_group'], drop_level=False)
        if len(lower_bucks_epo) > 1:
            print(f"✓ PASS: Lower Bucks has {len(lower_bucks_epo)} EPO variants")
            print("Variants found:")
            for idx in lower_bucks_epo.index:
                print(f"  - {idx[2]}")
        else:
            print("✗ FAIL: Lower Bucks does not show multiple EPO variants")
    else:
        print("- Lower Bucks (H3330) not found in data")

def main():
    """
    Main execution function
    """
    # File paths
    source_file = r"H:\Ben's Personal Folder\Use this\Copy of P Drive\Ben's Personal Folder\Misc\Personal\EFR\enrollment-automation-main\Source data.xlsx"
    
    try:
        print("="*60)
        print("ENROLLMENT AUTOMATION - FIXED VERSION")
        print("="*60)
        
        # Read and prepare data
        print("\n1. Reading source data...")
        df = read_and_prepare_data(source_file)
        
        # Process with integrity checks
        print("\n2. Processing enrollment data...")
        subscribers = process_enrollment_with_integrity(df)
        
        # Create pivots
        print("\n3. Creating pivot tables...")
        pivot_variants, pivot_grouped = create_pivots_with_integrity(subscribers)
        
        # Show sample results
        print("\n=== SAMPLE RESULTS ===")
        print("\nVariant-level pivot (first 10 rows):")
        print(pivot_variants.head(10))
        
        print("\nGrouped pivot (first 10 rows):")
        print(pivot_grouped.head(10))
        
        # Validate acceptance criteria
        validate_acceptance_criteria(pivot_variants, pivot_grouped)
        
        # Save results
        print("\n4. Saving results...")
        output_path = r"H:\Ben's Personal Folder\Use this\Copy of P Drive\Ben's Personal Folder\Misc\Personal\EFR\enrollment-automation-main"
        
        pivot_variants.to_csv(os.path.join(output_path, "enrollment_pivot_variants.csv"))
        pivot_grouped.to_csv(os.path.join(output_path, "enrollment_pivot_grouped.csv"))
        
        print("\n✓ Processing complete!")
        print(f"✓ Variant pivot saved to: enrollment_pivot_variants.csv")
        print(f"✓ Grouped pivot saved to: enrollment_pivot_grouped.csv")
        
        return pivot_variants, pivot_grouped
        
    except Exception as e:
        print(f"\nERROR: {e}")
        traceback.print_exc()
        return None, None

if __name__ == "__main__":
    main()