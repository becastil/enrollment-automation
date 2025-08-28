#!/usr/bin/env python3
"""
Simple runner script for the enrollment automation
This ensures the script runs correctly on Windows
"""
import sys
import os

def main():
    """Run the enrollment automation script"""
    
    # Add current directory to Python path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    print("="*60)
    print("STARTING ENROLLMENT AUTOMATION")
    print("="*60)
    print()
    
    try:
        # Import and run the main script
        import enrollment_automation_v6 as eat
        
        # Check for required files
        template_file = "Prime Enrollment Funding by Facility for August.xlsx"
        if not os.path.exists(template_file):
            print(f"ERROR: Template file not found: {template_file}")
            print("Please ensure the Excel template is in the current directory")
            return 1
        
        source_file = os.path.join("data", "input", "source_data.xlsx")
        if not os.path.exists(source_file):
            print(f"ERROR: Source data file not found: {source_file}")
            print("Please ensure the source data file exists")
            return 1
        
        # Run the main function
        eat.main()
        
        print("\n" + "="*60)
        print("ENROLLMENT AUTOMATION COMPLETE")
        print("="*60)
        print("\nOutput files created:")
        print("  • Prime Enrollment Funding by Facility for August_updated.xlsx")
        print("  • output/write_log.csv")
        print("  • output/tier_reconciliation_report.csv")
        
        return 0
        
    except ImportError as e:
        print(f"ERROR: Failed to import required module: {e}")
        print("\nPlease install required packages:")
        print("  pip install pandas openpyxl numpy")
        return 1
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = main()
    if sys.platform == "win32":
        input("\nPress Enter to exit...")
    sys.exit(exit_code)