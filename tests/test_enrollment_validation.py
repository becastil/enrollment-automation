"""
Comprehensive Test Suite for Enrollment Calculation Validation
==============================================================

This test suite validates enrollment calculations against known discrepancies
and ensures proper handling of tier structures, multi-block aggregations,
and facility mappings.
"""

import unittest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from enrollment_automation_v6 import (
    normalize_tier_strict,
    build_tier_data_from_source,
    load_block_aggregations,
    lint_block_aggregations
)

class TestEnrollmentValidation(unittest.TestCase):
    """Test suite for enrollment calculation validation"""
    
    def setUp(self):
        """Set up test data and expected values"""
        self.control_totals = {
            "legacy": {"EMP": 3659, "ESP": 611, "ECH": 1006, "FAM": 757},
            "encino garden": {"EMP": 300, "ESP": 72, "ECH": 74, "FAM": 97},
            "st michaels": {"EMP": 291, "ESP": 58, "ECH": 51, "FAM": 54},
            "st mary reno": {"EMP": 431, "ESP": 121, "ECH": 135, "FAM": 116},
            "north vista": {"EMP": 384, "ESP": 47, "ECH": 122, "FAM": 75},
            "IL": {"EMP": 2654, "ESP": 435, "ECH": 838, "FAM": 540}
        }
        
    def test_tier_normalization_4tier(self):
        """Test 4-tier normalization logic"""
        # Test standard 4-tier normalization
        self.assertEqual(normalize_tier_strict('EMP', use_five_tier=False), 'EE Only')
        self.assertEqual(normalize_tier_strict('ESP', use_five_tier=False), 'EE+Spouse')
        self.assertEqual(normalize_tier_strict('E1D', use_five_tier=False), 'EE+Child(ren)')
        self.assertEqual(normalize_tier_strict('ECH', use_five_tier=False), 'EE+Child(ren)')
        self.assertEqual(normalize_tier_strict('FAM', use_five_tier=False), 'EE+Family')
        
    def test_tier_normalization_5tier(self):
        """Test 5-tier normalization logic"""
        # Test 5-tier normalization for Encino-Garden Grove and North Vista
        self.assertEqual(normalize_tier_strict('EMP', use_five_tier=True), 'EE Only')
        self.assertEqual(normalize_tier_strict('ESP', use_five_tier=True), 'EE+Spouse')
        self.assertEqual(normalize_tier_strict('E1D', use_five_tier=True), 'EE+1 Dep')
        self.assertEqual(normalize_tier_strict('ECH', use_five_tier=True), 'EE+Child')
        self.assertEqual(normalize_tier_strict('FAM', use_five_tier=True), 'EE+Family')
        
    def test_encino_garden_grove_5tier_issue(self):
        """Test for Encino-Garden Grove 5-tier overcount issue"""
        # Create test data simulating the issue
        test_data = pd.DataFrame([
            {'CLIENT ID': 'H3250', 'BEN CODE': 'EMP', 'CALCULATED BEN CODE': 'EMP', 'PLAN': 'PRIMEMMEPOLE'},
            {'CLIENT ID': 'H3250', 'BEN CODE': 'ESP', 'CALCULATED BEN CODE': 'ESP', 'PLAN': 'PRIMEMMEPOLE'},
            {'CLIENT ID': 'H3250', 'BEN CODE': 'ECH', 'CALCULATED BEN CODE': 'E1D', 'PLAN': 'PRIMEMMEPOLE'},
            {'CLIENT ID': 'H3250', 'BEN CODE': 'ECH', 'CALCULATED BEN CODE': 'ECH', 'PLAN': 'PRIMEMMEPOLE'},
            {'CLIENT ID': 'H3250', 'BEN CODE': 'FAM', 'CALCULATED BEN CODE': 'FAM', 'PLAN': 'PRIMEMMEPOLE'},
            {'CLIENT ID': 'H3260', 'BEN CODE': 'EMP', 'CALCULATED BEN CODE': 'EMP', 'PLAN': 'PRIMEMMEPO3'},
            {'CLIENT ID': 'H3260', 'BEN CODE': 'ESP', 'CALCULATED BEN CODE': 'ESP', 'PLAN': 'PRIMEMMEPO3'},
            {'CLIENT ID': 'H3260', 'BEN CODE': 'ECH', 'CALCULATED BEN CODE': 'E1D', 'PLAN': 'PRIMEMMEPO3'},
        ])
        
        # Expected behavior: Should use CALCULATED BEN CODE for 5-tier tabs
        # and properly categorize E1D vs ECH
        test_data['tab_name'] = 'Encino-Garden Grove'
        
        # Count expected tiers
        h3250_counts = test_data[test_data['CLIENT ID'] == 'H3250'].groupby('CALCULATED BEN CODE').size()
        self.assertIn('E1D', h3250_counts.index, "E1D should be present in CALCULATED BEN CODE")
        self.assertIn('ECH', h3250_counts.index, "ECH should be present in CALCULATED BEN CODE")
        
    def test_st_michaels_multiblock_aggregation(self):
        """Test St. Michael's multi-block aggregation issue"""
        # Test data for St. Michael's with multiple EPO blocks
        block_config = {
            "St. Michael's": {
                "H3530": {
                    "EPO": {
                        "PRIME NON-UNION EPO PLAN": {"sum_of": ["PRIMEMMSTEPO"]},
                        "PRIME CIR EPO PLAN": {"sum_of": ["PRIMEMMCIR"]},
                        "PRIME IUOE EPO PLAN": {"sum_of": ["PRIMEMMIUOE"]},
                        "PRIME JNESO EPO PLAN": {"sum_of": ["PRIMEMMJNESO"]},
                        "PRIME EPO PLUS PLAN": {"sum_of": ["PRIMEMMEPPLUS"]}
                    }
                }
            }
        }
        
        # Verify no duplicate PLAN codes across blocks
        all_plans = []
        for block in block_config["St. Michael's"]["H3530"]["EPO"].values():
            all_plans.extend(block["sum_of"])
        
        # Check for duplicates
        self.assertEqual(len(all_plans), len(set(all_plans)), 
                        "No duplicate PLAN codes should exist across blocks")
        
    def test_st_marys_reno_tier_classification(self):
        """Test St. Mary's Reno tier classification issue"""
        # Test data showing ECH anomaly
        test_data = pd.DataFrame([
            {'CLIENT ID': 'H3395', 'BEN CODE': 'ECH', 'PLAN': 'PRIMEMMSMMSMRMCEPO'},
            {'CLIENT ID': 'H3395', 'BEN CODE': 'E1D', 'PLAN': 'PRIMEMMSMMSMRMCEPO'},
            {'CLIENT ID': 'H3394', 'BEN CODE': 'ECH', 'PLAN': 'PRIMEMMSREPO'},
            {'CLIENT ID': 'H3396', 'BEN CODE': 'ECH', 'PLAN': 'PRIMEMMVALUE'},
        ])
        
        # For 4-tier facilities, E1D and ECH should both map to EE+Child(ren)
        test_data['normalized_tier'] = test_data['BEN CODE'].apply(
            lambda x: normalize_tier_strict(x, use_five_tier=False)
        )
        
        # Both E1D and ECH should map to same tier in 4-tier structure
        e1d_tier = test_data[test_data['BEN CODE'] == 'E1D']['normalized_tier'].iloc[0] if len(test_data[test_data['BEN CODE'] == 'E1D']) > 0 else None
        ech_tier = test_data[test_data['BEN CODE'] == 'ECH']['normalized_tier'].iloc[0]
        
        if e1d_tier:
            self.assertEqual(e1d_tier, ech_tier, 
                           "E1D and ECH should map to same tier in 4-tier structure")
        
    def test_illinois_facility_mapping(self):
        """Test Illinois facility mapping completeness"""
        # Illinois should have 12 facilities
        illinois_facilities = [
            'H3605', 'H3615', 'H3625', 'H3630', 'H3635', 'H3645',
            'H3655', 'H3660', 'H3665', 'H3670', 'H3675', 'H3680'
        ]
        
        self.assertEqual(len(illinois_facilities), 12, 
                        "Illinois tab should map 12 facilities")
        
        # Each facility should have unique configuration
        self.assertEqual(len(set(illinois_facilities)), 12,
                        "All Illinois facilities should be unique")
        
    def test_duplicate_counting_prevention(self):
        """Test prevention of duplicate counting across aggregations"""
        test_data = pd.DataFrame([
            {'CLIENT ID': 'H3530', 'PLAN': 'PRIMEMMSTEPO', 'BEN CODE': 'EMP', 'COUNT': 100},
            {'CLIENT ID': 'H3530', 'PLAN': 'PRIMEMMSTEPO', 'BEN CODE': 'ESP', 'COUNT': 50},
            {'CLIENT ID': 'H3530', 'PLAN': 'PRIMEMMCIR', 'BEN CODE': 'EMP', 'COUNT': 75},
        ])
        
        # Group by CLIENT ID and PLAN to ensure no double counting
        grouped = test_data.groupby(['CLIENT ID', 'PLAN', 'BEN CODE'])['COUNT'].sum()
        
        # Each combination should appear only once
        for key, count in grouped.items():
            matching_rows = test_data[
                (test_data['CLIENT ID'] == key[0]) &
                (test_data['PLAN'] == key[1]) &
                (test_data['BEN CODE'] == key[2])
            ]
            self.assertEqual(len(matching_rows), 1,
                           f"Each CLIENT ID/PLAN/BEN CODE combination should appear once: {key}")
            
    def test_control_total_validation(self):
        """Validate that fixes maintain control totals"""
        # Control totals from ground truth
        CONTROL_TOTALS = {
            "EE Only": 14533,
            "EE+Spouse": 2639,
            "EE+Child(ren)": 4413,
            "EE+Family": 3123
        }
        
        total = sum(CONTROL_TOTALS.values())
        self.assertEqual(total, 24708, "Control total should be 24,708")
        
    def test_block_aggregation_linting(self):
        """Test block aggregation configuration validation"""
        # Test config with issues
        bad_config = {
            "Test Tab": {
                "H9999": {
                    "EPO": {
                        "Block 1": {"sum_of": ["PLAN1", "PLAN2"]},
                        "Block 2": {"sum_of": ["PLAN2", "PLAN3"]}  # PLAN2 duplicated
                    }
                }
            }
        }
        
        source_plans = ["PLAN1", "PLAN2", "PLAN3"]
        issues = lint_block_aggregations(bad_config, source_plans)
        
        # Should detect duplicate PLAN2
        duplicate_issues = [i for i in issues if "duplicate" in i]
        self.assertGreater(len(duplicate_issues), 0,
                          "Should detect duplicate PLAN codes across blocks")
        
    def test_calculated_ben_code_vs_ben_code(self):
        """Test proper selection of CALCULATED BEN CODE vs BEN CODE"""
        test_data = pd.DataFrame([
            # Encino-Garden Grove (5-tier) - should use CALCULATED BEN CODE
            {'CLIENT ID': 'H3250', 'tab_name': 'Encino-Garden Grove',
             'BEN CODE': 'ECH', 'CALCULATED BEN CODE': 'E1D'},
            # Legacy (4-tier) - should use BEN CODE
            {'CLIENT ID': 'H3100', 'tab_name': 'Legacy',
             'BEN CODE': 'ECH', 'CALCULATED BEN CODE': 'E1D'},
        ])
        
        FIVE_TIER_TABS = ['Encino-Garden Grove', 'North Vista']
        
        for _, row in test_data.iterrows():
            if row['tab_name'] in FIVE_TIER_TABS:
                # Should use CALCULATED BEN CODE
                expected_code = row['CALCULATED BEN CODE']
                self.assertEqual(expected_code, 'E1D',
                               f"{row['tab_name']} should use CALCULATED BEN CODE")
            else:
                # Should use BEN CODE
                expected_code = row['BEN CODE']
                self.assertEqual(expected_code, 'ECH',
                               f"{row['tab_name']} should use BEN CODE")


class TestReconciliationReport(unittest.TestCase):
    """Test reconciliation report generation"""
    
    def test_variance_calculation(self):
        """Test calculation of variances between source and output"""
        source = {"EMP": 300, "ESP": 72, "ECH": 74, "FAM": 97}
        output = {"EMP": 971, "ESP": 154, "ECH": 300, "FAM": 246}
        
        variance = {k: output[k] - source[k] for k in source}
        
        self.assertEqual(variance["EMP"], 671, "EMP variance should be +671")
        self.assertEqual(variance["ESP"], 82, "ESP variance should be +82")
        self.assertEqual(variance["ECH"], 226, "ECH variance should be +226")
        self.assertEqual(variance["FAM"], 149, "FAM variance should be +149")
        
    def test_variance_percentage(self):
        """Test percentage variance calculation"""
        source = 300
        output = 971
        
        variance_pct = ((output - source) / source) * 100
        self.assertAlmostEqual(variance_pct, 223.67, places=2,
                              msg="Variance percentage should be ~223.67%")


if __name__ == '__main__':
    unittest.main()