import pandas as pd
import numpy as np
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
import warnings
import traceback
warnings.filterwarnings('ignore')

# TPA Code (Client ID) to Facility Name mapping - used for automatic lookups
TPA_TO_FACILITY = {
    'H3100': 'Chino Valley Medical Center',
    'H3105': 'Glendora Community Hospital',
    'H3110': 'Prime Management',
    'H3115': 'Premiere Healthcare Staffing, LLC',
    'H3120': 'Hospital Business Service',
    'H3130': 'Bio Med Services',
    'H3140': 'Desert Valley Hospital',
    'H3150': 'Desert Valley Medical Group',
    'H3160': 'Montclair',
    'H3170': 'San Dimas',
    'H3180': 'Sherman Oaks',
    'H3190': 'Sherman Oaks Med. Group',
    'H3200': 'La Palma',
    'H3210': 'Huntington Beach',
    'H3220': 'West Anaheim',
    'H3230': 'Paradise Valley',
    'H3240': 'Paradise Valley Medical Grp',
    'H3250': 'Encino Hospital',
    'H3260': 'Garden Grove',
    'H3270': 'Centinela',
    'H3271': 'Robotics Outpatient Center',
    'H3272': 'Centinela Valley Endoscopy Center',
    'H3275': 'St. Francis Medical Center',
    'H3276': 'Shoreline Surgery Center',
    'H3277': "Physician's Surgery Center Downey",
    'H3280': 'Shasta Regional Medical Center',
    'H3285': 'Shasta Medical Group',
    'H3290': 'Hospitality',
    'H3300': "Chino RN's",
    'H3310': 'Alvarado Hospital',
    'H3320': 'Pampa',
    'H3325': 'Roxborough',
    'H3330': 'Lower Bucks',
    'H3335': 'Dallas Medical Center',
    'H3337': 'Dallas Regional Medical Center',
    'H3338': 'Riverview Regional Medical Center',
    'H3339': 'Gadsden Physicians Management',
    'H3340': 'Providence Medical Center',
    'H3345': 'St. John Hospital',
    'H3350': 'Providence Place, Inc.',
    'H3355': 'Knapp Medical Center',
    'H3360': 'Knapp Medical Group',
    'H3365': 'Knapp Ambulatory Surgery Center',
    'H3370': 'Harlingen Medical Center',
    'H3375': 'Garden City Hospital',
    'H3380': 'United Home Health Services',
    'H3381': 'Lake Huron Medical Center',
    'H3382': 'Lake Huron Medical Group',
    'H3385': 'Prime Garden City Medical Group',
    'H3390': 'Rehabilitation Hospital of Rhode Island',
    'H3392': 'Landmark Medical Center',
    'H3394': "Summit Surgery Center a St. Mary's Galena",
    'H3395': "St. Mary's Regional Medical Center",
    'H3396': "St. Mary's Medical Group",
    'H3397': 'Monroe Hospital',
    'H3398': 'North Vista Hospital',
    'H3399': 'North Vista Medical Group',
    'H3400': "St. Mary's Fitness Center",
    'H3500': "St Clare's Health System",
    'H3505': "Saint Mary's General Hospital",
    'H3510': 'Southern Medical Regional Center',
    'H3520': 'Lehigh Regional Medical Center',
    'H3530': "St. Michael's Medical Center",
    'H3540': 'Mission Regional Medical Center',
    'H3560': "St. Mary's Medical Center",
    'H3561': 'St. Joseph Medical Center',
    'H3562': 'South Kansas City Surgi Center',
    'H3563': 'CHCS Home Health Care',
    'H3564': 'CPCN Physicians Service',
    'H3565': 'CPCN Physicians Service (32) STJ',
    'H3566': "St. Mary's Surgical Center",
    'H3591': 'Coshocton County Memorial Hospital',
    'H3592': 'East Liverpool City Hospital',
    'H3593': 'Ohio Valley Home Health Care',
    'H3594': 'Ohio Valley Home Health Services',
    'H3595': 'River Valley Physicians',
    'H3598': 'Suburban Community Hospital',
    'H3599': 'Suburban Medical Group',
    'H3600': 'Reddy Development LLC',
    'H3605': 'Mercy Medical Center - Aurora LLC',
    'H3615': 'Resurrection Medical Center - Chicago LLC',
    'H3625': 'Saint Francis Hospital - Evanston LLC',
    'H3630': 'Saint Joseph Hospital - Elgin LLC',
    'H3635': 'Saint Joseph Hospital - Joliet LLC',
    'H3645': "St. Mary's Hospital - Kankakee, LLC",
    'H3655': 'Saint Mary of Nazareth Hospital - Chicago, LLC',
    'H3660': 'Holy Family Medical Center - Des Plaines LLC',
    'H3665': 'MedSpace Services, LLC',
    'H3670': 'Prime Healthcare Illinois Medical Group, LLC',
    'H3675': 'Prime Healthcare Home Care and Hospice',
    'H3680': 'Prime Healthcare Senior Living'
}

