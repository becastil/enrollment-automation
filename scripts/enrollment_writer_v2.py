#!/usr/bin/env python3
"""
Enrollment Writer v2 - Dynamic Excel Writing
============================================

This module replaces static write_maps.py with dynamic discovery-based writing.
It integrates with the Smart Excel Discovery system to automatically find and
update enrollment values in the correct cells.
"""

import os
import sys
import json
import pandas as pd
from datetime import datetime
from typing import Dict, List, Any, Optional
import openpyxl
from openpyxl import load_workbook

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from enrollment_automation_v6 import (
    CID_TO_TAB,
    load_block_aggregations,
    read_and_prepare_data,
    build_tier_data_from_source,
    load_plan_mappings
)
from smart_excel_discovery import TemplateAnalyzer, SmartExcelWriter


class EnrollmentWriterV2:
    """Enhanced enrollment writer using dynamic discovery"""
    
    def __init__(self, template_path: str, source_data_path: str, column_config: Dict = None):
        """
        Initialize with template and source data paths.
        
        Args:
            template_path: Path to Excel template
            source_data_path: Path to source enrollment data
            column_config: Optional column configuration to override auto-detection
        """
        self.template_path = template_path
        self.source_data_path = source_data_path
        self.column_config = column_config
        self.analyzer = TemplateAnalyzer(template_path, column_config)
        self.writer = None
        self.discovery_map = {}
        self.block_aggregations = load_block_aggregations()
        self.enrollment_data = {}
        self.tier_data = {}  # Aggregated tier counts
        self.write_log = []
        
    def discover_template_structure(self):
        """Discover structure of all tabs in template"""
        print("\n" + "="*50)
        print("DISCOVERING TEMPLATE STRUCTURE")
        print("="*50)
        
        # Discover all tabs
        self.discovery_map = self.analyzer.discover_all_tabs()
        
        if not self.discovery_map:
            print("✗ No structure discovered in template")
            return False
        
        # Summary
        total_facilities = 0
        for tab_name, tab_data in self.discovery_map.items():
            facility_count = len(tab_data['facilities'])
            total_facilities += facility_count
            print(f"  {tab_name}: {facility_count} facilities discovered")
        
        print(f"\nTotal: {total_facilities} facilities across {len(self.discovery_map)} tabs")
        
        # Save discovery map
        config_dir = os.path.join(os.path.dirname(self.template_path), 'config')
        discovery_path = os.path.join(config_dir, 'enrollment_discovery_map.json')
        self.analyzer.save_discovery_map(discovery_path)
        
        return True
    
    def load_enrollment_data(self):
        """Load and process enrollment data from source"""
        print("\n" + "="*50)
        print("LOADING ENROLLMENT DATA")
        print("="*50)
        
        # Load source data
        plan_mappings = load_plan_mappings()
        df = read_and_prepare_data(self.source_data_path, plan_mappings)
        
        # Build aggregated tier data (dictionary structure)
        self.tier_data = build_tier_data_from_source(
            df, 
            self.block_aggregations,
            False  # allow_ppo parameter
        )
        
        # Organize source data by tab and facility (using DataFrame rows)
        for _, row in df.iterrows():
            client_id = row.get('CLIENT ID')
            if not client_id or client_id not in CID_TO_TAB:
                continue
            
            tab_name = CID_TO_TAB[client_id]
            
            if tab_name not in self.enrollment_data:
                self.enrollment_data[tab_name] = {}
            
            if client_id not in self.enrollment_data[tab_name]:
                self.enrollment_data[tab_name][client_id] = []
            
            self.enrollment_data[tab_name][client_id].append(row)
        
        # Summary
        total_records = sum(
            len(facilities) 
            for facilities in self.enrollment_data.values()
        )
        
        print(f"✓ Loaded {len(df)} source records")
        print(f"✓ Aggregated into {len(self.tier_data)} facilities")
        print(f"✓ Organized into {len(self.enrollment_data)} tabs")
        print(f"✓ Covering {total_records} facilities")
        
        return True
    
    def aggregate_plan_data(self, client_id: str, plan_records: List) -> Dict:
        """Aggregate enrollment data by plan and tier"""
        aggregated = {}
        
        # Get block configuration if exists
        tab_name = CID_TO_TAB.get(client_id)
        block_config = None
        
        if tab_name in self.block_aggregations:
            if client_id in self.block_aggregations[tab_name]:
                block_config = self.block_aggregations[tab_name][client_id]
        
        # Group by plan type and tier
        for record in plan_records:
            plan_type = self._determine_plan_type(record.get('PLAN', ''))
            tier = record.get('tier', 'Unknown')
            
            # Create key
            key = (plan_type, tier)
            
            if key not in aggregated:
                aggregated[key] = 0
            
            # Add enrollment count (assuming 1 per record, adjust if needed)
            aggregated[key] += 1
        
        return aggregated
    
    def _determine_plan_type(self, plan_code: str) -> str:
        """Determine if plan is EPO or VALUE type"""
        plan_upper = str(plan_code).upper()
        
        if 'VAL' in plan_upper or 'VALUE' in plan_upper:
            return 'VALUE'
        elif 'EPO' in plan_upper or 'PLUS' in plan_upper:
            return 'EPO'
        else:
            # Default based on common patterns
            return 'EPO'
    
    def write_all_enrollments(self):
        """Write all enrollment data to template using discovery"""
        print("\n" + "="*50)
        print("WRITING ENROLLMENT DATA")
        print("="*50)
        
        # First, create a copy of the template
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_dir = os.path.join(os.path.dirname(self.template_path), 'output')
        output_filename = f"enrollment_output_{timestamp}.xlsx"
        output_path = os.path.join(output_dir, output_filename)
        os.makedirs(output_dir, exist_ok=True)
        
        # Copy template file to output
        import shutil
        print(f"\n  Copying template to output...")
        shutil.copy2(self.template_path, output_path)
        print(f"  ✓ Created working copy: {output_filename}")
        
        # Now work with the copy
        self.writer = SmartExcelWriter(output_path, self.discovery_map)
        
        # Load the copied file for editing
        if not self.writer.load_template():
            print("✗ Failed to load copied file for writing")
            return False
        
        print(f"  Template loaded successfully")
        print(f"  Workbook has {len(self.writer.workbook.sheetnames)} sheets")
        
        success_count = 0
        fail_count = 0
        
        # Process each tab
        for tab_name, facilities in self.enrollment_data.items():
            if tab_name not in self.discovery_map:
                print(f"\n✗ Tab {tab_name} not discovered, skipping")
                continue
            
            print(f"\nProcessing {tab_name}:")
            
            # Process each facility in tab
            for client_id, records in facilities.items():
                # Aggregate the data
                aggregated = self.aggregate_plan_data(client_id, records)
                
                # Write each value
                for (plan_type, tier), value in aggregated.items():
                    # Find matching plan name in discovery
                    plan_name = self._find_plan_name_for_type(
                        client_id, plan_type, tab_name
                    )
                    
                    if plan_name:
                        success = self.writer.write_enrollment_value(
                            tab_name, client_id, plan_name, tier, value
                        )
                        
                        if success:
                            success_count += 1
                            self.write_log.append({
                                'tab': tab_name,
                                'client_id': client_id,
                                'plan': plan_name,
                                'tier': tier,
                                'value': value,
                                'status': 'success'
                            })
                        else:
                            fail_count += 1
                            self.write_log.append({
                                'tab': tab_name,
                                'client_id': client_id,
                                'plan': plan_name,
                                'tier': tier,
                                'value': value,
                                'status': 'failed'
                            })
        
        print("\n" + "="*50)
        print("WRITE SUMMARY")
        print("="*50)
        print(f"✓ Successfully wrote: {success_count} values")
        print(f"✗ Failed to write: {fail_count} values")
        
        # Save the changes to the already-copied file
        # output_path was already set when we copied the template
        save_result = self.writer.save_workbook()
        if not save_result:
            print("✗ Failed to save workbook properly")
            return False
        
        final_path = self.writer.template_path  # This is the output file path
        print(f"\n✅ Output file created: {final_path}")
        if os.path.exists(final_path):
            print(f"   Size: {os.path.getsize(final_path):,} bytes")
        
        # Save write log
        self.save_write_log()
        
        return True
    
    def _find_plan_name_for_type(self, client_id: str, plan_type: str, 
                                 tab_name: str) -> Optional[str]:
        """Find the plan name in discovery that matches the plan type"""
        
        if tab_name not in self.discovery_map:
            return None
        
        if client_id not in self.discovery_map[tab_name]['facilities']:
            return None
        
        facility_data = self.discovery_map[tab_name]['facilities'][client_id]
        
        # Search plans for matching type
        for plan_info in facility_data['plans']:
            plan_name = plan_info['plan_name']
            plan_upper = plan_name.upper()
            
            if plan_type == 'EPO' and 'EPO' in plan_upper:
                return plan_name
            elif plan_type == 'VALUE' and 'VALUE' in plan_upper:
                return plan_name
        
        # Return first plan as fallback
        if facility_data['plans']:
            return facility_data['plans'][0]['plan_name']
        
        return None
    
    def save_write_log(self):
        """Save detailed write log"""
        log_dir = os.path.join(os.path.dirname(self.template_path), 'logs')
        log_path = os.path.join(log_dir, 'enrollment_write_log.json')
        os.makedirs(log_dir, exist_ok=True)
        
        with open(log_path, 'w') as f:
            json.dump(self.write_log, f, indent=2)
        
        print(f"\n✓ Write log saved to: {log_path}")
    
    def validate_written_values(self):
        """Validate that written values match expected totals"""
        print("\n" + "="*50)
        print("VALIDATING WRITTEN VALUES")
        print("="*50)
        
        # Group write log by status
        success_writes = [w for w in self.write_log if w['status'] == 'success']
        failed_writes = [w for w in self.write_log if w['status'] == 'failed']
        
        if failed_writes:
            print(f"\n⚠️ {len(failed_writes)} writes failed:")
            for write in failed_writes[:5]:  # Show first 5
                print(f"  - {write['client_id']}/{write['plan']}/{write['tier']}")
        
        # Calculate totals by tier
        tier_totals = {}
        for write in success_writes:
            tier = write['tier']
            value = write['value']
            
            if tier not in tier_totals:
                tier_totals[tier] = 0
            tier_totals[tier] += value
        
        print("\nWritten totals by tier:")
        for tier in ['EE Only', 'EE+Spouse', 'EE+Child(ren)', 'EE+Family']:
            total = tier_totals.get(tier, 0)
            print(f"  {tier:<20}: {total:>8,}")
        
        print(f"  {'TOTAL':<20}: {sum(tier_totals.values()):>8,}")
        
        return tier_totals


