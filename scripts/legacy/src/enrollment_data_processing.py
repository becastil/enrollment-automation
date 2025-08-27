
"""
Enrollment Data Processing with Pandas - Main Implementation
===========================================================

This module contains the complete implementation of the enrollment data processing
functions as described in the technical documentation. It automates Excel-based
enrollment data workflows with robust error handling and validation.

Key Features:
- Process individual sheets or all tabs at once
- Flexible column mapping and reference data lookup
- Data validation with missing mapping flags
- Support for contract counting or measure aggregation
- Facility group filtering capabilities

Author: Automated Processing System
Date: August 2025
Version: 1.0
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Union
import warnings

warnings.filterwarnings('ignore')


def build_facility_summary(
    excel_path: str,
    sheet_name: str = "Cleaned use this one",
    facility_key_col: str = "FacilityKey", 
    plan_type_col: str = "PlanType",
    measure_col: str | None = None,
    facility_map=None,
    plan_map=None,
    facility_id_col: str = "facility_id",
    facility_name_col: str = "facility_name", 
    client_id_col: str = "client_id",
    plan_group_col: str = "plan_group",
    facility_group: str = "Centinela",
    facility_group_names: list[str] = None,
    facility_group_client_ids: list[str] = None
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Process enrollment data to produce facility-level summaries.

    This function reads enrollment data from Excel, performs data cleaning and validation,
    looks up facility and plan information, and produces aggregated summaries.

    Args:
        excel_path: Path to the Excel file
        sheet_name: Name of the worksheet to process
        facility_key_col: Column name containing facility identifiers
        plan_type_col: Column name containing plan type codes
        measure_col: Column to aggregate (None for contract counting)
        facility_map: DataFrame or dict mapping facility keys to facility info
        plan_map: DataFrame or dict mapping plan types to plan groups
        facility_id_col: Output column name for facility ID
        facility_name_col: Output column name for facility name
        client_id_col: Output column name for client ID
        plan_group_col: Output column name for plan group
        facility_group: Name of facility group for filtering
        facility_group_names: List of facility names to include in group
        facility_group_client_ids: List of client IDs to include in group

    Returns:
        Tuple of (enriched_data, full_summary, filtered_summary) DataFrames

    Raises:
        IOError: If Excel file cannot be read
        KeyError: If required columns are missing
        ValueError: If facility mapping cannot be resolved
    """

    # Step 1: Read the Excel sheet into a DataFrame
    try:
        # Special handling for 'Cleaned use this one' sheet - header at row 5
        if sheet_name == "Cleaned use this one":
            df = pd.read_excel(excel_path, sheet_name=sheet_name, header=5)
        else:
            df = pd.read_excel(excel_path, sheet_name=sheet_name, header=0)
    except Exception as e:
        raise IOError(f"Error reading '{sheet_name}' from file: {e}")

    # If the first row isn't the actual header, find the header row
    if facility_key_col not in df.columns:
        # Try reading without header to find the correct row
        df_raw = pd.read_excel(excel_path, sheet_name=sheet_name, header=None, nrows=30)
        header_row = None
        
        for i in range(30):  # check first 30 rows for header clues
            row_values = df_raw.iloc[i].astype(str).tolist()
            if any(facility_key_col in str(val) for val in row_values) or \
               any(plan_type_col in str(val) for val in row_values):
                header_row = i
                break
        
        if header_row is not None:
            df = pd.read_excel(excel_path, sheet_name=sheet_name, header=header_row)
        else:
            # If still not found, try to use first non-empty row as header
            df = pd.read_excel(excel_path, sheet_name=sheet_name, header=None)
            df.dropna(how='all', inplace=True)
            df.reset_index(drop=True, inplace=True)
            if len(df) > 0:
                df.columns = df.iloc[0]  # use first row of data as columns
                df = df[1:]

    # Drop any entirely unnamed columns (extra blank columns from Excel)
    df = df.loc[:, ~df.columns.astype(str).str.startswith("Unnamed")]
    
    # Clean the dataframe for 'Cleaned use this one' sheet
    if sheet_name == "Cleaned use this one" and facility_key_col in df.columns:
        # Remove header rows that might be mixed in with data
        df = df[df[facility_key_col].notna()]
        df = df[~df[facility_key_col].astype(str).str.startswith('CLIENT')]
        df = df[~df[facility_key_col].astype(str).str.startswith('Client')]

    # Step 2: Clean data rows
    # Remove rows with no contract ID (these might be group labels or empty lines)
    contract_col = None
    for col in ["ContractID", "Contract ID", "ALT ID", "Alt ID", "SubscriberID"]:
        if col in df.columns:
            contract_col = col
            break

    if contract_col:
        df = df[df[contract_col].notna()].reset_index(drop=True)

    # Strip whitespace from key identifying columns
    if not pd.api.types.is_numeric_dtype(df[facility_key_col]):
        df[facility_key_col] = df[facility_key_col].astype(str).str.strip()
    if not pd.api.types.is_numeric_dtype(df[plan_type_col]):
        df[plan_type_col] = df[plan_type_col].astype(str).str.strip()

    # Copy original data for enrichment
    df_enriched = df.copy()

    # Step 3: Lookup facility details via mapping
    if facility_map is not None:
        if isinstance(facility_map, dict):
            # Simple dictionary mapping
            df_enriched[facility_name_col] = df_enriched[facility_key_col].map(facility_map)
            df_enriched[client_id_col] = df_enriched[facility_key_col]
            df_enriched[facility_id_col] = df_enriched[facility_key_col]
        else:
            fac_map_df = facility_map.copy()
            # Determine which column to join on
            if facility_key_col in fac_map_df.columns:
                map_key = facility_key_col
            else:
                map_key = None
                if "TPA Code" in fac_map_df.columns and \
                   df_enriched[facility_key_col].astype(str).isin(fac_map_df["TPA Code"].astype(str)).any():
                    map_key = "TPA Code"
                elif "Facility" in fac_map_df.columns and \
                     df_enriched[facility_key_col].astype(str).isin(fac_map_df["Facility"].astype(str)).any():
                    map_key = "Facility"
                else:
                    raise ValueError(f"Could not find matching key in facility_map for column '{facility_key_col}'")

            # Merge the facility mapping (left join to retain all enrollments)
            df_enriched = pd.merge(df_enriched, fac_map_df, how='left',
                                   left_on=facility_key_col, right_on=map_key,
                                   suffixes=("", "_map"))

            if map_key != facility_key_col:
                df_enriched.drop(columns=[map_key], inplace=True)

            # Assign output columns from merged data
            if "Facility" in df_enriched.columns and facility_name_col not in df_enriched.columns:
                df_enriched[facility_name_col] = df_enriched["Facility"]
            if "TPA Code" in df_enriched.columns and client_id_col not in df_enriched.columns:
                df_enriched[client_id_col] = df_enriched["TPA Code"]

            # Set facility ID
            if facility_id_col not in df_enriched.columns:
                df_enriched[facility_id_col] = df_enriched.get("Facility ID", 
                                                               df_enriched.get(client_id_col, 
                                                                             df_enriched[facility_key_col]))
    else:
        # No facility mapping provided
        df_enriched[facility_name_col] = df_enriched[facility_key_col]
        df_enriched[client_id_col] = df_enriched[facility_key_col]
        df_enriched[facility_id_col] = df_enriched[facility_key_col]

    # Flag contracts with missing facility mapping
    df_enriched["missing_facility_flag"] = df_enriched[facility_name_col].isna() | \
                                           (df_enriched[facility_name_col].astype(str).str.strip() == "")

    # Step 4: Lookup plan group via mapping
    if plan_map is not None:
        if isinstance(plan_map, dict):
            plan_mapping = plan_map
        else:
            plan_map_df = plan_map.copy()
            # Determine plan columns
            plan_key = plan_type_col if plan_type_col in plan_map_df.columns else "PLAN"
            plan_val = plan_group_col if plan_group_col in plan_map_df.columns else "EPO-PPO-VALUE"

            if plan_key not in plan_map_df.columns:
                plan_key = plan_map_df.columns[0]
            if plan_val not in plan_map_df.columns:
                plan_val = plan_map_df.columns[1] if plan_map_df.shape[1] > 1 else plan_map_df.columns[0]

            plan_mapping = dict(zip(plan_map_df[plan_key].astype(str), plan_map_df[plan_val]))

        # Map each PlanType to its plan group
        df_enriched[plan_group_col] = df_enriched[plan_type_col].astype(str).map(plan_mapping)
    else:
        df_enriched[plan_group_col] = df_enriched[plan_type_col]

    # Flag missing plan group mappings
    df_enriched["missing_plan_flag"] = df_enriched[plan_group_col].isna()

    # Step 5: Filter to one row per contract (subscriber)
    subscriber_mask = None

    # Look for sequence number or relation columns
    for col in ["SEQ. #", "Sequence", "Seq", "RELATION"]:
        if col in df_enriched.columns:
            if col.upper().startswith("SEQ"):
                # Handle both numeric and string sequence numbers
                if pd.api.types.is_numeric_dtype(df_enriched[col]):
                    subscriber_mask = (df_enriched[col] == 0) | (df_enriched[col] == 0.0)
                else:
                    subscriber_mask = (df_enriched[col].astype(str).str.strip() == "0")
            elif col.upper() == "RELATION":
                subscriber_mask = df_enriched[col].astype(str).str.upper() == "SELF"
            break

    if subscriber_mask is None and contract_col:
        # Fallback: take first occurrence of each ContractID
        subscriber_mask = ~df_enriched[contract_col].duplicated(keep='first')

    if subscriber_mask is None:
        subscriber_mask = pd.Series(True, index=df_enriched.index)

    df_contracts = df_enriched[subscriber_mask].copy()

    # Step 6: Aggregation
    if measure_col:
        if measure_col not in df_contracts.columns:
            raise KeyError(f"Column '{measure_col}' not found for aggregation")

        # Handle special case for member counting
        if measure_col.lower() == "members" and df_contracts.get(measure_col) is None:
            if contract_col:
                member_counts = df_enriched.groupby(contract_col)[contract_col].size()
                df_contracts = df_contracts.merge(member_counts.rename("Members"), how='left',
                                                left_on=contract_col, right_index=True)
                measure = "Members"
            else:
                df_contracts["Members"] = 1
                measure = "Members"
        else:
            measure = measure_col

        # Ensure numeric dtype for aggregation
        df_contracts[measure] = pd.to_numeric(df_contracts[measure], errors='coerce').fillna(0)
        summary = df_contracts.groupby([facility_name_col, client_id_col, plan_group_col], 
                                     as_index=False)[measure].sum()
    else:
        # Default: count contracts
        summary = df_contracts.groupby([facility_name_col, client_id_col, plan_group_col], 
                                     as_index=False).size()
        summary.rename(columns={"size": "contract_count"}, inplace=True)

    df_summary_full = summary

    # Step 7: Filter summary for specified facility group
    if facility_group_names is None and facility_group_client_ids is None:
        if facility_group.casefold() == "centinela":
            facility_group_names = [
                "Centinela Hospital Medical Center",
                "Robotics Outpatient Center", 
                "Centinela Valley Endoscopy Center"
            ]
            facility_group_client_ids = ["H3270", "H3271", "H3272"]
        else:
            facility_group_names, facility_group_client_ids = [], []

    # Build filter mask
    mask_name = pd.Series(False, index=df_summary_full.index)
    if facility_group_names:
        name_series = df_summary_full[facility_name_col].astype(str).str.casefold()
        for name in facility_group_names:
            if pd.isna(name):
                continue
            mask_name |= name_series.str.contains(str(name).casefold())

    mask_id = pd.Series(False, index=df_summary_full.index)
    if facility_group_client_ids:
        id_series = df_summary_full[client_id_col].astype(str).str.casefold()
        id_list_cf = [str(x).casefold() for x in facility_group_client_ids]
        mask_id = id_series.isin(id_list_cf)

    filter_mask = mask_name | mask_id
    df_summary_filtered = df_summary_full[filter_mask].reset_index(drop=True)

    return df_enriched, df_summary_full, df_summary_filtered