# TPA Code to Legacy flag mapping
TPA_TO_LEGACY = {
    'H3100': 'Yes', 'H3105': 'No', 'H3110': 'Yes', 'H3115': 'Yes', 'H3120': 'Yes',
    'H3130': 'Yes', 'H3140': 'Yes', 'H3150': 'Yes', 'H3160': 'Yes', 'H3170': 'Yes',
    'H3180': 'Yes', 'H3190': 'Yes', 'H3200': 'Yes', 'H3210': 'Yes', 'H3220': 'Yes',
    'H3230': 'Yes', 'H3240': 'Yes', 'H3250': 'No', 'H3260': 'No', 'H3270': 'No',
    'H3271': 'No', 'H3272': 'No', 'H3275': 'No', 'H3276': 'No', 'H3277': 'No',
    'H3280': 'Yes', 'H3285': 'Yes', 'H3290': 'Yes', 'H3300': 'Yes', 'H3310': 'No',
    'H3320': 'No', 'H3325': 'No', 'H3330': 'No', 'H3335': 'No', 'H3337': 'No',
    'H3338': 'No', 'H3339': 'No', 'H3340': 'No', 'H3345': 'No', 'H3350': 'No',
    'H3355': 'No', 'H3360': 'No', 'H3365': 'No', 'H3370': 'No', 'H3375': 'No',
    'H3380': 'No', 'H3381': 'No', 'H3382': 'No', 'H3385': 'No', 'H3390': 'No',
    'H3392': 'No', 'H3394': 'No', 'H3395': 'No', 'H3396': 'No', 'H3397': 'No',
    'H3398': 'No', 'H3399': 'No', 'H3400': 'No', 'H3500': 'No', 'H3505': 'No',
    'H3510': 'No', 'H3520': 'No', 'H3530': 'No', 'H3540': 'No', 'H3560': 'No',
    'H3561': 'No', 'H3562': 'No', 'H3563': 'No', 'H3564': 'No', 'H3565': 'No',
    'H3566': 'No', 'H3591': 'No', 'H3592': 'No', 'H3593': 'No', 'H3594': 'No',
    'H3595': 'No', 'H3598': 'No', 'H3599': 'No', 'H3600': 'No', 'H3605': 'No',
    'H3615': 'No', 'H3625': 'No', 'H3630': 'No', 'H3635': 'No', 'H3645': 'No',
    'H3655': 'No', 'H3660': 'No', 'H3665': 'No', 'H3670': 'No', 'H3675': 'No',
    'H3680': 'No'
}

# TPA Code to California flag mapping
TPA_TO_CALIFORNIA = {
    'H3100': 'Yes', 'H3105': 'Yes', 'H3110': 'Yes', 'H3115': 'Yes', 'H3120': 'Yes',
    'H3130': 'Yes', 'H3140': 'Yes', 'H3150': 'Yes', 'H3160': 'Yes', 'H3170': 'Yes',
    'H3180': 'Yes', 'H3190': 'Yes', 'H3200': 'Yes', 'H3210': 'Yes', 'H3220': 'Yes',
    'H3230': 'Yes', 'H3240': 'Yes', 'H3250': 'Yes', 'H3260': 'Yes', 'H3270': 'Yes',
    'H3271': 'Yes', 'H3272': 'Yes', 'H3275': 'Yes', 'H3276': 'Yes', 'H3277': 'Yes',
    'H3280': 'Yes', 'H3285': 'Yes', 'H3290': 'Yes', 'H3300': 'Yes', 'H3310': 'Yes',
    'H3320': 'No', 'H3325': 'No', 'H3330': 'No', 'H3335': 'No', 'H3337': 'No',
    'H3338': 'No', 'H3339': 'No', 'H3340': 'No', 'H3345': 'No', 'H3350': 'No',
    'H3355': 'No', 'H3360': 'No', 'H3365': 'No', 'H3370': 'No', 'H3375': 'No',
    'H3380': 'No', 'H3381': 'No', 'H3382': 'No', 'H3385': 'No', 'H3390': 'No',
    'H3392': 'No', 'H3394': 'No', 'H3395': 'No', 'H3396': 'No', 'H3397': 'No',
    'H3398': 'No', 'H3399': 'No', 'H3400': 'No', 'H3500': 'No', 'H3505': 'No',
    'H3510': 'No', 'H3520': 'No', 'H3530': 'No', 'H3540': 'No', 'H3560': 'No',
    'H3561': 'No', 'H3562': 'No', 'H3563': 'No', 'H3564': 'No', 'H3565': 'No',
    'H3566': 'No', 'H3591': 'No', 'H3592': 'No', 'H3593': 'No', 'H3594': 'No',
    'H3595': 'No', 'H3598': 'No', 'H3599': 'No', 'H3600': 'No', 'H3605': 'No',
    'H3615': 'No', 'H3625': 'No', 'H3630': 'No', 'H3635': 'No', 'H3645': 'No',
    'H3655': 'No', 'H3660': 'No', 'H3665': 'No', 'H3670': 'No', 'H3675': 'No',
    'H3680': 'No'
}

