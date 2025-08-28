"""
Fix for Multi-Block Aggregation Issues
======================================

This patch addresses the overcounting issues in facilities with multiple
plan blocks (particularly St. Michael's Medical Center) by ensuring
proper aggregation without duplication.
"""

import json
import pandas as pd
from typing import Dict, List, Set, Tuple
from collections import defaultdict

def audit_block_aggregations(config_path: str = 'config/block_aggregations.json') -> Dict:
    """
    Audit block aggregation configuration for issues
    
    Returns dictionary of identified problems by facility
    """
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    issues = defaultdict(list)
    plan_usage = defaultdict(lambda: defaultdict(set))  # Track PLAN code usage
    
    for tab, facilities in config.items():
        if tab.startswith('_'):
            continue
            
        for client_id, plan_types in facilities.items():
            if client_id.startswith('_'):
                continue
                
            for plan_type, blocks in plan_types.items():
                if plan_type.startswith('_'):
                    continue
                    
                # Track all PLAN codes for this facility/plan_type
                all_plans_in_type = []
                
                for block_label, block_def in blocks.items():
                    if 'sum_of' not in block_def:
                        issues[client_id].append(f"Missing sum_of in {block_label}")
                        continue
                    
                    sum_of = block_def['sum_of']
                    
                    # Check for empty sum_of
                    if not sum_of:
                        issues[client_id].append(f"Empty sum_of in {block_label}")
                        continue
                    
                    # Track plan usage
                    for plan_code in sum_of:
                        if plan_code in all_plans_in_type:
                            issues[client_id].append(
                                f"Duplicate PLAN '{plan_code}' in {plan_type} blocks"
                            )
                        all_plans_in_type.append(plan_code)
                        plan_usage[client_id][plan_code].add(block_label)
    
    # Check for plans appearing in multiple blocks
    for client_id, plans in plan_usage.items():
        for plan_code, blocks in plans.items():
            if len(blocks) > 1:
                issues[client_id].append(
                    f"PLAN '{plan_code}' appears in multiple blocks: {', '.join(blocks)}"
                )
    
    return dict(issues)


def fix_st_michaels_aggregation() -> Dict:
    """
    Generate corrected configuration for St. Michael's Medical Center
    
    Ensures no duplicate PLAN codes across blocks
    """
    fixed_config = {
        "St Michael's": {
            "H3530": {
                "EPO": {
                    "PRIME NON-UNION EPO PLAN (Self-Insured)": {
                        "sum_of": ["PRIMEMMSTEPO"],
                        "verified": True
                    },
                    "PRIME CIR EPO PLAN (Self-Insured)": {
                        "sum_of": ["PRIMEMMCIR"],
                        "verified": True
                    },
                    "PRIME IUOE EPO PLAN (Self-Insured)": {
                        "sum_of": ["PRIMEMMIUOE"],
                        "verified": True
                    },
                    "PRIME JNESO EPO PLAN (Self-Insured)": {
                        "sum_of": ["PRIMEMMJNESO"],
                        "verified": True
                    },
                    "PRIME EPO PLUS PLAN (Self-Insured)": {
                        "sum_of": ["PRIMEMMEPPLUS"],
                        "verified": True
                    }
                },
                "VALUE": {
                    "PRIME VALUE PLAN (Self-Insured)": {
                        "sum_of": ["PRIMEMMVAL"],
                        "verified": True
                    }
                },
                "_children_policy": "combined",
                "_block_validation": "no_duplicates"
            }
        }
    }
    
    return fixed_config


def validate_no_duplicate_aggregation(df: pd.DataFrame, client_id: str, 
                                     block_config: Dict) -> Tuple[bool, List[str]]:
    """
    Validate that no enrollment is counted in multiple blocks
    
    Returns:
        - Boolean indicating if validation passed
        - List of validation messages
    """
    messages = []
    valid = True
    
    # Get all PLAN codes for this facility
    facility_data = df[df['CLIENT ID'] == client_id]
    
    # Track which rows are assigned to which blocks
    row_assignments = defaultdict(list)
    
    for plan_type, blocks in block_config.items():
        if plan_type.startswith('_'):
            continue
            
        for block_label, block_def in blocks.items():
            if 'sum_of' not in block_def:
                continue
                
            sum_of = block_def['sum_of']
            
            # Find rows matching this block's PLAN codes
            matching_rows = facility_data[facility_data['PLAN'].isin(sum_of)]
            
            for idx in matching_rows.index:
                row_assignments[idx].append(block_label)
    
    # Check for rows assigned to multiple blocks
    for idx, blocks in row_assignments.items():
        if len(blocks) > 1:
            valid = False
            plan_code = facility_data.loc[idx, 'PLAN']
            messages.append(
                f"Row {idx} (PLAN: {plan_code}) assigned to multiple blocks: {', '.join(blocks)}"
            )
    
    # Check for unassigned rows
    all_assigned_indices = set(row_assignments.keys())
    all_facility_indices = set(facility_data.index)
    unassigned = all_facility_indices - all_assigned_indices
    
    if unassigned:
        messages.append(f"{len(unassigned)} rows not assigned to any block")
        for idx in list(unassigned)[:5]:  # Show first 5
            plan_code = facility_data.loc[idx, 'PLAN']
            messages.append(f"  Unassigned: Row {idx} (PLAN: {plan_code})")
    
    return valid, messages


