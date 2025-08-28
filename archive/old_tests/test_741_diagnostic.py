"""
Test script to demonstrate the 741 row loss diagnostic
Shows exactly where rows are being dropped
"""

import pandas as pd
import numpy as np

def create_test_data_with_issues():
    """
    Create test data that simulates common row loss scenarios
    """
    test_data = []
    
    # Good rows - San Dimas with proper tiers
    for i in range(10):
        test_data.append({
            'CLIENT ID': 'H3170',
            'RELATION': 'SELF',
            'STATUS': 'A',
            'BEN CODE': ['EMP', 'ESP', 'E1D', 'ECH', 'FAM'][i % 5],
            'PLAN': 'PRIMEMMEPOLE',
            'EMPLOYEE NAME': f'Employee_{i}'
        })
    
    # Rows that might get dropped - various STATUS values
    problematic_statuses = ['ACTIVE', 'Act', 'a', 'I', 'INACTIVE', 'T', '1', 'Y']
    for i, status in enumerate(problematic_statuses):
        test_data.append({
            'CLIENT ID': 'H3330',
            'RELATION': 'SELF',
            'STATUS': status,
            'BEN CODE': 'EMP',
            'PLAN': 'PRIMEMMLB',
            'EMPLOYEE NAME': f'Status_Issue_{i}'
        })
    
    # Rows that might get dropped - various RELATION values
    problematic_relations = ['EE', 'EMPLOYEE', 'SUBSCRIBER', 'S', 'SPOUSE', 'CHILD', 'self', 'Self']
    for i, relation in enumerate(problematic_relations):
        test_data.append({
            'CLIENT ID': 'H3330',
            'RELATION': relation,
            'STATUS': 'A',
            'BEN CODE': 'ESP',
            'PLAN': 'PRIMEMMLKEP1',
            'EMPLOYEE NAME': f'Relation_Issue_{i}'
        })
    
    # Rows with unmapped CLIENT IDs
    for i in range(5):
        test_data.append({
            'CLIENT ID': f'UNKNOWN_{i}',
            'RELATION': 'SELF',
            'STATUS': 'A',
            'BEN CODE': 'FAM',
            'PLAN': 'PRIMEMMEPOLE',
            'EMPLOYEE NAME': f'Unknown_Facility_{i}'
        })
    
    # Rows with unusual tier codes
    unusual_tiers = ['EMPLOYEE ONLY', 'EE + SPOUSE', 'EMPLOYEE+CHILD', 'E+F', 'SOMETHING']
    for i, tier in enumerate(unusual_tiers):
        test_data.append({
            'CLIENT ID': 'H3270',
            'RELATION': 'SELF',
            'STATUS': 'A',
            'BEN CODE': tier,
            'PLAN': 'PRIMEMMEPOCEN',
            'EMPLOYEE NAME': f'Tier_Issue_{i}'
        })
    
    # Rows with spaces in keys
    test_data.append({
        'CLIENT ID': ' H3170 ',  # Leading/trailing spaces
        'RELATION': ' SELF ',
        'STATUS': ' A ',
        'BEN CODE': 'EMP',
        'PLAN': ' PRIMEMMEPOLE ',
        'EMPLOYEE NAME': 'Spaces_In_Keys'
    })
    
    # Add some dependents that should be filtered
    for i in range(10):
        test_data.append({
            'CLIENT ID': 'H3170',
            'RELATION': 'SPOUSE',
            'STATUS': 'A',
            'BEN CODE': None,
            'PLAN': 'PRIMEMMEPOLE',
            'EMPLOYEE NAME': f'Dependent_{i}'
        })
    
    return pd.DataFrame(test_data)

def simulate_old_processing(df):
    """
    Simulate the old processing logic that loses rows
    """
    print("="*60)
    print("OLD PROCESSING (WITH ROW LOSS)")
    print("="*60)
    
    start_count = len(df)
    print(f"Starting rows: {start_count}")
    
    # Strict status filter
    df_active = df[df['STATUS'] == 'A'].copy()
    print(f"After STATUS == 'A': {len(df_active)} (-{start_count - len(df_active)})")
    
    # Strict relation filter
    df_subscribers = df_active[df_active['RELATION'] == 'SELF'].copy()
    print(f"After RELATION == 'SELF': {len(df_subscribers)} (-{len(df_active) - len(df_subscribers)})")
    
    # Drop unmapped facilities
    df_subscribers['Location'] = df_subscribers['CLIENT ID'].map({
        'H3170': 'San Dimas',
        'H3330': 'Lower Bucks',
        'H3270': 'Centinela'
    })
    df_mapped = df_subscribers.dropna(subset=['Location']).copy()
    print(f"After dropna(Location): {len(df_mapped)} (-{len(df_subscribers) - len(df_mapped)})")
    
    print(f"\nTOTAL LOST: {start_count - len(df_mapped)} rows")
    return df_mapped