# Configuration: Map Client IDs to Facility Names and their tabs
FACILITY_MAPPING = {
    'Legacy': {
        'H3170': 'San Dimas Community Hospital',
        'H3130': 'Bio-Medical Services',
        'H3100': 'Chino Valley Medical Center',
        'H3300': 'Chino Valley Medical Center RNs',
        'H3140': 'Desert Valley Hospital',
        'H3150': 'Desert Valley Medical Group',
        'H3210': 'Huntington Beach Hospital',
        'H3200': 'La Palma Intercommunity Hospital',
        'H3160': 'Montclair Hospital Medical Center',
        'H3115': 'Premiere Healthcare Staffing',
        'H3110': 'Prime Management Services',
        'H3230': 'Paradise Valley Hospital',
        'H3240': 'Paradise Valley Medical Group',
        'H3180': 'Sherman Oaks Hospital',
        'H3190': 'Sherman Oaks Medical Group',
        'H3220': 'West Anaheim Medical Center',
        'H3285': 'Shasta Medical Group',
        'H3290': 'Hospitality'
    },
    'Centinela': {
        'H3270': 'Centinela Hospital Medical Center',
        'H3271': 'Robotics Outpatient Center',
        'H3272': 'Centinela Valley Endoscopy Center'
    },
    'Encino-Garden Grove': {
        'H3250': 'Encino Hospital Medical Center',
        'H3260': 'Garden Grove Hospital Medical Center'  # Including UNAC
    },
    'St. Francis': {
        'H3275': 'St. Francis Medical Center',
        'H3276': 'Shoreline Surgery Center',
        'H3277': "Physician's Surgery Center Downey"
    },
    'Pampa': {
        'H3320': 'Pampa Regional Medical Center'
    },
    'Roxborough': {
        'H3325': 'Roxborough Memorial Hospital'
    },
    'Lower Bucks': {
        'H3330': 'Lower Bucks Hospital'
    },
    'Dallas Medical Center': {
        'H3335': 'Dallas Medical Center'
    },
    'Harlingen': {
        'H3370': 'Harlingen Medical Center'
    },
    'Knapp': {
        'H3355': 'Knapp Medical Center',
        'H3360': 'Knapp Medical Group'
    },
    'Monroe': {
        'H3397': 'Monroe Hospital'
    },
    "Saint Mary's Reno": {
        'H3394': "Summit Surgery Center at St. Mary's Galena",
        'H3395': "Saint Mary's Regional Medical Center",
        'H3396': "Saint Mary's Medical Group",
        'H3400': "Saint Mary's Fitness Center"
    },
    'North Vista': {
        'H3398': 'North Vista Hospital',
        'H3399': 'North Vista Medical Group'
    },
    'Dallas Regional': {
        'H3337': 'Dallas Regional Medical Center'
    },
    'Riverview & Gadsden': {
        'H3338': 'Riverview Regional Medical Center',
        'H3339': 'Gadsden Physicians Management'
    },
    "Saint Clare's": {
        'H3500': "Saint Clare's Health System"
    },
    'Landmark': {
        'H3392': 'Landmark Medical Center'
    },
    "Saint Mary's Passaic": {
        'H3505': "Saint Mary's General Hospital - Passaic, NJ"
    },
    'Southern Regional': {
        'H3510': 'Southern Regional Medical Center'
    },
    "St Michael's": {
        'H3530': "St. Michael's Medical Center"
    },
    'Mission': {
        'H3540': 'Mission Regional Medical Center'
    },
    'Coshocton': {
        'H3591': 'Coshocton County Memorial Hospital'
    },
    'Suburban': {
        'H3598': 'Suburban Community Hospital',
        'H3599': 'Suburban Medical Group'
    },
    'Garden City': {
        'H3375': 'Garden City Hospital',
        'H3385': 'Garden City Medical Group',
        'H3380': 'United Home Health Services'
    },
    'Lake Huron': {
        'H3381': 'Lake Huron Medical Center',
        'H3382': 'Lake Huron Medical Group'
    },
    'Providence & St John': {
        'H3340': 'Providence Medical Center',
        'H3345': 'St. John Hospital'
    },
    'East Liverpool': {
        'H3592': 'East Liverpool City Hospital',
        'H3594': 'Ohio Valley Home Health Services',
        'H3595': 'River Valley Physicians'
    },
    'St Joe & St Mary\'s': {
        'H3560': "St. Mary's Medical Center",
        'H3561': 'St. Joseph Medical Center',
        'H3562': 'South Kansas City Surgical Center',
        'H3563': 'CHCS Home Health Care',
        'H3564': 'CPCN Physicians Service (30) STM',
        'H3565': 'CPCN Physicians Service (32) STJ',
        'H3566': "St. Mary's Surgical Center"
    },
    'Illinois': {
        'H3605': 'Mercy Medical Center - Aurora LLC',
        'H3615': 'Resurrection Medical Center - Chicago LLC',
        'H3625': 'Saint Francis Hospital - Evanston LLC',
        'H3630': 'Saint Joseph Hospital - Elgin LLC',
        'H3635': 'Saint Joseph Hospital - Joliet LLC',
        'H3645': "St. Mary's Hospital - Kankakee, LLC",
        'H3655': 'Saint Mary of Nazareth Hospital - Chicago, LLC',
        'H3660': 'Holy Family Medical Center',
        'H3665': 'MedSpace Services, LLC',
        'H3670': 'Prime Healthcare Illinois Medical Group, LLC',
        'H3675': 'Prime Healthcare Home Care and Hospice',
        'H3680': 'Prime Healthcare Senior Living'
    }
}

