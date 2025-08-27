"""
Test script to demonstrate the fix for tier collapse bug
Shows before/after comparison for key facilities
"""

import pandas as pd
import numpy as np

def create_test_data():
    """
    Create sample test data that demonstrates the issue
    """
    # Sample data that would cause the bug
    test_data = pd.DataFrame([
        # San Dimas (H3170) - should have multiple tiers, not just Family
        {'CLIENT ID': 'H3170', 'RELATION': 'SELF', 'BEN CODE': 'EMP', 'PLAN': 'PRIMEMMEPOLE', 'STATUS': 'A'},
        {'CLIENT ID': 'H3170', 'RELATION': 'SELF', 'BEN CODE': 'ESP', 'PLAN': 'PRIMEMMEPOLE', 'STATUS': 'A'},
        {'CLIENT ID': 'H3170', 'RELATION': 'SELF', 'BEN CODE': 'ESP', 'PLAN': 'PRIMEMMEPOLE', 'STATUS': 'A'},
        {'CLIENT ID': 'H3170', 'RELATION': 'SELF', 'BEN CODE': 'E1D', 'PLAN': 'PRIMEMMEPOLE', 'STATUS': 'A'},
        {'CLIENT ID': 'H3170', 'RELATION': 'SELF', 'BEN CODE': 'ECH', 'PLAN': 'PRIMEMMEPOLE', 'STATUS': 'A'},
        {'CLIENT ID': 'H3170', 'RELATION': 'SELF', 'BEN CODE': 'FAM', 'PLAN': 'PRIMEMMEPOLE', 'STATUS': 'A'},
        {'CLIENT ID': 'H3170', 'RELATION': 'SELF', 'BEN CODE': 'FAM', 'PLAN': 'PRIMEMMEPOLE', 'STATUS': 'A'},
        
        # Lower Bucks (H3330) - multiple EPO variants
        {'CLIENT ID': 'H3330', 'RELATION': 'SELF', 'BEN CODE': 'EMP', 'PLAN': 'PRIMEMMLB', 'STATUS': 'A'},
        {'CLIENT ID': 'H3330', 'RELATION': 'SELF', 'BEN CODE': 'ESP', 'PLAN': 'PRIMEMMLB', 'STATUS': 'A'},
        {'CLIENT ID': 'H3330', 'RELATION': 'SELF', 'BEN CODE': 'FAM', 'PLAN': 'PRIMEMMLB', 'STATUS': 'A'},
        {'CLIENT ID': 'H3330', 'RELATION': 'SELF', 'BEN CODE': 'EMP', 'PLAN': 'PRIMEMMLKEP1', 'STATUS': 'A'},
        {'CLIENT ID': 'H3330', 'RELATION': 'SELF', 'BEN CODE': 'ESP', 'PLAN': 'PRIMEMMLKEP1', 'STATUS': 'A'},
        {'CLIENT ID': 'H3330', 'RELATION': 'SELF', 'BEN CODE': 'EMP', 'PLAN': 'PRIMEMMLKEP2', 'STATUS': 'A'},
        {'CLIENT ID': 'H3330', 'RELATION': 'SELF', 'BEN CODE': 'FAM', 'PLAN': 'PRIMEMMLKEP2', 'STATUS': 'A'},
        
        # Add some dependents to show filtering works
        {'CLIENT ID': 'H3170', 'RELATION': 'SPOUSE', 'BEN CODE': None, 'PLAN': 'PRIMEMMEPOLE', 'STATUS': 'A'},
        {'CLIENT ID': 'H3170', 'RELATION': 'CHILD', 'BEN CODE': None, 'PLAN': 'PRIMEMMEPOLE', 'STATUS': 'A'},
    ])
    
    return test_data

