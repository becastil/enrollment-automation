"""
Analyze discrepancy between expected Legacy totals and actual source data
Expected: 5,395 total (4,963 EPO + 432 Value)
Actual: 5,326 total (4,935 EPO + 391 Value)
Missing: 69 records
"""

import pandas as pd

def analyze_discrepancy():
    """Analyze the 69-record discrepancy in Legacy tab"""
    
    print("="*70)
    print("LEGACY TAB DISCREPANCY ANALYSIS")
    print("="*70)
    
    # Read source data
    df = pd.read_excel('/mnt/c/Users/becas/Prime_EFR/data/input/source_data.xlsx')
    
    # Legacy CLIENT IDs
    legacy_cids = [
        'H3100', 'H3105', 'H3110', 'H3115', 'H3120', 'H3130', 'H3140', 'H3150',
        'H3160', 'H3170', 'H3180', 'H3190', 'H3200', 'H3210', 'H3230', 'H3240',
        'H3280', 'H3285', 'H3290', 'H3300'
    ]
    
    # Get ALL Legacy rows to understand data
    df_legacy_all = df[df['CLIENT ID'].isin(legacy_cids)].copy()
    print(f"\n1. TOTAL Legacy rows (all): {len(df_legacy_all)}")
    
    # Check STATUS distribution
    print("\n2. STATUS distribution:")
    print(df_legacy_all['STATUS'].value_counts())
    
    # Check RELATION distribution
    print("\n3. RELATION distribution:")
    print(df_legacy_all['RELATION'].value_counts())
    
    # Apply standard filters
    df_active = df_legacy_all[df_legacy_all['STATUS'].str.upper().isin(['A', 'C'])].copy()
    print(f"\n4. After STATUS filter (A or C): {len(df_active)}")
    
    df_subscribers = df_active[df_active['RELATION'].str.upper().isin(['SELF', 'EE', 'EMPLOYEE', 'SUBSCRIBER'])].copy()
    print(f"5. After RELATION filter (subscribers only): {len(df_subscribers)}")
    
    # Map plan types
    df_subscribers['plan_type'] = df_subscribers['PLAN'].apply(
        lambda x: 'Value' if 'VALUE' in str(x).upper() or 'VAL' in str(x).upper() 
        else ('EPO' if 'EPO' in str(x).upper() else 'Other')
    )
    
    # Create summary by BEN CODE and plan_type
    summary = df_subscribers.groupby(['BEN CODE', 'plan_type']).size().unstack(fill_value=0)
    
    print("\n6. ACTUAL VALUES FROM SOURCE DATA:")
    print("="*50)
    print("Tier\t\tEPO\tValue\tTotal")
    print("-"*50)
    
    totals = {'EPO': 0, 'Value': 0}
    for tier in ['EMP', 'ESP', 'ECH', 'FAM']:
        if tier in summary.index:
            epo = summary.loc[tier, 'EPO'] if 'EPO' in summary.columns else 0
            value = summary.loc[tier, 'Value'] if 'Value' in summary.columns else 0
            total = epo + value
            totals['EPO'] += epo
            totals['Value'] += value
            print(f"{tier}\t\t{epo}\t{value}\t{total}")
    
    print("-"*50)
    print(f"Grand Total\t{totals['EPO']}\t{totals['Value']}\t{totals['EPO'] + totals['Value']}")
    
    print("\n7. EXPECTED VALUES:")
    print("="*50)
    print("Tier\t\tEPO\tValue\tTotal")
    print("-"*50)
    expected = {
        'EMP': {'EPO': 3053, 'Value': 290, 'Total': 3343},
        'ESP': {'EPO': 481, 'Value': 34, 'Total': 515},
        'ECH': {'EPO': 833, 'Value': 60, 'Total': 893},
        'FAM': {'EPO': 596, 'Value': 48, 'Total': 644}
    }
    
    expected_totals = {'EPO': 0, 'Value': 0}
    for tier, values in expected.items():
        expected_totals['EPO'] += values['EPO']
        expected_totals['Value'] += values['Value']
        print(f"{tier}\t\t{values['EPO']}\t{values['Value']}\t{values['Total']}")
    
    print("-"*50)
    print(f"Grand Total\t{expected_totals['EPO']}\t{expected_totals['Value']}\t{expected_totals['EPO'] + expected_totals['Value']}")
    
    print("\n8. DISCREPANCIES:")
    print("="*50)
    print("Tier\t\tEPO Diff\tValue Diff\tTotal Diff")
    print("-"*50)
    
    total_diff = {'EPO': 0, 'Value': 0}
    for tier in ['EMP', 'ESP', 'ECH', 'FAM']:
        if tier in summary.index:
            actual_epo = summary.loc[tier, 'EPO'] if 'EPO' in summary.columns else 0
            actual_value = summary.loc[tier, 'Value'] if 'Value' in summary.columns else 0
        else:
            actual_epo = 0
            actual_value = 0
        
        epo_diff = actual_epo - expected[tier]['EPO']
        value_diff = actual_value - expected[tier]['Value']
        total_diff['EPO'] += epo_diff
        total_diff['Value'] += value_diff
        
        print(f"{tier}\t\t{epo_diff:+d}\t\t{value_diff:+d}\t\t{epo_diff + value_diff:+d}")
    
    print("-"*50)
    print(f"Grand Total\t{total_diff['EPO']:+d}\t\t{total_diff['Value']:+d}\t\t{total_diff['EPO'] + total_diff['Value']:+d}")
    
    print("\n9. ANALYSIS SUMMARY:")
    print("="*50)
    print(f"Total records missing: {expected_totals['EPO'] + expected_totals['Value'] - (totals['EPO'] + totals['Value'])}")
    print(f"EPO records difference: {total_diff['EPO']:+d}")
    print(f"Value records difference: {total_diff['Value']:+d}")
    
    # Check for any excluded statuses or relations that might account for the difference
    print("\n10. POTENTIAL MISSING RECORDS:")
    print("="*50)
    
    # Check if STATUS='B' has any records
    df_b_status = df_legacy_all[df_legacy_all['STATUS'] == 'B']
    if len(df_b_status) > 0:
        print(f"Found {len(df_b_status)} records with STATUS='B' (might be excluded)")
    
    # Check for other RELATION values
    other_relations = df_active[~df_active['RELATION'].str.upper().isin(['SELF', 'EE', 'EMPLOYEE', 'SUBSCRIBER'])]
    if len(other_relations) > 0:
        print(f"Found {len(other_relations)} active records with non-subscriber relations:")
        print(other_relations['RELATION'].value_counts())
    
    print("\n" + "="*70)
    print("CONCLUSION:")
    print("The source data contains 5,326 Legacy subscriber records.")
    print("Your expected values show 5,395 records (difference of 69).")
    print("This suggests the expected values may come from a different")
    print("data source, time period, or include additional filtering criteria.")
    print("="*70)

if __name__ == "__main__":
    analyze_discrepancy()