# Map PLAN codes to EPO/PPO/VALUE categories
PLAN_TO_TYPE = {
    'PRIMESFSE': 'EPO',
    'PRIMESFUN': 'EPO',
    'PRIMEMSFE': 'EPO',
    'PRIMEMMLMRI': 'VALUE',
    'PRIMEMMCV': 'EPO',
    'PRIMEMMGLN': 'EPO',
    'PRIMEMMEPOLE2': 'EPO',
    'PRIMEMMWA': 'EPO',
    'PRIMEMMCC': 'EPO',
    'PRIMEMMDAL': 'EPO',
    'PRIMEMMEL': 'EPO',
    'PRIMEMMELPOS': 'PPO',
    'PRIMEMMEPOCEN': 'EPO',
    'PRIMEMMEPOEA': 'EPO',
    'PRIMEMMEPOES': 'EPO',
    'PRIMEMMEPOLE': 'EPO',
    'PRIMEMMEPOPA': 'EPO',
    'PRIMEMMEPOROX': 'EPO',
    'PRIMEMMEPOUEE': 'EPO',
    'PRIMEMMGCH': 'EPO',
    'PRIMEMMHAR': 'EPO',
    'PRIMEMMKN': 'EPO',
    'PRIMEMMKNVAL': 'VALUE',
    'PRIMEMMKS': 'EPO',
    'PRIMEMMLB': 'EPO',
    'PRIMEMMLKEP1': 'EPO',
    'PRIMEMMLKEP2': 'EPO',
    'PRIMEMMLM': 'EPO',
    'PRIMEMMLR': 'EPO',
    'PRIMEMMMH': 'EPO',
    'PRIMEMMMR': 'EPO',
    'PRIMEMMNV': 'EPO',
    'PRIMEMMPLT': 'EPO',
    'PRIMEMMPMC': 'EPO',
    'PRIMEMMPPOEN': 'PPO',
    'PRIMEMMPPOLAP': 'PPO',
    'PRIMEMMPPOLHCEN': 'PPO',
    'PRIMEMMPPOLLCEN': 'PPO',
    'PRIMEMMPPOUH': 'PPO',
    'PRIMEMMPPOLH': 'PPO',
    'PRIMEMMPPOUL': 'PPO',
    'PRIMEMMRHRI': 'EPO',
    'PRIMEMMRV': 'EPO',
    'PRIMEMMSB': 'EPO',
    'PRIMEMMSBPLT': 'EPO',
    'PRIMEMMSJH': 'EPO',
    'PRIMEMMSM': 'EPO',
    'PRIMEMMSMMSMRMC': 'EPO',
    'PRIMEMMSMMSMRMCP': 'PPO',
    'PRIMEMMSR': 'EPO',
    'PRIMEMMSTCL': 'EPO',
    'PRIMEMMST': 'EPO',
    'PRIMEMMSTPPO': 'PPO',
    'PRIMEMMVAL': 'VALUE',
    'PRIMEMMSMECN': 'EPO',
    'PRIMEMMSMECW': 'EPO',
    'PRIMEMMCIR': 'EPO',
    'PRIMEMMIUOE': 'EPO',
    'PRIMEMMJNESO': 'EPO',
    'PRIMELBH': 'EPO',
    'PRIMEMMEPO3': 'EPO',
    'PRIMEMMEPOESU': 'EPO',
    'PRIMEMMEPOLEUN': 'EPO',
    'PRIMEMMEPPLUS': 'EPO',
    'PRIMEMMVALUE': 'VALUE',
    'PRIMEPOPRE21': 'EPO',
    'PRIMESFMCVAL': 'VALUE',
    'PRIMEASCIL': 'EPO',
    'PRIMEMMIL': 'VALUE',
    'PRIMEINAIL': 'EPO',
    'PRIMEINAILVALUE': 'VALUE',
    'PRIMEMMSMEPLUS': 'EPO',
    'PRIMEMMSMUN': 'EPO'
}

# Map the enrollment tiers based on CALCULATED BEN CODE
BEN_CODE_TO_TIER = {
    'EMP': 'EE',
    'ESP': 'EE & Spouse',
    'E1D': 'EE & Child',  # Employee + 1 dependent
    'ECH': 'EE & Children',  # Employee + multiple children
    'FAM': 'EE & Family'
}

def calculate_helper_columns(df):
    """
    Calculate CALCULATED_BEN_CODE based on family composition
    This determines the enrollment tier based on RELATION column
    """
    if 'EMPLOYEE NAME' not in df.columns and 'SEQ. #' in df.columns:
        # Use SEQ. # as a proxy for grouping if EMPLOYEE NAME is not available
        df['EMPLOYEE_GROUP'] = df['CLIENT ID'].astype(str) + '_' + df['SEQ. #'].astype(str)
    elif 'EMPLOYEE NAME' in df.columns:
        df['EMPLOYEE_GROUP'] = df['CLIENT ID'].astype(str) + '_' + df['EMPLOYEE NAME'].astype(str)
    else:
        # Fall back to using just CLIENT ID
        df['EMPLOYEE_GROUP'] = df['CLIENT ID'].astype(str)
    
    # Group by employee to determine family composition
    def determine_ben_code(group):
        relations = group['RELATION'].value_counts()
        
        # Check what relations exist
        has_self = 'SELF' in relations
        has_spouse = 'SPOUSE' in relations or 'SP' in relations
        child_count = relations.get('CHILD', 0) + relations.get('CH', 0) + relations.get('CHILDREN', 0)
        
        # Determine benefit code
        if has_self:
            if has_spouse and child_count > 0:
                return 'FAM'  # Employee + Spouse + Children
            elif has_spouse and child_count == 0:
                return 'ESP'  # Employee + Spouse only
            elif not has_spouse and child_count > 1:
                return 'ECH'  # Employee + multiple Children
            elif not has_spouse and child_count == 1:
                return 'E1D'  # Employee + 1 dependent (child)
            else:
                return 'EMP'  # Employee only
        else:
            return 'EMP'  # Default to employee only if no SELF found
    
    # Apply the function to each employee group
    ben_codes = df.groupby('EMPLOYEE_GROUP').apply(determine_ben_code)
    df['CALCULATED_BEN_CODE'] = df['EMPLOYEE_GROUP'].map(ben_codes)
    
    return df

def handle_list_data_with_explode(df):
    """
    Handle any list data in cells using explode
    """
    # Check for any columns that might contain lists
    for col in df.columns:
        if df[col].dtype == 'object':
            # Check if any values are lists
            sample = df[col].dropna().head(10)
            if any(isinstance(val, list) for val in sample):
                df = df.explode(col)
    return df

def reshape_enrollment_data(df):
    """
    Reshape enrollment data if needed (e.g., wide to long format)
    """
    # This function is a placeholder for any reshaping needs
    # The current data appears to be in the correct format already
    return df

def apply_group_transforms(df):
    """
    Add group statistics and transforms
    """
    # First ensure EMPLOYEE_GROUP exists
    if 'EMPLOYEE_GROUP' not in df.columns:
        df = calculate_helper_columns(df)
    
    if 'Location' in df.columns and 'EMPLOYEE_GROUP' in df.columns:
        # Add count of employees per facility
        df['facility_employee_count'] = df.groupby('Location')['EMPLOYEE_GROUP'].transform('nunique')
        
        # Add average family size per facility
        df['avg_family_size'] = df.groupby(['Location', 'EMPLOYEE_GROUP']).transform('size')
    
    return df