def process_all_enrollment_tabs(
    excel_path: str,
    facility_map=None,
    plan_map=None,
    facility_key_col: str = "CLIENT ID", 
    plan_type_col: str = "PLAN",
    measure_col: str | None = None,
    verbose: bool = True
) -> Dict[str, Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]]:
    """
    Process enrollment data for all facility tabs in the Excel file.

    This function processes multiple worksheets in an Excel file, applying the same
    data processing logic to each sheet. It handles errors gracefully and returns
    results for successfully processed sheets.

    Args:
        excel_path: Path to the Excel file
        facility_map: DataFrame or dict mapping facility keys to facility info
        plan_map: DataFrame or dict mapping plan types to plan groups  
        facility_key_col: Column name containing facility identifiers
        plan_type_col: Column name containing plan type codes
        measure_col: Column to aggregate (None for contract counting)
        verbose: Whether to print progress messages

    Returns:
        Dictionary with sheet names as keys and processing results as values.
        None values indicate failed processing for that sheet.
    """

    # List of all tabs to process
    sheet_names = [
        "Cleaned use this one", "Legacy", "Centinela", "Encino-Garden Grove", 
        "St. Francis", "Alvarado", "Pampa", "Roxborough", "Lower Bucks", 
        "Dallas Medical Center", "Harlingen", "Knapp", "Glendora", "RHRI", 
        "Monroe", "Saint Mary's Reno", "North Vista", "Dallas Regional", 
        "Riverview & Gadsden", "Saint Clare's", "Landmark", "Saint Mary's Passaic", 
        "Southern Regional", "Lehigh", "St Michael's", "Reddy Dev.", "Mission", 
        "Coshocton", "Suburban", "Garden City", "Lake Huron", "Providence & St John", 
        "East Liverpool", "St Joe & St Mary's", "Illinois"
    ]

    results = {}
    successful_count = 0

    for sheet_name in sheet_names:
        try:
            if verbose:
                print(f"Processing sheet: {sheet_name}")

            # Process each sheet
            enriched, full_summary, filtered_summary = build_facility_summary(
                excel_path=excel_path,
                sheet_name=sheet_name,
                facility_key_col=facility_key_col,
                plan_type_col=plan_type_col,
                measure_col=measure_col,
                facility_map=facility_map,
                plan_map=plan_map,
                facility_group=sheet_name if sheet_name != "Cleaned use this one" else "Centinela"
            )

            results[sheet_name] = (enriched, full_summary, filtered_summary)
            successful_count += 1

            if verbose:
                print(f"✓ Successfully processed {sheet_name}: {len(enriched)} total records, "
                      f"{len(full_summary)} summary records")

        except Exception as e:
            if verbose:
                print(f"✗ Error processing sheet '{sheet_name}': {str(e)}")
            results[sheet_name] = None

    if verbose:
        print(f"\nProcessing complete: {successful_count}/{len(sheet_names)} sheets processed successfully")

    return results


