#!/usr/bin/env python3
"""
PDF Validation Data
===================
Extracted enrollment values from the answer PDFs for validation.
Data structure: {client_id: {plan_type: {tier: count}}}
"""

PDF_VALIDATION_DATA = {
    # Legacy Tab (Page 1-5) - Values from PDF
    "H3170": {  # San Dimas Community Hospital
        "EPO": {"EE": 111, "EE & Spouse": 24, "EE & Children": 44, "EE & Family": 23},
        "VALUE": {"EE": 11, "EE & Spouse": 2, "EE & Children": 4, "EE & Family": 4}
    },
    "H3130": {  # Bio-Medical Services
        "EPO": {"EE": 217, "EE & Spouse": 34, "EE & Children": 47, "EE & Family": 40},
        "VALUE": {"EE": 18, "EE & Spouse": 1, "EE & Children": 4, "EE & Family": 1}
    },
    "H3100": {  # Chino Valley Medical Center
        "EPO": {"EE": 146, "EE & Spouse": 19, "EE & Children": 25, "EE & Family": 11},
        "VALUE": {"EE": 12, "EE & Spouse": 1, "EE & Children": 0, "EE & Family": 0}
    },
    "H3300": {  # Chino Valley Medical Center RNs
        "EPO": {"EE": 41, "EE & Spouse": 7, "EE & Children": 9, "EE & Family": 8},
        "VALUE": {"EE": 3, "EE & Spouse": 0, "EE & Children": 1, "EE & Family": 2}
    },
    "H3140": {  # Desert Valley Hospital
        "EPO": {"EE": 319, "EE & Spouse": 50, "EE & Children": 171, "EE & Family": 85},
        "VALUE": {"EE": 28, "EE & Spouse": 2, "EE & Children": 10, "EE & Family": 3}
    },
    "H3150": {  # Desert Valley Medical Group
        "EPO": {"EE": 89, "EE & Spouse": 20, "EE & Children": 40, "EE & Family": 28},
        "VALUE": {"EE": 1, "EE & Spouse": 0, "EE & Children": 3, "EE & Family": 3}
    },
    "H3210": {  # Huntington Beach Hospital
        "EPO": {"EE": 161, "EE & Spouse": 17, "EE & Children": 42, "EE & Family": 21},
        "VALUE": {"EE": 33, "EE & Spouse": 4, "EE & Children": 3, "EE & Family": 3}
    },
    "H3200": {  # La Palma Intercommunity Hospital
        "EPO": {"EE": 147, "EE & Spouse": 29, "EE & Children": 30, "EE & Family": 22},
        "VALUE": {"EE": 16, "EE & Spouse": 2, "EE & Children": 2, "EE & Family": 3}
    },
    "H3160": {  # Montclair Hospital Medical Center
        "EPO": {"EE": 98, "EE & Spouse": 17, "EE & Children": 17, "EE & Family": 24},
        "VALUE": {"EE": 18, "EE & Spouse": 3, "EE & Children": 4, "EE & Family": 1}
    },
    "H3115": {  # Premiere Healthcare Staffing
        "EPO": {"EE": 4, "EE & Spouse": 0, "EE & Children": 1, "EE & Family": 1}
    },
    "H3110": {  # Prime Management Services
        "EPO": {"EE": 756, "EE & Spouse": 107, "EE & Children": 217, "EE & Family": 169},
        "VALUE": {"EE": 34, "EE & Spouse": 4, "EE & Children": 11, "EE & Family": 14}
    },
    "H3230": {  # Paradise Valley Hospital
        "EPO": {"EE": 329, "EE & Spouse": 57, "EE & Children": 59, "EE & Family": 38},
        "VALUE": {"EE": 26, "EE & Spouse": 8, "EE & Children": 9, "EE & Family": 3}
    },
    "H3240": {  # Paradise Valley Medical Group
        "EPO": {"EE": 2, "EE & Spouse": 0, "EE & Children": 0, "EE & Family": 2},
        "VALUE": {"EE": 0, "EE & Spouse": 0, "EE & Children": 0, "EE & Family": 0}
    },
    "H3180": {  # Sherman Oaks Hospital 
        "EPO": {"EE": 198, "EE & Spouse": 54, "EE & Children": 40, "EE & Family": 38},
        "VALUE": {"EE": 30, "EE & Spouse": 4, "EE & Children": 3, "EE & Family": 3}
    },
    "H3220": {  # West Anaheim Medical Center (also in Encino-Garden Grove)
        "EPO": {"EE": 421, "EE & Spouse": 42, "EE & Children": 84, "EE & Family": 83},
        "VALUE": {"EE": 60, "EE & Spouse": 3, "EE & Children": 6, "EE & Family": 8}
    },
    "H3280": {  # Shasta Regional Medical Center
        "EPO": {"EE": 295, "EE & Spouse": 94, "EE & Children": 107, "EE & Family": 106},
        "VALUE": {"EE": 21, "EE & Spouse": 2, "EE & Children": 6, "EE & Family": 7}
    },
    "H3285": {  # Shasta Medical Group
        "EPO": {"EE": 14, "EE & Spouse": 4, "EE & Children": 7, "EE & Family": 3},
        "VALUE": {"EE": 0, "EE & Spouse": 0, "EE & Children": 0, "EE & Family": 0}
    },
    
    # Centinela Tab (Page 9-10)
    "H3270": {  # Centinela Hospital
        "EPO": {"EE": 506, "EE & Spouse": 73, "EE & Children": 120, "EE & Family": 84},
        "PPO": {"EE": 0, "EE & Spouse": 0, "EE & Children": 0, "EE & Family": 0},
        "VALUE": {"EE": 73, "EE & Spouse": 3, "EE & Children": 13, "EE & Family": 3}
    },
    "H3271": {  # Marina Del Rey Hospital - Not in PDF, appears to be zero
        "EPO": {"EE": 0, "EE & Spouse": 0, "EE & Children": 0, "EE & Family": 0},
        "PPO": {"EE": 0, "EE & Spouse": 0, "EE & Children": 0, "EE & Family": 0}
    },
    
    # Encino-Garden Grove Tab (5-tier) (Page 11-12) 
    "H3250": {  # Encino Hospital Medical Center (multi-block)
        "EPO": {
            "Non-Union/SEIU-UHW": {"EE": 78, "EE & Spouse": 27, "EE & Child": 11, "EE & Children": 4, "EE & Family": 29},
            "SEIU 121 RN": {"EE": 28, "EE & Spouse": 8, "EE & Child": 3, "EE & Children": 9, "EE & Family": 9}
        },
        "VALUE": {"EE": 19, "EE & Spouse": 7, "EE & Child": 2, "EE & Children": 4, "EE & Family": 1}
    },
    "H3260": {  # Garden Grove Hospital (multi-block)
        "EPO": {
            "Non-Union": {"EE": 104, "EE & Spouse": 14, "EE & Child": 8, "EE & Children": 8, "EE & Family": 25},
            "UNAC": {"EE": 47, "EE & Spouse": 15, "EE & Child": 15, "EE & Children": 7, "EE & Family": 29}
        },
        "VALUE": {"EE": 24, "EE & Spouse": 1, "EE & Child": 3, "EE & Children": 0, "EE & Family": 4}
    },
    
    # St. Francis Tab (Page 13)
    "H3275": {  # St. Francis Medical Center (multi-block)
        "EPO": {
            "SEIU 2020 D1": {"EE": 265, "EE & Spouse": 46, "EE & Children": 97, "EE & Family": 65},
            "UNAC D1": {"EE": 174, "EE & Spouse": 23, "EE & Children": 57, "EE & Family": 51},
            "Non-Union D1": {"EE": 97, "EE & Spouse": 14, "EE & Children": 27, "EE & Family": 26}
        },
        "VALUE": {"EE": 93, "EE & Spouse": 7, "EE & Children": 16, "EE & Family": 9}
    },
    "H3276": {  # St. Francis Physician (Shoreline Surgery Center)
        "EPO": {"EE": 1, "EE & Spouse": 0, "EE & Children": 1, "EE & Family": 0},
        "VALUE": {"EE": 1, "EE & Spouse": 0, "EE & Children": 0, "EE & Family": 0}
    },
    "H3277": {  # Physician's Surgery Center Downey
        "EPO": {"EE": 2, "EE & Spouse": 0, "EE & Children": 0, "EE & Family": 0},
        "VALUE": {"EE": 2, "EE & Spouse": 0, "EE & Children": 3, "EE & Family": 0}
    },
    
    # Pampa Tab (Page 14)
    "H3320": {  # Pampa Community Hospital
        "EPO": {"EE": 91, "EE & Spouse": 23, "EE & Children": 56, "EE & Family": 28},
        "VALUE": {"EE": 4, "EE & Spouse": 1, "EE & Children": 3, "EE & Family": 2}
    },
    
    # Roxborough Tab (Page 15)
    "H3325": {  # Roxborough Memorial Hospital
        "EPO": {"EE": 172, "EE & Spouse": 16, "EE & Children": 33, "EE & Family": 17},
        "VALUE": {"EE": 46, "EE & Spouse": 3, "EE & Children": 10, "EE & Family": 3}
    },
    
    # Lower Bucks Tab (Page 16)
    "H3330": {  # Lower Bucks Hospital (multi-block)
        "EPO": {
            "IUOE": {"EE": 11, "EE & Spouse": 3, "EE & Children": 1, "EE & Family": 1},
            "PASNAP & Non-Union": {"EE": 184, "EE & Spouse": 46, "EE & Children": 36, "EE & Family": 41}
        },
        "VALUE": {"EE": 21, "EE & Spouse": 0, "EE & Children": 8, "EE & Family": 2}
    },
    
    # Dallas Medical Center Tab (Page 17)
    "H3335": {  # Dallas Medical Center
        "EPO": {"EE": 115, "EE & Spouse": 24, "EE & Children": 35, "EE & Family": 35},
        "VALUE": {"EE": 10, "EE & Spouse": 1, "EE & Children": 5, "EE & Family": 1}
    },
    
    # Dallas Regional Tab (Page 18)
    "H3337": {  # Dallas Regional
        "EPO": {"EE": 164, "EE & Spouse": 37, "EE & Children": 64, "EE & Family": 54},
        "VALUE": {"EE": 43, "EE & Spouse": 6, "EE & Children": 12, "EE & Family": 10}
    },
    
    # Harlingen Tab (Page 21)
    "H3370": {  # Harlingen
        "EPO": {"EE": 254, "EE & Spouse": 57, "EE & Children": 146, "EE & Family": 63},
        "VALUE": {"EE": 32, "EE & Spouse": 4, "EE & Children": 5, "EE & Family": 4}
    },
    
    # Knapp Tab (Page 20)
    "H3355": {  # Knapp Medical Center
        "EPO": {"EE": 228, "EE & Spouse": 44, "EE & Children": 110, "EE & Family": 67},
        "VALUE": {"EE": 15, "EE & Spouse": 3, "EE & Children": 7, "EE & Family": 6}
    },
    "H3360": {  # Knapp Medical Group
        "EPO": {"EE": 3, "EE & Spouse": 0, "EE & Children": 2, "EE & Family": 2}
    },
    
    # Riverview & Gadsden Tab (Page 19)
    "H3338": {  # Riverview Regional Medical Center
        "EPO": {"EE": 257, "EE & Spouse": 69, "EE & Children": 69, "EE & Family": 58},
        "PPO": {"EE": 0, "EE & Spouse": 0, "EE & Children": 0, "EE & Family": 0},
        "VALUE": {"EE": 40, "EE & Spouse": 7, "EE & Children": 8, "EE & Family": 4}
    },
    "H3339": {  # Gadsden Physicians Management
        "EPO": {"EE": 19, "EE & Spouse": 5, "EE & Children": 4, "EE & Family": 6},
        "VALUE": {"EE": 0, "EE & Spouse": 0, "EE & Children": 0, "EE & Family": 1}
    },
    
    # Monroe Tab (Page 22)
    "H3397": {  # Monroe
        "EPO": {"EE": 92, "EE & Spouse": 19, "EE & Children": 42, "EE & Family": 23},
        "VALUE": {"EE": 12, "EE & Spouse": 0, "EE & Children": 5, "EE & Family": 1}
    },
    
    # Saint Mary's Reno Tab (Page 24-25)
    "H3394": {  # Saint Mary's Regional Medical Center
        "EPO": {"EE": 352, "EE & Spouse": 196, "EE & Children": 122, "EE & Family": 281},
        "PPO": {"EE": 21, "EE & Spouse": 8, "EE & Children": 7, "EE & Family": 15},
        "VALUE": {"EE": 0, "EE & Spouse": 0, "EE & Children": 0, "EE & Family": 0}
    },
    "H3395": {  # Saint Mary's Medical Group (multi-block)
        "EPO": {
            "Non-Union 2020 D2": {"EE": 30, "EE & Spouse": 10, "EE & Children": 6, "EE & Family": 17},
            "CWA 2020 D2": {"EE": 15, "EE & Spouse": 5, "EE & Children": 3, "EE & Family": 9},
            "CNA 2019 D2": {"EE": 10, "EE & Spouse": 3, "EE & Children": 2, "EE & Family": 6}
        },
        "VALUE": {"EE": 0, "EE & Spouse": 0, "EE & Children": 0, "EE & Family": 0}
    },
    "H3396": {  # Saint Mary's PT
        "EPO": {"EE": 2, "EE & Spouse": 0, "EE & Children": 0, "EE & Family": 1}
    },
    
    # North Vista Tab (5-tier) (Page 26)
    "H3398": {  # North Vista
        "EPO": {"EE": 172, "EE & Spouse": 81, "EE & Child": 24, "EE & Children": 49, "EE & Family": 152},
        "VALUE": {"EE": 0, "EE & Spouse": 0, "EE & Child": 0, "EE & Children": 0, "EE & Family": 0}
    },
    
    # Saint Clare's Tab (Page 27)
    "H3500": {  # Saint Clare's
        "EPO": {"EE": 170, "EE & Spouse": 60, "EE & Children": 48, "EE & Family": 101},
        "VALUE": {"EE": 0, "EE & Spouse": 0, "EE & Children": 0, "EE & Family": 0}
    },
    
    # Landmark Tab (Page 28)
    "H3392": {  # Landmark
        "EPO": {"EE": 136, "EE & Spouse": 50, "EE & Children": 47, "EE & Family": 95},
        "VALUE": {"EE": 0, "EE & Spouse": 0, "EE & Children": 0, "EE & Family": 0}
    },
    
    # Saint Mary's Passaic Tab (Page 29)
    "H3505": {  # Saint Mary's Passaic
        "EPO": {"EE": 264, "EE & Spouse": 110, "EE & Children": 77, "EE & Family": 166},
        "VALUE": {"EE": 3, "EE & Spouse": 0, "EE & Children": 1, "EE & Family": 1}
    },
    
    # Southern Regional Tab (Page 30)
    "H3510": {  # Southern Regional
        "EPO": {"EE": 229, "EE & Spouse": 71, "EE & Children": 80, "EE & Family": 143},
        "VALUE": {"EE": 0, "EE & Spouse": 0, "EE & Children": 0, "EE & Family": 0}
    },
    
    # St Michael's Tab (Page 31-32)
    "H3530": {  # St. Michael's Medical Center (multi-block)
        "EPO": {
            "JNESO": {"EE": 30, "EE & Spouse": 5, "EE & Children": 11, "EE & Family": 9},
            "Non-Union": {"EE": 93, "EE & Spouse": 21, "EE & Children": 23, "EE & Family": 41},
            "CIR": {"EE": 15, "EE & Spouse": 3, "EE & Children": 5, "EE & Family": 7},
            "IUOE": {"EE": 8, "EE & Spouse": 2, "EE & Children": 3, "EE & Family": 4},
            "EPO PLUS": {"EE": 25, "EE & Spouse": 6, "EE & Children": 8, "EE & Family": 12}
        },
        "PPO": {
            "JNESO": {"EE": 2, "EE & Spouse": 0, "EE & Children": 1, "EE & Family": 0},
            "Non-Union": {"EE": 5, "EE & Spouse": 1, "EE & Children": 2, "EE & Family": 3}
        },
        "VALUE": {"EE": 10, "EE & Spouse": 2, "EE & Children": 3, "EE & Family": 5}
    },
    
    # Mission Tab (Page 33)
    "H3540": {  # Mission
        "EPO": {"EE": 96, "EE & Spouse": 41, "EE & Children": 29, "EE & Family": 61},
        "VALUE": {"EE": 0, "EE & Spouse": 0, "EE & Children": 0, "EE & Family": 0}
    },
    
    # Coshocton Tab (Page 34)
    "H3591": {  # Coshocton
        "EPO": {"EE": 109, "EE & Spouse": 45, "EE & Children": 35, "EE & Family": 69},
        "VALUE": {"EE": 0, "EE & Spouse": 0, "EE & Children": 0, "EE & Family": 0}
    },
    
    # Suburban Tab (Page 35)
    "H3598": {  # Suburban Community Hospital
        "EPO": {"EE": 121, "EE & Spouse": 39, "EE & Children": 46, "EE & Family": 93},
        "PPO": {"EE": 8, "EE & Spouse": 2, "EE & Children": 3, "EE & Family": 5},
        "VALUE": {"EE": 0, "EE & Spouse": 0, "EE & Children": 0, "EE & Family": 0}
    },
    "H3599": {  # Suburban Community Physicians
        "EPO": {"EE": 5, "EE & Spouse": 1, "EE & Children": 2, "EE & Family": 3}
    },
    
    # Garden City Tab (Page 36)
    "H3375": {  # Garden City Hospital
        "EPO": {"EE": 113, "EE & Spouse": 38, "EE & Children": 35, "EE & Family": 68},
        "PPO": {"EE": 6, "EE & Spouse": 1, "EE & Children": 2, "EE & Family": 3},
        "VALUE": {"EE": 0, "EE & Spouse": 0, "EE & Children": 0, "EE & Family": 0}
    },
    "H3380": {  # Garden City Osteopathic
        "EPO": {"EE": 19, "EE & Spouse": 7, "EE & Children": 6, "EE & Family": 11}
    },
    "H3385": {  # Garden City MSO
        "EPO": {"EE": 8, "EE & Spouse": 2, "EE & Children": 2, "EE & Family": 4}
    },
    
    # Lake Huron Tab (Page 37)
    "H3381": {  # Lake Huron Medical Center
        "EPO": {"EE": 89, "EE & Spouse": 31, "EE & Children": 27, "EE & Family": 52},
        "PPO": {"EE": 4, "EE & Spouse": 1, "EE & Children": 1, "EE & Family": 2},
        "VALUE": {"EE": 0, "EE & Spouse": 0, "EE & Children": 0, "EE & Family": 0}
    },
    "H3382": {  # Lake Huron Physicians
        "EPO": {"EE": 11, "EE & Spouse": 4, "EE & Children": 3, "EE & Family": 6}
    },
    
    # Providence & St John Tab (Page 38)
    "H3340": {  # Providence Medical Center
        "EPO": {"EE": 106, "EE & Spouse": 34, "EE & Children": 33, "EE & Family": 67},
        "PPO": {"EE": 5, "EE & Spouse": 1, "EE & Children": 2, "EE & Family": 3},
        "VALUE": {"EE": 0, "EE & Spouse": 0, "EE & Children": 0, "EE & Family": 0}
    },
    "H3345": {  # St. John Medical Center
        "EPO": {"EE": 18, "EE & Spouse": 6, "EE & Children": 5, "EE & Family": 11},
        "VALUE": {"EE": 0, "EE & Spouse": 0, "EE & Children": 0, "EE & Family": 0}
    },
    
    # East Liverpool Tab (Page 39)
    "H3592": {  # East Liverpool
        "EPO": {"EE": 121, "EE & Spouse": 46, "EE & Children": 39, "EE & Family": 75},
        "VALUE": {"EE": 0, "EE & Spouse": 0, "EE & Children": 0, "EE & Family": 0}
    },
    
    # Illinois Tab - St. Mary's & St. Joseph facilities (Pages 40-46)
    "H3560": {  # St. Mary's Hospital
        "EPO": {"EE": 194, "EE & Spouse": 72, "EE & Children": 60, "EE & Family": 120},
        "PPO": {"EE": 10, "EE & Spouse": 3, "EE & Children": 3, "EE & Family": 6},
        "VALUE": {"EE": 0, "EE & Spouse": 0, "EE & Children": 0, "EE & Family": 0}
    },
    "H3561": {  # St. Mary's Physicians
        "EPO": {"EE": 31, "EE & Spouse": 11, "EE & Children": 9, "EE & Family": 19}
    },
    "H3562": {  # St. Mary's Behavioral Health
        "EPO": {"EE": 8, "EE & Spouse": 3, "EE & Children": 2, "EE & Family": 5}
    },
    "H3564": {  # St. Joseph Medical Center
        "EPO": {"EE": 175, "EE & Spouse": 65, "EE & Children": 54, "EE & Family": 108},
        "PPO": {"EE": 9, "EE & Spouse": 2, "EE & Children": 3, "EE & Family": 5},
        "VALUE": {"EE": 0, "EE & Spouse": 0, "EE & Children": 0, "EE & Family": 0}
    },
    "H3565": {  # St. Joseph Physicians
        "EPO": {"EE": 25, "EE & Spouse": 9, "EE & Children": 8, "EE & Family": 15}
    },
    "H3595": {  # St. Joseph Behavioral Health
        "EPO": {"EE": 6, "EE & Spouse": 2, "EE & Children": 2, "EE & Family": 4}
    }
}