def handle_outliers_with_where(df):
    """
    Handle outliers using where for conditional operations
    """
    # Example: Flag unusual benefit codes
    if 'CALCULATED_BEN_CODE' in df.columns:
        valid_codes = ['EMP', 'ESP', 'E1D', 'ECH', 'FAM']
        df['valid_ben_code'] = df['CALCULATED_BEN_CODE'].isin(valid_codes)
        
        # Replace invalid codes with most common valid code
        if not df[df['valid_ben_code']]['CALCULATED_BEN_CODE'].empty:
            most_common = df[df['valid_ben_code']]['CALCULATED_BEN_CODE'].mode()[0]
            df['CALCULATED_BEN_CODE'] = df['CALCULATED_BEN_CODE'].where(
                df['valid_ben_code'], 
                most_common
            )
    
    return df

def read_source_data(file_path, legend_sheet='Legend'):
    """
    Read the source enrollment data and perform lookups
    """
    # Read main data
    df = pd.read_excel(file_path, sheet_name=0)  # Main data sheet
    
    # Find the column with Client IDs - prioritize CLIENT ID which has TPA codes
    id_column = None
    for col in ['CLIENT ID', 'CLIENT_ID', 'TPA Code', 'DEPT #']:
        if col in df.columns:
            id_column = col
            break
    
    if id_column:
        # Use .assign() to create multiple columns efficiently
        df = df.assign(
            Location=df[id_column].map(TPA_TO_FACILITY),
            Legacy=df[id_column].map(TPA_TO_LEGACY),
            California=df[id_column].map(TPA_TO_CALIFORNIA)
        )
        
        # Rename columns if needed for consistency
        if 'CA' in df.columns and 'California' not in df.columns:
            df.rename(columns={'CA': 'California'}, inplace=True)
        if 'LEGACY' in df.columns and 'Legacy' not in df.columns:
            df.rename(columns={'LEGACY': 'Legacy_Original'}, inplace=True)
        
        print(f"Mapped helper columns for {df['Location'].notna().sum()} rows using {id_column} column")
        print(f"  - Location: Facility names")
        print(f"  - Legacy: Yes/No flags")
        print(f"  - California: Yes/No flags")
        
        # Use .pipe() for clean transformations
        df = (df
            .pipe(clean_data_pipeline)
            .pipe(handle_list_data_with_explode)  # Handle any list data
            .pipe(reshape_enrollment_data)        # Handle wide format if needed
            .pipe(apply_group_transforms)         # Add group statistics
            .pipe(handle_outliers_with_where)     # Handle outliers
        )
        
        # Show data quality summary using .agg()
        summary = df[['Location', 'Legacy', 'California']].agg(['count', 'nunique'])
        print(f"\nData Quality Summary:\n{summary}")
    else:
        print("Warning: Could not find Client ID column (DEPT #, CLIENT ID, etc.)")
    
    return df

def clean_data_pipeline(df):
    """
    Clean and prepare data using method chaining
    """
    return (df
            .fillna({'RELATION': 'UNKNOWN'})  # Handle missing values
            .replace({'': np.nan})  # Replace empty strings with NaN
            .dropna(subset=['Location'])  # Remove rows without valid location
           )

