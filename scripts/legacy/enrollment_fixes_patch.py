"""
PATCH FOR enrollment_automation.py - Fixes tier collapse bug

This patch modifies the existing enrollment_automation.py to fix the tier normalization issue.
Apply these changes to your existing file.
"""

# ADD THIS NEW FUNCTION after line 449 (after BEN_CODE_TO_TIER dictionary):

def normalize_tier(raw_tier):
    """
    Normalize raw tier text to standardized format
    Returns one of: 'EE', 'EE & Spouse', 'EE & Child', 'EE & Children', 'EE & Family', 'UNKNOWN'
    """
    if pd.isna(raw_tier):
        return 'UNKNOWN'
    
    # Clean the input
    tier_str = str(raw_tier).strip().upper()
    # Normalize separators
    tier_str = tier_str.replace('&', ' AND ').replace('+', ' AND ').replace('/', ' AND ')
    # Remove extra spaces
    tier_str = ' '.join(tier_str.split())
    
    # Employee Only variants
    if tier_str in ['EMP', 'EE', 'EMPLOYEE ONLY', 'EE ONLY', 'EMPLOYEE', 'E']:
        return 'EE'
    
    # Employee + Spouse variants
    if tier_str in ['ESP', 'EE AND SPOUSE', 'EMPLOYEE AND SPOUSE', 'EE SPOUSE', 
                    'EMPLOYEE SPOUSE', 'ES', 'E AND S']:
        return 'EE & Spouse'
    
    # Employee + 1 Child variants
    if tier_str in ['E1D', 'EE AND CHILD', 'EMPLOYEE AND CHILD', 'EE CHILD',
                    'EE AND 1 CHILD', 'EE AND 1 DEPENDENT']:
        return 'EE & Child'
    
    # Employee + Children variants
    if tier_str in ['ECH', 'EE AND CHILDREN', 'EMPLOYEE AND CHILDREN', 'EE CHILDREN',
                    'EC', 'E AND C']:
        return 'EE & Children'
    
    # Employee + Family variants
    if tier_str in ['FAM', 'FAMILY', 'EE AND FAMILY', 'EMPLOYEE AND FAMILY',
                    'EE FAMILY', 'EF', 'E AND F']:
        return 'EE & Family'
    
    # Return UNKNOWN instead of defaulting to any tier
    return 'UNKNOWN'


# REPLACE the process_enrollment_data function (starting around line 646) with:

