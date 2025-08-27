"""
Quick diagnostic script to check if your data has the tier collapse issue
Run this to determine if you need to use the fixed version
"""

import pandas as pd
import sys
from pathlib import Path

def diagnose_tier_collapse(file_path, sheet_name=0):
    """
    Check if the enrollment data shows signs of tier collapse bug
    """
    print("="*60)
    print("TIER COLLAPSE DIAGNOSTIC TOOL")
    print("="*60)
    
    try:
        # Read the data
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        print(f"\n✓ Successfully read {len(df)} rows from {file_path}")
        
        # Filter to active subscribers
        if 'STATUS' in df.columns:
            df = df[df['STATUS'] == 'A']
        
        if 'RELATION' in df.columns:
            df = df[df['RELATION'] == 'SELF']
            print(f"✓ Filtered to {len(df)} active subscribers")
        
        # Check BEN CODE distribution
        issues_found = []
        
        if 'BEN CODE' in df.columns:
            ben_dist = df['BEN CODE'].value_counts()
            print(f"\n📊 BEN CODE Distribution:")
            print(ben_dist.head(10))
            
            # Check for suspicious patterns
            total = len(df)
            if len(ben_dist) == 1:
                issues_found.append("CRITICAL: All enrollments in single tier!")
            
            # Check by facility
            if 'CLIENT ID' in df.columns:
                print("\n📍 Checking facilities for single-tier collapse...")
                
                suspicious_facilities = []
                for facility in df['CLIENT ID'].unique():
                    if pd.notna(facility):
                        fac_data = df[df['CLIENT ID'] == facility]
                        if len(fac_data) > 10:  # Only check facilities with >10 employees
                            unique_tiers = fac_data['BEN CODE'].nunique()
                            if unique_tiers == 1:
                                tier = fac_data['BEN CODE'].iloc[0]
                                suspicious_facilities.append({
                                    'facility': facility,
                                    'count': len(fac_data),
                                    'tier': tier
                                })
                
                if suspicious_facilities:
                    issues_found.append(f"Found {len(suspicious_facilities)} facilities with all employees in single tier")
                    print("\n⚠️  Suspicious facilities (all in one tier):")
                    for sf in suspicious_facilities[:5]:  # Show first 5
                        print(f"  - {sf['facility']}: {sf['count']} employees all in '{sf['tier']}'")
                
                # Check specific known problem facilities
                if 'H3170' in df['CLIENT ID'].values:
                    san_dimas = df[df['CLIENT ID'] == 'H3170']
                    if len(san_dimas) > 0:
                        sd_tiers = san_dimas['BEN CODE'].nunique()
                        print(f"\n🔍 San Dimas (H3170) check:")
                        print(f"  - {len(san_dimas)} employees")
                        print(f"  - {sd_tiers} unique tier(s)")
                        if sd_tiers == 1:
                            issues_found.append("San Dimas showing single tier (known bug indicator)")
        else:
            print("\n⚠️  No BEN CODE column found - cannot diagnose tier issues")
        
        # Final diagnosis
        print("\n" + "="*60)
        print("DIAGNOSIS RESULTS")
        print("="*60)
        
        if issues_found:
            print("\n❌ TIER COLLAPSE BUG DETECTED!")
            print("\nIssues found:")
            for issue in issues_found:
                print(f"  - {issue}")
            print("\n✅ RECOMMENDATION: Use enrollment_automation_fixed.py")
            print("   Run: python enrollment_automation_fixed.py")
            return False
        else:
            print("\n✅ No obvious tier collapse issues detected")
            print("   Your data appears to have proper tier distribution")
            return True
            
    except Exception as e:
        print(f"\n❌ Error reading file: {e}")
        return None

def main():
    """
    Main execution
    """
    # Default path or get from command line
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        # Use default path
        file_path = r"H:\Ben's Personal Folder\Use this\Copy of P Drive\Ben's Personal Folder\Misc\Personal\EFR\enrollment-automation-main\Source data.xlsx"
        
        # Check if default exists, otherwise prompt
        if not Path(file_path).exists():
            print("Please provide the path to your source data Excel file:")
            print("Usage: python check_tier_issue.py <path_to_excel>")
            sys.exit(1)
    
    # Run diagnostic
    result = diagnose_tier_collapse(file_path)
    
    if result is False:
        sys.exit(1)  # Exit with error code if bug detected
    elif result is True:
        sys.exit(0)  # Exit successfully if no bug
    else:
        sys.exit(2)  # Exit with different code if error

if __name__ == "__main__":
    main()