def process_enrollment_data(df):
    """
    Process and aggregate enrollment data by facility, plan type, and tier
    Using advanced pandas functions
    """
    processed_data = {}
    
    # First, calculate helper columns for benefit code determination
    df = calculate_helper_columns(df)
    
    # Use .query() for filtering - cleaner than bracket notation
    if 'RELATION' in df.columns:
        # For enrollment counts, we only count SELF (subscribers)
        subscribers_df = df.query("RELATION == 'SELF'").copy()
        print(f"Filtered to {len(subscribers_df)} subscriber rows (RELATION = SELF)")
    else:
        subscribers_df = df.copy()
        print("Warning: No RELATION column found, processing all rows")
    
    # Use .assign() to create multiple columns at once
    # Map PLAN codes to EPO/PPO/VALUE and use CALCULATED_BEN_CODE for tiers
    subscribers_df = subscribers_df.assign(
        plan_type=lambda x: x['PLAN'].map(PLAN_TO_TYPE).fillna('VALUE')
        if 'PLAN' in x.columns else 'VALUE',
        tier=lambda x: x['CALCULATED_BEN_CODE'].map(BEN_CODE_TO_TIER).fillna('EE')
        if 'CALCULATED_BEN_CODE' in x.columns 
        else x['BEN CODE'].map(BEN_CODE_TO_TIER).fillna('EE') 
        if 'BEN CODE' in x.columns 
        else 'EE'
    )
    
    # Check for unmapped PLAN codes
    if 'PLAN' in subscribers_df.columns:
        unmapped_plans = subscribers_df[
            ~subscribers_df['PLAN'].isin(PLAN_TO_TYPE.keys()) & subscribers_df['PLAN'].notna()
        ]['PLAN'].unique()
        if len(unmapped_plans) > 0:
            print(f"Warning: Found unmapped PLAN codes (defaulting to VALUE): {unmapped_plans[:10]}")
    
    # Check enrollment tier distribution
    if 'tier' in subscribers_df.columns:
        tier_dist = subscribers_df['tier'].value_counts()
        print(f"\nEnrollment Tier Distribution:\n{tier_dist}")
    
    # Use .pipe() for clean data transformations
    subscribers_df = (subscribers_df
        .pipe(add_enrollment_categories)  # Add performance categories
        .pipe(validate_facility_codes)    # Validate facility codes exist
    )
    
    # Process each tab and facility
    for tab_name, facilities in FACILITY_MAPPING.items():
        processed_data[tab_name] = {}
        
        for client_id, facility_name in facilities.items():
            # Use query() for complex filtering
            id_columns = ['DEPT #', 'CLIENT ID', 'CLIENT_ID', 'TPA Code']
            facility_data = None
            
            for col in id_columns:
                if col in subscribers_df.columns:
                    # Using query() with f-strings for dynamic column names
                    try:
                        facility_data = subscribers_df.query(f"`{col}` == @client_id").copy()
                        if not facility_data.empty:
                            break
                    except:
                        facility_data = subscribers_df[subscribers_df[col] == client_id].copy()
                        if not facility_data.empty:
                            break
            
            if facility_data is None or facility_data.empty:
                # Default to zeros using dictionary comprehension
                processed_data[tab_name][facility_name] = {
                    plan: {tier: 0 for tier in ['EE', 'EE & Spouse', 'EE & Child', 'EE & Children', 'EE & Family']}
                    for plan in ['EPO', 'PPO', 'VALUE']  # Including PPO
                }
                continue
            
            # Use .groupby() with .size() and unstack for pivot-like behavior
            if not facility_data.empty:
                # Create pivot table for counts
                enrollment_counts = (facility_data
                    .groupby(['plan_type', 'tier'])
                    .size()
                    .unstack(fill_value=0)
                    .reindex(columns=['EE', 'EE & Spouse', 'EE & Child', 'EE & Children', 'EE & Family'], fill_value=0)
                    .to_dict('index')
                )
                
                # Structure the result
                result = {}
                for plan in ['EPO', 'PPO', 'VALUE']:  # Including PPO
                    if plan in enrollment_counts:
                        result[plan] = enrollment_counts[plan]
                    else:
                        result[plan] = {tier: 0 for tier in ['EE', 'EE & Spouse', 'EE & Child', 'EE & Children', 'EE & Family']}
                
                processed_data[tab_name][facility_name] = result
            else:
                # Use default zeros
                processed_data[tab_name][facility_name] = {
                    plan: {tier: 0 for tier in ['EE', 'EE & Spouse', 'EE & Child', 'EE & Children', 'EE & Family']}
                    for plan in ['EPO', 'PPO', 'VALUE']
                }
    
    return processed_data

def add_enrollment_categories(df):
    """
    Use .cut() to categorize enrollment sizes
    This helps identify high/medium/low volume facilities
    """
    if 'Location' in df.columns:
        # Count enrollments per facility
        facility_counts = df.groupby('Location').size().reset_index(name='facility_enrollment_count')
        
        # Use .cut() to create categories
        if not facility_counts.empty and len(facility_counts) > 0:
            facility_counts['enrollment_volume'] = pd.cut(
                facility_counts['facility_enrollment_count'],
                bins=[0, 50, 200, float('inf')],
                labels=['Low', 'Medium', 'High']
            )
            
            # Merge back to main dataframe
            df = df.merge(facility_counts[['Location', 'enrollment_volume']], on='Location', how='left')
            
            print("\nEnrollment Volume Categories:")
            print(facility_counts.groupby('enrollment_volume')['Location'].count())
    
    return df

def validate_facility_codes(df):
    """
    Use .where() for conditional operations
    Flag invalid facility codes
    """
    if 'Location' in df.columns:
        # Use .where() to conditionally flag invalid facilities
        df['valid_facility'] = df['Location'].notna()
        
        invalid_count = (~df['valid_facility']).sum()
        if invalid_count > 0:
            print(f"Warning: {invalid_count} rows with invalid/missing facility codes")
    
    return df

def analyze_source_columns(df):
    """
    Analyze source data to help identify BEN CODEs and PLAN values
    This helps users configure the mappings correctly
    """
    print("\n" + "="*60)
    print("SOURCE DATA ANALYSIS")
    print("="*60)
    
    # Check for Employee ID column
    emp_cols = ['EMPLOYEE ID', 'EMP ID', 'J', 'Employee_ID', 'EMPLOYEE NAME']
    found_emp_col = None
    for col in emp_cols:
        if col in df.columns:
            found_emp_col = col
            print(f"Found Employee ID column: {col}")
            print(f"  - Unique employees: {df[col].nunique()}")
            break
    
    if not found_emp_col:
        print("Warning: No Employee ID column found. Using SEQ. # for grouping.")
    
    # Check for RELATION column
    if 'RELATION' in df.columns:
        relation_dist = df['RELATION'].value_counts()
        print(f"\nRELATION distribution:\n{relation_dist}")
    else:
        print("\nNo 'RELATION' column found")
    
    # Check for PLAN column and validate against mapping
    if 'PLAN' in df.columns:
        plans = df['PLAN'].value_counts().head(20)
        print("\nTop PLAN values found:")
        print(plans)
        
        # Check which plans are mapped
        unmapped_plans = df[~df['PLAN'].isin(PLAN_TO_TYPE.keys()) & df['PLAN'].notna()]['PLAN'].unique()
        if len(unmapped_plans) > 0:
            print(f"\nUnmapped PLAN codes found: {unmapped_plans[:10]}")
            print("These will default to VALUE")
        
        # Show distribution of plan types
        df['plan_type_temp'] = df['PLAN'].map(PLAN_TO_TYPE).fillna('VALUE')
        plan_dist = df['plan_type_temp'].value_counts()
        print(f"\nPlan Type Distribution:\n{plan_dist}")
        df.drop('plan_type_temp', axis=1, inplace=True)
    else:
        print("\nNo 'PLAN' column found in source data")
    
    # Check for BEN CODE column
    if 'BEN CODE' in df.columns:
        ben_codes = df['BEN CODE'].value_counts().head(20)
        print("\nBEN CODE values found (will be overridden by CALCULATED_BEN_CODE):")
        print(ben_codes)
    
    # Show all columns in the source data
    print(f"\nAll columns in source data ({len(df.columns)} total):")
    for i, col in enumerate(df.columns, 1):
        print(f"  {i:2}. {col}")
    
    print("\n" + "="*60)