def process_enrollment_data(df):
    """
    Fixed version that uses direct tier normalization instead of calculating from relations
    """
    processed_data = {}
    
    # DO NOT call calculate_helper_columns - we'll use raw BEN CODE directly
    
    # Filter to only count main subscribers (not dependents)
    if 'RELATION' in df.columns:
        subscribers_df = df.query("RELATION == 'SELF'").copy()
        print(f"Filtered to {len(subscribers_df)} subscriber rows (RELATION = SELF)")
    else:
        subscribers_df = df.copy()
        print("Warning: No RELATION column found, processing all rows")
    
    # Normalize tiers directly from BEN CODE column
    if 'BEN CODE' in subscribers_df.columns:
        print("Using BEN CODE column for tier information")
        subscribers_df['tier'] = subscribers_df['BEN CODE'].apply(normalize_tier)
        
        # Log unknown tiers
        unknown_tiers = subscribers_df[subscribers_df['tier'] == 'UNKNOWN']
        if len(unknown_tiers) > 0:
            print(f"\nWarning: Found {len(unknown_tiers)} rows with UNKNOWN tier")
            print("Top unmapped BEN CODE values:")
            print(unknown_tiers['BEN CODE'].value_counts().head(10))
            # Don't default to EE - keep as UNKNOWN for visibility
    else:
        print("Warning: No BEN CODE column found, defaulting to EE")
        subscribers_df['tier'] = 'EE'
    
    # Map plan codes to types
    if 'PLAN' in subscribers_df.columns:
        subscribers_df['plan_type'] = subscribers_df['PLAN'].map(PLAN_TO_TYPE).fillna(
            subscribers_df['PLAN'].apply(infer_plan_type)
        )
        subscribers_df['plan_variant'] = subscribers_df['PLAN']  # Keep original for variant tracking
        
        # Check for unmapped PLAN codes
        unmapped_plans = subscribers_df[
            ~subscribers_df['PLAN'].isin(PLAN_TO_TYPE.keys()) & subscribers_df['PLAN'].notna()
        ]['PLAN'].unique()
        if len(unmapped_plans) > 0:
            print(f"Warning: Found unmapped PLAN codes (defaulting based on keywords): {unmapped_plans[:10]}")
    else:
        subscribers_df['plan_type'] = 'VALUE'
        subscribers_df['plan_variant'] = 'DEFAULT'
    
    # Show enrollment tier distribution
    tier_dist = subscribers_df['tier'].value_counts()
    print(f"\nEnrollment Tier Distribution:\n{tier_dist}")
    
    # Validate tier integrity - ensure no collapse
    if 'tier' in subscribers_df.columns:
        facilities_with_single_tier = []
        for facility_id in subscribers_df['CLIENT ID'].unique():
            facility_data = subscribers_df[subscribers_df['CLIENT ID'] == facility_id]
            unique_tiers = facility_data['tier'].nunique()
            if unique_tiers == 1 and len(facility_data) > 10:  # Only flag if >10 employees
                facilities_with_single_tier.append(facility_id)
        
        if facilities_with_single_tier:
            print(f"\nWarning: {len(facilities_with_single_tier)} facilities have all enrollments in single tier:")
            for fid in facilities_with_single_tier[:5]:  # Show first 5
                tier = subscribers_df[subscribers_df['CLIENT ID'] == fid]['tier'].iloc[0]
                count = len(subscribers_df[subscribers_df['CLIENT ID'] == fid])
                print(f"  - {fid}: {count} employees all in '{tier}'")
    
    # Continue with existing facility processing logic...
    # (rest of function remains similar but uses normalized 'tier' column)
    
    # Process each tab and facility
    for tab_name, facilities in FACILITY_MAPPING.items():
        processed_data[tab_name] = {}
        
        for client_id, facility_name in facilities.items():
            # Find data for this facility
            id_columns = ['CLIENT ID', 'CLIENT_ID', 'TPA Code', 'DEPT #']
            facility_data = None
            
            for col in id_columns:
                if col in subscribers_df.columns:
                    try:
                        facility_data = subscribers_df.query(f"`{col}` == @client_id").copy()
                        if not facility_data.empty:
                            break
                    except:
                        facility_data = subscribers_df[subscribers_df[col] == client_id].copy()
                        if not facility_data.empty:
                            break
            
            if facility_data is None or facility_data.empty:
                # Default to zeros if no data found
                processed_data[tab_name][facility_name] = {
                    plan: {tier: 0 for tier in ['EE', 'EE & Spouse', 'EE & Child', 'EE & Children', 'EE & Family']}
                    for plan in ['EPO', 'PPO', 'VALUE']
                }
                continue
            
            # Count enrollments by plan type and tier
            if not facility_data.empty:
                # Create pivot table for counts - exclude UNKNOWN tiers from final output
                valid_data = facility_data[facility_data['tier'] != 'UNKNOWN']
                
                if len(valid_data) < len(facility_data):
                    print(f"  Note: Excluded {len(facility_data) - len(valid_data)} UNKNOWN tiers for {facility_name}")
                
                enrollment_counts = (valid_data
                    .groupby(['plan_type', 'tier'])
                    .size()
                    .unstack(fill_value=0)
                    .reindex(columns=['EE', 'EE & Spouse', 'EE & Child', 'EE & Children', 'EE & Family'], fill_value=0)
                    .to_dict('index')
                )
                
                # Structure the result
                result = {}
                for plan in ['EPO', 'PPO', 'VALUE']:
                    if plan in enrollment_counts:
                        result[plan] = enrollment_counts[plan]
                    else:
                        result[plan] = {tier: 0 for tier in ['EE', 'EE & Spouse', 'EE & Child', 'EE & Children', 'EE & Family']}
                
                processed_data[tab_name][facility_name] = result
            else:
                # Use default zeros
                processed_data[tab_name][facility_name] = {
                    plan: {tier: 0 for tier in ['EE', 'EE & Spouse', 'EE & Child', 'EE & Children', 'EE & Family']}
                    for plan in ['EPO', 'PPO', 'VALUE']
                }
    
    # Run integrity check
    print("\n=== INTEGRITY CHECK ===")
    total_subscribers = len(subscribers_df[subscribers_df['tier'] != 'UNKNOWN'])
    total_in_output = 0
    
    for tab_data in processed_data.values():
        for facility_data in tab_data.values():
            for plan_data in facility_data.values():
                total_in_output += sum(plan_data.values())
    
    print(f"Total subscribers (excluding UNKNOWN): {total_subscribers}")
    print(f"Total in output: {total_in_output}")
    
    if abs(total_subscribers - total_in_output) > 0:
        print(f"WARNING: Mismatch of {total_subscribers - total_in_output} records")
    else:
        print("✓ Integrity check passed!")
    
    return processed_data