def simulate_new_processing(df):
    """
    Simulate the new processing with flexible filters
    """
    print("\n" + "="*60)
    print("NEW PROCESSING (PRESERVES ROWS)")
    print("="*60)
    
    start_count = len(df)
    print(f"Starting rows: {start_count}")
    
    # Flexible status filter
    active_statuses = ['A', 'ACTIVE', 'ACT']
    df['is_active'] = df['STATUS'].str.strip().str.upper().isin(active_statuses) | \
                       df['STATUS'].str.strip().str.upper().str.startswith('A')
    df_active = df[df['is_active']].copy()
    print(f"After flexible is_active: {len(df_active)} (-{start_count - len(df_active)})")
    
    # Flexible relation filter
    subscriber_values = ['SELF', 'EE', 'EMP', 'EMPLOYEE', 'SUBSCRIBER', 'S']
    df_active['is_subscriber'] = df_active['RELATION'].str.strip().str.upper().isin(subscriber_values)
    df_subscribers = df_active[df_active['is_subscriber']].copy()
    print(f"After flexible is_subscriber: {len(df_subscribers)} (-{len(df_active) - len(df_subscribers)})")
    
    # Keep unmapped facilities as UNKNOWN
    df_subscribers['Location'] = df_subscribers['CLIENT ID'].str.strip().map({
        'H3170': 'San Dimas',
        'H3330': 'Lower Bucks',
        'H3270': 'Centinela'
    })
    df_subscribers['Location'].fillna('UNKNOWN', inplace=True)
    print(f"After facility mapping (kept UNKNOWNs): {len(df_subscribers)} (-0)")
    
    print(f"\nTOTAL LOST: {start_count - len(df_subscribers)} rows")
    return df_subscribers

def main():
    print("="*80)
    print("741 ROW LOSS DIAGNOSTIC DEMONSTRATION")
    print("="*80)
    
    # Create test data
    test_df = create_test_data_with_issues()
    print(f"\nTest data created: {len(test_df)} total rows")
    
    # Show composition
    print("\nData composition:")
    print(f"  STATUS values: {test_df['STATUS'].nunique()}")
    print(f"  RELATION values: {test_df['RELATION'].nunique()}")
    print(f"  CLIENT ID values: {test_df['CLIENT ID'].nunique()}")
    
    # Run old processing
    old_result = simulate_old_processing(test_df.copy())
    
    # Run new processing
    new_result = simulate_new_processing(test_df.copy())
    
    # Compare results
    print("\n" + "="*60)
    print("COMPARISON")
    print("="*60)
    print(f"Old processing final rows: {len(old_result)}")
    print(f"New processing final rows: {len(new_result)}")
    print(f"ROWS RECOVERED: {len(new_result) - len(old_result)}")
    
    # Show what was recovered
    if len(new_result) > len(old_result):
        print("\nRecovered row categories:")
        unknown_facilities = new_result[new_result['Location'] == 'UNKNOWN']
        print(f"  - Unknown facilities: {len(unknown_facilities)}")
        
        # Check for flexible status matches
        flexible_status = test_df[
            ~test_df['STATUS'].isin(['A']) & 
            test_df['STATUS'].str.strip().str.upper().str.startswith('A')
        ]
        print(f"  - Flexible status matches: {len(flexible_status)}")
        
        # Check for flexible relation matches
        flexible_relation = test_df[
            ~test_df['RELATION'].isin(['SELF']) &
            test_df['RELATION'].str.strip().str.upper().isin(['EE', 'EMPLOYEE', 'SUBSCRIBER', 'S'])
        ]
        print(f"  - Flexible relation matches: {len(flexible_relation)}")

if __name__ == "__main__":
    main()