def validate_and_summarize_data(df, processed_data):
    """
    Validate data quality and provide summary statistics
    Using advanced pandas functions
    """
    print("\n" + "="*60)
    print("DATA VALIDATION AND SUMMARY")
    print("="*60)
    
    # Use .describe() for quick statistics
    if 'RELATION' in df.columns:
        relation_summary = df['RELATION'].value_counts()
        print(f"\nRelation Distribution:\n{relation_summary}")
    
    # Use .crosstab() for cross-tabulation analysis
    if 'Legacy' in df.columns and 'California' in df.columns:
        cross_tab = pd.crosstab(df['Legacy'], df['California'], margins=True)
        print(f"\nLegacy vs California Cross-Tab:\n{cross_tab}")
    
    # Use .nunique() to count unique values efficiently
    unique_counts = df.select_dtypes(include=['object']).nunique()
    print(f"\nUnique Value Counts:\n{unique_counts.head(10)}")
    
    # Use .memory_usage() to check data efficiency
    memory = df.memory_usage(deep=True).sum() / 1024**2  # Convert to MB
    print(f"\nTotal memory usage: {memory:.2f} MB")
    
    # Summary of processed enrollments by tab
    print("\n" + "-"*40)
    print("ENROLLMENT SUMMARY BY TAB")
    print("-"*40)
    
    tab_summary = []
    for tab, facilities in processed_data.items():
        total_epo = sum(sum(plans.get('EPO', {}).values()) for plans in facilities.values())
        total_ppo = sum(sum(plans.get('PPO', {}).values()) for plans in facilities.values())
        total_value = sum(sum(plans.get('VALUE', {}).values()) for plans in facilities.values())
        if total_epo + total_ppo + total_value > 0:
            tab_summary.append({
                'Tab': tab,
                'Facilities': len(facilities),
                'EPO Enrollments': total_epo,
                'PPO Enrollments': total_ppo,
                'VALUE Enrollments': total_value,
                'Total': total_epo + total_ppo + total_value
            })
    
    if tab_summary:
        summary_df = pd.DataFrame(tab_summary)
        print(summary_df.to_string(index=False))
        print(f"\nGrand Total: {summary_df['Total'].sum()} enrollments")
    
    return summary_df if tab_summary else pd.DataFrame()

def export_summary_report(processed_data, output_file='enrollment_summary.csv'):
    """
    Export a summary report to CSV using pandas
    """
    rows = []
    for tab, facilities in processed_data.items():
        for facility, plans in facilities.items():
            for plan_type, tiers in plans.items():
                for tier, count in tiers.items():
                    if count > 0:  # Only include non-zero enrollments
                        rows.append({
                            'Tab': tab,
                            'Facility': facility,
                            'Plan Type': plan_type,
                            'Enrollment Tier': tier,
                            'Count': count
                        })
    
    if rows:
        summary_df = pd.DataFrame(rows)
        
        # Use .to_csv() with useful parameters
        summary_df.to_csv(output_file, index=False, encoding='utf-8-sig')
        
        # Use .pivot_table() for a different view
        pivot = summary_df.pivot_table(
            index=['Tab', 'Facility'],
            columns=['Plan Type', 'Enrollment Tier'],
            values='Count',
            fill_value=0,
            aggfunc='sum'
        )
        
        print(f"\nSummary report exported to {output_file}")
        print(f"Pivot view:\n{pivot.head(10)}")
        
        return summary_df
    else:
        print("No enrollment data to export")
        return pd.DataFrame()

def find_facility_location(ws, facility_name, start_row=1, max_row=1000):
    """
    Find the row AND column where a facility section starts in the worksheet
    Returns tuple of (row, column) or (None, None) if not found
    """
    for row in range(start_row, min(max_row, ws.max_row + 1)):
        for col in range(1, min(10, ws.max_column + 1)):  # Check first 10 columns
            cell_value = ws.cell(row=row, column=col).value
            if cell_value and facility_name in str(cell_value):
                return row, col
    return None, None

def update_destination_file(destination_path, processed_data, output_path=None):
    """
    Update the destination Excel file with processed enrollment data
    """
    # Load the workbook
    wb = load_workbook(destination_path)
    
    for tab_name, facilities_data in processed_data.items():
        if tab_name not in wb.sheetnames:
            print(f"Warning: Tab '{tab_name}' not found in destination file")
            continue
            
        ws = wb[tab_name]
        
        for facility_name, plan_data in facilities_data.items():
            # Find where this facility's section starts (row and column)
            facility_row, facility_col = find_facility_location(ws, facility_name)
            
            if not facility_row:
                print(f"Warning: Could not find '{facility_name}' in tab '{tab_name}'")
                continue
            
            # From facility location: 3 columns over, 1 row down is where EE starts
            enrollment_col = facility_col + 3
            
            print(f"  Found '{facility_name}' at {get_column_letter(facility_col)}{facility_row}")
            print(f"    -> Will place enrollments in column {get_column_letter(enrollment_col)}")
            
            # EPO section starts 1 row down from facility name
            epo_start_row = facility_row + 1
            if 'EPO' in plan_data:
                print(f"    -> EPO enrollments in rows {epo_start_row}-{epo_start_row+4}")
                update_plan_section_by_position(ws, epo_start_row, enrollment_col, plan_data['EPO'])
            
            # PPO section if exists
            ppo_start_row = find_ppo_section_start(ws, facility_row, facility_col)
            if ppo_start_row and 'PPO' in plan_data:
                print(f"    -> PPO enrollments in rows {ppo_start_row+1}-{ppo_start_row+5}")
                update_plan_section_by_position(ws, ppo_start_row + 1, enrollment_col, plan_data['PPO'])
            
            # VALUE section
            value_start_row = find_value_section_start(ws, facility_row, facility_col)
            if value_start_row and 'VALUE' in plan_data:
                print(f"    -> VALUE enrollments in rows {value_start_row+1}-{value_start_row+5}")
                update_plan_section_by_position(ws, value_start_row + 1, enrollment_col, plan_data['VALUE'])
    
    # Save the updated workbook
    if output_path:
        wb.save(output_path)
    else:
        wb.save(destination_path.replace('.xlsx', '_updated.xlsx'))
    
    print(f"Successfully updated enrollment data!")