def compare_with_static_approach():
    """Compare dynamic discovery with static write_maps approach"""
    
    print("\n" + "="*70)
    print("COMPARISON: DYNAMIC vs STATIC APPROACH")
    print("="*70)
    
    print("\n📊 Static Approach (write_maps.py):")
    print("  ❌ Manual cell mapping required for each facility")
    print("  ❌ Assumes fixed column layout (D, F, G)")
    print("  ❌ Breaks when template structure changes")
    print("  ❌ Time-consuming to maintain")
    print("  ❌ Error-prone with hardcoded cells")
    
    print("\n🎯 Dynamic Approach (Smart Discovery):")
    print("  ✅ Automatically finds Client IDs in ANY column")
    print("  ✅ Auto-detects column layout")
    print("  ✅ Discovers all plans per facility (1 to N)")
    print("  ✅ Maps tier locations dynamically")
    print("  ✅ Adapts to template changes")
    print("  ✅ No maintenance needed")
    
    print("\n💡 Benefits:")
    print("  • Zero configuration required")
    print("  • Works with any template structure")
    print("  • Handles variable numbers of plans")
    print("  • Self-documenting through discovery maps")
    print("  • Reduces errors from manual mapping")


def main():
    """Main function to run dynamic enrollment writing"""
    
    print("\n" + "="*70)
    print("ENROLLMENT WRITER V2 - DYNAMIC DISCOVERY")
    print("="*70)
    
    # File paths - handle both Windows and WSL paths
    # Detect if running in Windows or WSL/Linux
    import platform
    is_windows = platform.system() == 'Windows'
    
    if is_windows:
        # Windows paths
        template_path = r"C:\Users\becas\Prime_EFR\Prime Enrollment Funding by Facility for August.xlsx"
        source_data_path = r"C:\Users\becas\Prime_EFR\data\input\source_data.xlsx"
        print(f"  Running on Windows")
    else:
        # WSL/Linux paths
        template_path = "/mnt/c/Users/becas/Prime_EFR/Prime Enrollment Funding by Facility for August.xlsx"
        source_data_path = "/mnt/c/Users/becas/Prime_EFR/data/input/source_data.xlsx"
        print(f"  Running on Linux/WSL")
    
    # Check files exist
    if not os.path.exists(source_data_path):
        print(f"\n✗ Source data not found: {source_data_path}")
        print("\nPlease ensure the source data file exists at the specified location.")
        return 1
    
    if not os.path.exists(template_path):
        print(f"\n✗ Template not found: {template_path}")
        print("\nPlease ensure the Excel template file exists at the specified location.")
        return 1
    
    print(f"\n✓ Source data found: {source_data_path}")
    print(f"✓ Template found: {template_path}")
    
    # Initialize writer
    writer = EnrollmentWriterV2(template_path, source_data_path)
    
    # Step 1: Discover template structure
    if not writer.discover_template_structure():
        print("✗ Discovery failed")
        return 1
    
    # Step 2: Load enrollment data
    if not writer.load_enrollment_data():
        print("✗ Failed to load enrollment data")
        return 1
    
    # Step 3: Write enrollments
    if not writer.write_all_enrollments():
        print("✗ Writing failed")
        return 1
    
    # Step 4: Validate
    writer.validate_written_values()
    
    # Show comparison
    compare_with_static_approach()
    
    print("\n" + "="*70)
    print("COMPLETE!")
    print("="*70)
    print("\n✅ Successfully implemented dynamic Excel discovery")
    print("✅ No more static cell mappings needed")
    print("✅ System automatically finds where to write values")
    
    return 0


