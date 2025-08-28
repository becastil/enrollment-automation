#!/usr/bin/env python3
"""
Test script to verify Windows path compatibility
"""
import os
import sys

def test_paths():
    """Test that all paths are correctly constructed for Windows"""
    
    print("Testing Windows Path Compatibility")
    print("="*50)
    
    # Test base directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Base directory: {base_dir}")
    print(f"  Exists: {os.path.exists(base_dir)}")
    
    # Test data path
    source_file = os.path.join("data", "input", "source_data.xlsx")
    print(f"\nSource file path: {source_file}")
    print(f"  Exists: {os.path.exists(source_file)}")
    
    # Test template file
    template_filename = "Prime Enrollment Funding by Facility for August.xlsx"
    template_file = os.path.join(base_dir, template_filename)
    print(f"\nTemplate file path: {template_file}")
    print(f"  Exists: {os.path.exists(template_file)}")
    
    # If not in base, try current directory
    if not os.path.exists(template_file):
        template_file = template_filename
        print(f"  Trying current dir: {template_file}")
        print(f"  Exists: {os.path.exists(template_file)}")
    
    # Test output directory
    output_dir = os.path.join(base_dir, 'output')
    print(f"\nOutput directory: {output_dir}")
    print(f"  Exists: {os.path.exists(output_dir)}")
    
    # Test normpath
    test_path = r"C:\Users\test\file.xlsx"
    normalized = os.path.normpath(test_path)
    print(f"\nPath normalization test:")
    print(f"  Original: {test_path}")
    print(f"  Normalized: {normalized}")
    
    # Test path splitting
    base_name = os.path.splitext(template_file)[0]
    output_path = f"{base_name}_updated.xlsx"
    print(f"\nOutput path generation:")
    print(f"  Base name: {base_name}")
    print(f"  Output path: {output_path}")
    
    print("\n" + "="*50)
    print("Path compatibility test complete!")
    
    # Import the main module to check for syntax errors
    try:
        import enrollment_automation_tier_reconciled
        print("\n✓ Main module imports successfully")
    except Exception as e:
        print(f"\n✗ Error importing main module: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = test_paths()
    sys.exit(0 if success else 1)