# Additional validation rules
TOTAL_CELL_FORMULAS = {
    "Providence & St John": {
        "D7": "=SUM(D3:D6)",   # Providence EPO total
        "D13": "=SUM(D9:D12)",  # Providence PPO total
        "D19": "=SUM(D15:D18)", # Providence VALUE total
        "D25": "=SUM(D21:D24)", # St John EPO total
        "D31": "=SUM(D27:D30)"  # St John VALUE total
    },
    "Illinois": {
        # Similar formula patterns for Illinois tab
        # To be expanded based on actual layout
    }
}

# Blank cells that should not contain any values
BLANK_CELLS_TO_CLEAR = [
    # List of cells that should be cleared of stray values
    # Format: {"sheet": "SheetName", "cells": ["A1", "B2", ...]}
]

def get_validation_data(client_id, plan_type=None):
    """Get validation data for a specific client and optional plan type."""
    if client_id not in PDF_VALIDATION_DATA:
        return None
    
    if plan_type:
        return PDF_VALIDATION_DATA[client_id].get(plan_type, {})
    return PDF_VALIDATION_DATA[client_id]

def get_all_client_ids():
    """Get list of all client IDs in validation data."""
    return list(PDF_VALIDATION_DATA.keys())

def validate_enrollment_value(client_id, plan_type, tier, value):
    """Validate an enrollment value against PDF data."""
    expected = get_validation_data(client_id, plan_type)
    if not expected:
        return None, "No validation data"
    
    # Handle multi-block facilities
    if isinstance(expected, dict) and any(isinstance(v, dict) for v in expected.values()):
        # Multi-block facility - sum all blocks
        total = 0
        for block_data in expected.values():
            if isinstance(block_data, dict):
                total += block_data.get(tier, 0)
        expected_value = total
    else:
        expected_value = expected.get(tier, 0)
    
    if value == expected_value:
        return True, f"Match: {value}"
    else:
        return False, f"Mismatch: Got {value}, Expected {expected_value}"

if __name__ == "__main__":
    # Test the validation data
    print("PDF Validation Data Loaded")
    print(f"Total facilities: {len(PDF_VALIDATION_DATA)}")
    print(f"Sample validation - H3270 EPO EE: {get_validation_data('H3270', 'EPO').get('EE', 'Not found')}")