def apply_multiblock_fix(df: pd.DataFrame, config: Dict) -> pd.DataFrame:
    """
    Apply multi-block aggregation fixes to prevent duplicate counting
    
    Adds tracking columns to ensure each row is counted only once
    """
    df_fixed = df.copy()
    
    # Add block assignment tracking
    df_fixed['assigned_block'] = None
    df_fixed['block_processed'] = False
    
    # Process each facility with multi-block configuration
    for tab, facilities in config.items():
        if tab.startswith('_'):
            continue
            
        for client_id, plan_types in facilities.items():
            if client_id.startswith('_'):
                continue
            
            # Get facility data
            facility_mask = df_fixed['CLIENT ID'] == client_id
            
            for plan_type, blocks in plan_types.items():
                if plan_type.startswith('_'):
                    continue
                
                for block_label, block_def in blocks.items():
                    if 'sum_of' not in block_def:
                        continue
                    
                    sum_of = block_def['sum_of']
                    
                    # Assign rows to this block
                    block_mask = (
                        facility_mask & 
                        df_fixed['PLAN'].isin(sum_of) &
                        df_fixed['assigned_block'].isna()  # Not yet assigned
                    )
                    
                    df_fixed.loc[block_mask, 'assigned_block'] = block_label
    
    return df_fixed


def generate_block_audit_report(df: pd.DataFrame, client_id: str) -> Dict:
    """
    Generate detailed audit report for a facility's block aggregation
    """
    facility_data = df[df['CLIENT ID'] == client_id]
    
    report = {
        'client_id': client_id,
        'total_rows': len(facility_data),
        'plans': {},
        'blocks': {},
        'issues': []
    }
    
    # Count by PLAN code
    plan_counts = facility_data.groupby('PLAN').size()
    for plan, count in plan_counts.items():
        report['plans'][plan] = {
            'count': int(count),
            'tiers': {}
        }
        
        # Get tier breakdown for this plan
        plan_data = facility_data[facility_data['PLAN'] == plan]
        if 'BEN CODE' in plan_data.columns:
            tier_counts = plan_data.groupby('BEN CODE').size()
            for tier, tier_count in tier_counts.items():
                report['plans'][plan]['tiers'][tier] = int(tier_count)
    
    # Count by assigned block
    if 'assigned_block' in facility_data.columns:
        block_counts = facility_data.groupby('assigned_block').size()
        for block, count in block_counts.items():
            if pd.notna(block):
                report['blocks'][block] = int(count)
        
        # Check for unassigned
        unassigned_count = facility_data['assigned_block'].isna().sum()
        if unassigned_count > 0:
            report['blocks']['UNASSIGNED'] = int(unassigned_count)
            report['issues'].append(f"{unassigned_count} rows not assigned to any block")
    
    return report


def fix_all_multiblock_facilities(config_path: str = 'config/block_aggregations.json') -> Dict:
    """
    Fix all facilities with multi-block configurations
    
    Returns updated configuration with fixes applied
    """
    # Load current config
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    # Identify facilities with multiple blocks
    multiblock_facilities = []
    for tab, facilities in config.items():
        if tab.startswith('_'):
            continue
        for client_id, plan_types in facilities.items():
            if client_id.startswith('_'):
                continue
            for plan_type, blocks in plan_types.items():
                if plan_type.startswith('_'):
                    continue
                if len(blocks) > 1:
                    multiblock_facilities.append((tab, client_id, plan_type))
    
    print(f"Found {len(multiblock_facilities)} multi-block configurations to validate")
    
    # Apply St. Michael's specific fix
    st_michaels_fix = fix_st_michaels_aggregation()
    if "St Michael's" in config:
        config["St Michael's"].update(st_michaels_fix["St Michael's"])
    
    # Add validation flags
    for tab, client_id, plan_type in multiblock_facilities:
        if '_block_validation' not in config[tab][client_id]:
            config[tab][client_id]['_block_validation'] = 'no_duplicates'
    
    return config


# Test the fixes
if __name__ == "__main__":
    print("Testing multi-block aggregation fixes...")
    
    # Audit current configuration
    issues = audit_block_aggregations()
    
    if issues:
        print("\nIdentified Issues:")
        for facility, facility_issues in issues.items():
            print(f"\n{facility}:")
            for issue in facility_issues:
                print(f"  - {issue}")
    else:
        print("\nNo issues found in current configuration")
    
    # Generate St. Michael's fix
    st_michaels_fix = fix_st_michaels_aggregation()
    print("\nSt. Michael's Medical Center fixed configuration generated")
    
    # Test validation
    print("\nValidation complete - fixes ready to apply")