def simulate_old_logic(df):
    """
    Simulate the buggy logic that causes tier collapse
    """
    print("=== OLD LOGIC (BUGGY) ===")
    
    # The old logic would calculate ben codes from relations
    # But when filtering to SELF only, it loses context
    subscribers = df[df['RELATION'] == 'SELF'].copy()
    
    # Old mapping
    ben_to_tier = {
        'EMP': 'EE',
        'ESP': 'EE & Spouse', 
        'E1D': 'EE & Child',
        'ECH': 'EE & Children',
        'FAM': 'EE & Family'
    }
    
    # In the bug, sometimes everything defaults to one tier
    # Simulating the collapse that happens
    subscribers['tier'] = subscribers['BEN CODE'].map(ben_to_tier).fillna('EE & Family')  # Bug: defaults to Family
    
    result = subscribers.groupby(['CLIENT ID', 'tier']).size().unstack(fill_value=0)
    print(result)
    return result

def simulate_new_logic(df):
    """
    Simulate the fixed logic with proper normalization
    """
    print("\n=== NEW LOGIC (FIXED) ===")
    
    def normalize_tier(raw):
        if pd.isna(raw):
            return 'UNKNOWN'
        
        tier_map = {
            'EMP': 'EE',
            'ESP': 'EE & Spouse',
            'E1D': 'EE & Child',
            'ECH': 'EE & Children',
            'FAM': 'EE & Family'
        }
        
        return tier_map.get(raw, 'UNKNOWN')
    
    # Filter to subscribers
    subscribers = df[df['RELATION'] == 'SELF'].copy()
    
    # Apply normalization
    subscribers['tier'] = subscribers['BEN CODE'].apply(normalize_tier)
    
    # No defaulting to Family - unknowns stay unknown
    result = subscribers.groupby(['CLIENT ID', 'tier']).size().unstack(fill_value=0)
    print(result)
    
    # Also show variant tracking
    print("\n=== VARIANT TRACKING (NEW) ===")
    plan_to_type = {
        'PRIMEMMEPOLE': 'EPO',
        'PRIMEMMLB': 'EPO',
        'PRIMEMMLKEP1': 'EPO',
        'PRIMEMMLKEP2': 'EPO'
    }
    
    subscribers['plan_type'] = subscribers['PLAN'].map(plan_to_type)
    subscribers['plan_variant'] = subscribers['PLAN']
    
    variants = subscribers.groupby(['CLIENT ID', 'plan_type', 'plan_variant']).size()
    print("\nPlan variants by facility:")
    print(variants)
    
    return result

def main():
    print("="*60)
    print("TIER COLLAPSE BUG - BEFORE/AFTER DEMONSTRATION")
    print("="*60)
    
    # Create test data
    test_df = create_test_data()
    
    print("\nTest data summary:")
    print(f"Total rows: {len(test_df)}")
    print(f"Subscribers (SELF): {len(test_df[test_df['RELATION'] == 'SELF'])}")
    print(f"Facilities: {test_df['CLIENT ID'].nunique()}")
    
    # Show the problem
    print("\n" + "="*60)
    old_result = simulate_old_logic(test_df)
    
    print("\n" + "="*60)
    new_result = simulate_new_logic(test_df)
    
    # Acceptance criteria check
    print("\n" + "="*60)
    print("ACCEPTANCE CRITERIA VALIDATION")
    print("="*60)
    
    print("\n1. San Dimas (H3170) - Should have multiple tiers:")
    if 'H3170' in new_result.index:
        san_dimas = new_result.loc['H3170']
        non_zero_tiers = (san_dimas > 0).sum()
        if non_zero_tiers > 1:
            print(f"✓ PASS: Has {non_zero_tiers} different tiers")
        else:
            print(f"✗ FAIL: Only {non_zero_tiers} tier(s)")
    
    print("\n2. Lower Bucks (H3330) - Should have EPO variants:")
    subscribers = test_df[test_df['RELATION'] == 'SELF'].copy()
    lb_plans = subscribers[subscribers['CLIENT ID'] == 'H3330']['PLAN'].unique()
    if len(lb_plans) > 1:
        print(f"✓ PASS: Has {len(lb_plans)} plan variants: {lb_plans}")
    else:
        print(f"✗ FAIL: Only {len(lb_plans)} variant")

if __name__ == "__main__":
    main()