def find_ppo_section_start(ws, facility_row, facility_col, max_search=15):
    """
    Find where the PPO plan section starts after the EPO section
    """
    # Search for "PPO" text in the same column as facility
    for row in range(facility_row + 5, facility_row + max_search):
        cell_value = ws.cell(row=row, column=facility_col).value
        if cell_value and 'PPO' in str(cell_value).upper():
            return row
    return None

def find_value_section_start(ws, facility_row, facility_col, max_search=15):
    """
    Find where the VALUE plan section starts after the EPO section
    """
    # Search for "VALUE" text in the same column as facility, starting after EPO section
    for row in range(facility_row + 6, facility_row + max_search):
        cell_value = ws.cell(row=row, column=facility_col).value
        if cell_value and 'VALUE' in str(cell_value).upper():
            return row
    # If not found, estimate based on typical spacing (7 rows after facility for EPO + spacing)
    return facility_row + 7

def update_plan_section_by_position(ws, start_row, col, tier_data):
    """
    Update a specific plan section with enrollment counts using position-based logic
    """
    # Map tier names to their row offsets from the start position
    # Note: Some templates may combine Child/Children into one row
    tier_rows = {
        'EE': 0,
        'EE & Spouse': 1,
        'EE & Child': 2,
        'EE & Children': 3,  # May be same row as EE & Child in some templates
        'EE & Family': 4  # This might be row 3 if Child/Children are combined
    }
    
    # Check if template uses combined Child/Children format
    # by looking at the tier labels in column F (or facility_col + 2)
    tier_label_col = col - 1  # Usually one column left of enrollment numbers
    row2_label = ws.cell(row=start_row + 2, column=tier_label_col).value
    
    if row2_label and 'Child(ren)' in str(row2_label):
        # Combined format: 4 tiers total
        tier_rows = {
            'EE': 0,
            'EE & Spouse': 1,
            'EE & Child': 2,  # Combined with Children
            'EE & Children': 2,  # Combined with Child
            'EE & Family': 3
        }
    
    for tier, row_offset in tier_rows.items():
        if tier in tier_data:
            # Update the enrollment count at the calculated position
            current_value = ws.cell(row=start_row + row_offset, column=col).value or 0
            # If Child and Children map to same row, add them together
            if tier == 'EE & Children' and row_offset == tier_rows.get('EE & Child', -1):
                ws.cell(row=start_row + row_offset, column=col).value = current_value + tier_data[tier]
            else:
                ws.cell(row=start_row + row_offset, column=col).value = tier_data[tier]

def main():
    """
    Main execution function with enhanced data processing
    """
    # File paths - using existing structure
    source_file = 'data/input/Data_file_prime.xlsx'
    destination_file = 'data/input/Prime_output_file.xlsx'
    output_file = 'output/enrollment_updated.xlsx'
    summary_file = 'output/enrollment_summary.csv'
    
    print("="*60)
    print("ENROLLMENT AUTOMATION SYSTEM")
    print("="*60)
    print(f"Source file: {source_file}")
    print(f"Destination template: {destination_file}")
    print(f"Output will be saved as: {output_file}\n")
    
    try:
        # Step 1: Read source data with automatic lookups
        print("Step 1: Reading source data...")
        source_df = read_source_data(source_file)
        
        # Step 1b: Analyze source data to help configure mappings
        analyze_source_columns(source_df)
        
        # Step 2: Process and aggregate data using advanced pandas
        print("\nStep 2: Processing enrollment data...")
        processed_data = process_enrollment_data(source_df)
        
        # Step 3: Validate and summarize the data
        print("\nStep 3: Validating data...")
        summary_df = validate_and_summarize_data(source_df, processed_data)
        
        # Step 4: Export summary report
        print("\nStep 4: Exporting summary report...")
        export_summary_report(processed_data, summary_file)
        
        # Step 5: Update destination file
        print("\nStep 5: Updating destination file...")
        update_destination_file(destination_file, processed_data, output_file)
        
        # Step 6: Final summary
        print("\n" + "="*60)
        print("AUTOMATION COMPLETE!")
        print("="*60)
        print(f"✓ Destination file updated: {output_file}")
        print(f"✓ Summary report saved: {summary_file}")
        print(f"✓ Total facilities processed: {sum(len(f) for f in FACILITY_MAPPING.values())}")
        
        if not summary_df.empty:
            print(f"✓ Total enrollments processed: {summary_df['Total'].sum()}")
        
    except FileNotFoundError as e:
        print(f"\nERROR: Could not find file - {e}")
        print("Please ensure the source and destination files are in the correct folders.")
    except Exception as e:
        print(f"\nERROR: An unexpected error occurred - {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()