def export_consolidated_summary(
    all_results: Dict[str, Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]],
    output_path: str = "consolidated_enrollment_summary.csv",
    include_failed: bool = False
) -> pd.DataFrame:
    """
    Export consolidated summary across all processed sheets.

    Args:
        all_results: Dictionary of processing results from process_all_enrollment_tabs
        output_path: Path for output CSV file
        include_failed: Whether to include information about failed processing

    Returns:
        Consolidated DataFrame with all summary data
    """

    all_summaries = []
    processing_log = []

    for sheet_name, result in all_results.items():
        if result is not None:
            enriched, full_summary, filtered_summary = result
            # Add sheet identifier
            full_summary = full_summary.copy()
            full_summary['source_sheet'] = sheet_name
            full_summary['processing_status'] = 'Success'
            all_summaries.append(full_summary)

            processing_log.append({
                'sheet_name': sheet_name,
                'status': 'Success',
                'total_records': len(enriched),
                'summary_records': len(full_summary),
                'filtered_records': len(filtered_summary)
            })
        else:
            processing_log.append({
                'sheet_name': sheet_name,
                'status': 'Failed',
                'total_records': 0,
                'summary_records': 0,
                'filtered_records': 0
            })

    if all_summaries:
        consolidated_summary = pd.concat(all_summaries, ignore_index=True)
        consolidated_summary.to_csv(output_path, index=False)

        # Create processing log
        log_df = pd.DataFrame(processing_log)
        log_path = output_path.replace('.csv', '_processing_log.csv')
        log_df.to_csv(log_path, index=False)

        print(f"Consolidated summary exported: {len(consolidated_summary)} records -> {output_path}")
        print(f"Processing log exported: {len(log_df)} entries -> {log_path}")

        return consolidated_summary
    else:
        print("No successful processing results to export")
        return pd.DataFrame()