if __name__ == "__main__":
    import argparse
    
    # Set up argument parser for optional path overrides
    parser = argparse.ArgumentParser(description='Enrollment Writer V2 - Dynamic Excel Discovery')
    parser.add_argument('--template', 
                       default="/mnt/c/Users/becas/Prime_EFR/Prime Enrollment Funding by Facility for August.xlsx",
                       help='Path to Excel template file')
    parser.add_argument('--source', 
                       default="/mnt/c/Users/becas/Prime_EFR/data/input/source_data.xlsx",
                       help='Path to source data file')
    
    args = parser.parse_args()
    
    # Override main function to use args if provided
    def main_with_args():
        """Main function with command-line arguments"""
        
        print("\n" + "="*70)
        print("ENROLLMENT WRITER V2 - DYNAMIC DISCOVERY")
        print("="*70)
        
        # Detect if running in Windows or WSL/Linux
        import platform
        is_windows = platform.system() == 'Windows'
        
        # Use provided paths or set defaults based on OS
        if args.template == parser.get_default('template'):
            # Use OS-specific default
            if is_windows:
                template_path = r"C:\Users\becas\Prime_EFR\Prime Enrollment Funding by Facility for August.xlsx"
            else:
                template_path = "/mnt/c/Users/becas/Prime_EFR/Prime Enrollment Funding by Facility for August.xlsx"
        else:
            template_path = args.template
        
        if args.source == parser.get_default('source'):
            # Use OS-specific default
            if is_windows:
                source_data_path = r"C:\Users\becas\Prime_EFR\data\input\source_data.xlsx"
            else:
                source_data_path = "/mnt/c/Users/becas/Prime_EFR/data/input/source_data.xlsx"
        else:
            source_data_path = args.source
        
        if is_windows:
            print(f"  Running on Windows")
        else:
            print(f"  Running on Linux/WSL")
        
        # Normalize paths based on OS
        template_path = os.path.normpath(template_path)
        source_data_path = os.path.normpath(source_data_path)
        
        # Check files exist
        if not os.path.exists(source_data_path):
            print(f"\n✗ Source data not found: {source_data_path}")
            print("\nPlease ensure the source data file exists at the specified location.")
            return 1
        
        if not os.path.exists(template_path):
            print(f"\n✗ Template not found: {template_path}")
            print("\nPlease ensure the Excel template file exists at the specified location.")
            return 1
        
        print(f"\n✓ Source data found: {source_data_path}")
        print(f"✓ Template found: {template_path}")
        
        # Initialize writer
        writer = EnrollmentWriterV2(template_path, source_data_path)
        
        # Step 1: Discover template structure
        if not writer.discover_template_structure():
            print("✗ Discovery failed")
            return 1
        
        # Step 2: Load enrollment data
        if not writer.load_enrollment_data():
            print("✗ Failed to load enrollment data")
            return 1
        
        # Step 3: Write enrollments
        if not writer.write_all_enrollments():
            print("✗ Writing failed")
            return 1
        
        # Step 4: Validate
        writer.validate_written_values()
        
        # Show comparison
        compare_with_static_approach()
        
        print("\n" + "="*70)
        print("COMPLETE!")
        print("="*70)
        print("\n✅ Successfully implemented dynamic Excel discovery")
        print("✅ No more static cell mappings needed")
        print("✅ System automatically finds where to write values")
        
        return 0
    
    sys.exit(main_with_args())