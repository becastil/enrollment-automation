#!/usr/bin/env python3
"""
Test Windows Path Compatibility
================================

This script tests that the path handling works correctly on Windows.
"""

import os
import platform

def test_path_handling():
    """Test that paths are handled correctly based on OS"""
    
    print("\n" + "="*50)
    print("PATH COMPATIBILITY TEST")
    print("="*50)
    
    # Detect OS
    system = platform.system()
    print(f"\nDetected OS: {system}")
    print(f"Python version: {platform.python_version()}")
    
    # Test paths based on OS
    if system == 'Windows':
        print("\nRunning on Windows")
        
        # Windows paths
        paths_to_test = [
            r"C:\Users\becas\Prime_EFR\data\input\source_data.xlsx",
            r"C:\Users\becas\Prime_EFR\Prime Enrollment Funding by Facility for August.xlsx",
        ]
    else:
        print("\nRunning on Linux/WSL")
        
        # WSL/Linux paths
        paths_to_test = [
            "/mnt/c/Users/becas/Prime_EFR/data/input/source_data.xlsx",
            "/mnt/c/Users/becas/Prime_EFR/Prime Enrollment Funding by Facility for August.xlsx",
        ]
    
    print("\nTesting file existence:")
    for path in paths_to_test:
        exists = os.path.exists(path)
        status = "✓ Found" if exists else "✗ Not found"
        print(f"  {status}: {path}")
    
    # Test path normalization
    print("\nPath normalization test:")
    test_path = "C:\\Users\\becas\\Prime_EFR\\data\\input\\source_data.xlsx"
    normalized = os.path.normpath(test_path)
    print(f"  Original:   {test_path}")
    print(f"  Normalized: {normalized}")
    
    # Test path joining
    print("\nPath joining test:")
    base = "C:\\Users\\becas\\Prime_EFR" if system == 'Windows' else "/mnt/c/Users/becas/Prime_EFR"
    joined = os.path.join(base, 'output', 'test.xlsx')
    print(f"  Base:   {base}")
    print(f"  Joined: {joined}")
    
    print("\n" + "="*50)
    print("TEST COMPLETE")
    print("="*50)
    
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(test_path_handling())