# OPTIONAL: Add this function to create variant-level output

def create_variant_pivot(df):
    """
    Create a pivot showing plan variants separately
    """
    # Filter to subscribers
    if 'RELATION' in df.columns:
        subscribers = df[df['RELATION'] == 'SELF'].copy()
    else:
        subscribers = df.copy()
    
    # Normalize tiers
    if 'BEN CODE' in subscribers.columns:
        subscribers['tier'] = subscribers['BEN CODE'].apply(normalize_tier)
    else:
        subscribers['tier'] = 'EE'
    
    # Get plan info
    if 'PLAN' in subscribers.columns:
        subscribers['plan_type'] = subscribers['PLAN'].map(PLAN_TO_TYPE).fillna(
            subscribers['PLAN'].apply(infer_plan_type)
        )
        subscribers['plan_variant'] = subscribers['PLAN']
    else:
        subscribers['plan_type'] = 'VALUE'
        subscribers['plan_variant'] = 'DEFAULT'
    
    # Get facility info
    if 'CLIENT ID' in subscribers.columns:
        subscribers['facility_id'] = subscribers['CLIENT ID']
    else:
        subscribers['facility_id'] = 'UNKNOWN'
    
    # Create variant-level pivot
    pivot = subscribers.groupby(
        ['facility_id', 'plan_type', 'plan_variant', 'tier']
    ).size().reset_index(name='count')
    
    pivot = pivot.pivot_table(
        index=['facility_id', 'plan_type', 'plan_variant'],
        columns='tier',
        values='count',
        fill_value=0
    )
    
    # Ensure all tier columns exist
    for col in ['EE', 'EE & Spouse', 'EE & Child', 'EE & Children', 'EE & Family']:
        if col not in pivot.columns:
            pivot[col] = 0
    
    # Add total column
    tier_cols = ['EE', 'EE & Spouse', 'EE & Child', 'EE & Children', 'EE & Family']
    pivot['Total'] = pivot[tier_cols].sum(axis=1)
    
    return pivot


# KEY CHANGES SUMMARY:
# 1. Added normalize_tier() function to properly map tier values
# 2. Modified process_enrollment_data() to use BEN CODE directly instead of calculating
# 3. Added integrity checks and unknown tier auditing
# 4. Added optional create_variant_pivot() for variant-level output
# 5. Removed dependency on flawed calculate_helper_columns() logic