def create_facility_report(
    consolidated_summary: pd.DataFrame,
    report_path: str = "facility_enrollment_report.csv"
) -> pd.DataFrame:
    """
    Create a facility-level report with key metrics.

    Args:
        consolidated_summary: Consolidated summary DataFrame
        report_path: Path for output report file

    Returns:
        Facility report DataFrame
    """

    if consolidated_summary.empty:
        print("Cannot create report: consolidated summary is empty")
        return pd.DataFrame()

    # Determine the count column name
    count_col = 'contract_count' if 'contract_count' in consolidated_summary.columns else consolidated_summary.select_dtypes(include=[np.number]).columns[0]

    # Create facility-level summary
    facility_report = consolidated_summary.groupby(['facility_name', 'client_id']).agg({
        count_col: 'sum',
        'plan_group': 'nunique',
        'source_sheet': 'first'
    }).reset_index()

    facility_report.rename(columns={
        count_col: 'total_contracts',
        'plan_group': 'plan_groups_offered'
    }, inplace=True)

    # Sort by total contracts descending
    facility_report = facility_report.sort_values('total_contracts', ascending=False)

    # Export report
    facility_report.to_csv(report_path, index=False)
    print(f"Facility report exported: {len(facility_report)} facilities -> {report_path}")

    return facility_report


if __name__ == "__main__":
    print("Enrollment Data Processing Module Loaded")
    print("========================================")
    print("Available functions:")
    print("- build_facility_summary(): Process individual sheet")
    print("- process_all_enrollment_tabs(): Process all sheets")
    print("- export_consolidated_summary(): Export consolidated results")
    print("- create_facility_report(): Generate facility-level report")
    print("\nSee enrollment_processing_demo.py for usage examples")
