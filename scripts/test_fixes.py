#!/usr/bin/env python3
"""
Simple test script to validate that enrollment fixes are working
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from enrollment_automation_v6 import (
    normalize_tier_strict,
    lint_block_aggregations,
    load_block_aggregations
)

def test_5tier_normalization():
    """Test that 5-tier normalization works correctly"""
    print("Testing 5-tier normalization...")
    
    # Test 4-tier mode
    assert normalize_tier_strict('EMP', use_five_tier=False) == 'EE Only'
    assert normalize_tier_strict('E1D', use_five_tier=False) == 'EE+Child(ren)'
    assert normalize_tier_strict('ECH', use_five_tier=False) == 'EE+Child(ren)'
    
    # Test 5-tier mode
    assert normalize_tier_strict('EMP', use_five_tier=True) == 'EE Only'
    assert normalize_tier_strict('E1D', use_five_tier=True) == 'EE+1 Dep'
    assert normalize_tier_strict('ECH', use_five_tier=True) == 'EE+Child'
    
    print("✅ 5-tier normalization tests passed")

def test_block_validation():
    """Test that block aggregation validation works"""
    print("\nTesting block aggregation validation...")
    
    # Load actual config
    block_config = load_block_aggregations()
    
    # Create sample source plans
    source_plans = ['PRIMEMMSTEPO', 'PRIMEMMCIR', 'PRIMEMMIUOE', 'PRIMEMMJNESO', 'PRIMEMMEPPLUS']
    
    # Run validation
    issues = lint_block_aggregations(block_config, source_plans)
    
    # Check for critical issues
    critical_issues = [i for i in issues if "CRITICAL" in i or "duplicate" in i]
    
    if critical_issues:
        print("❌ Found critical issues:")
        for issue in critical_issues:
            print(f"   - {issue}")
    else:
        print("✅ No critical block aggregation issues found")
    
    return len(critical_issues) == 0

def main():
    print("="*60)
    print("TESTING ENROLLMENT FIXES")
    print("="*60)
    
    # Run tests
    test_5tier_normalization()
    block_valid = test_block_validation()
    
    print("\n" + "="*60)
    if block_valid:
        print("✅ ALL TESTS PASSED")
    else:
        print("⚠️  SOME TESTS FAILED - Review issues above")
    print("="*60)
    
    return 0 if block_valid else 1

if __name__ == "__main__":
    sys.exit(main())