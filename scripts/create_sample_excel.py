import pandas as pd
import numpy as np

# Create sample enrollment data similar to what the system expects
np.random.seed(42)

# Sample facility IDs from the facility mapping
facility_ids = ['H3100', 'H3270', 'H3271', 'H3272', 'H3130', 'H3564', 'H3565']
plan_codes = ['PRIMEASCILEPO', 'PRIMEINAILEPO', 'PRIMEINAILVALUE', 'PRIMELBHEPO', 'PRIMEMMCCEPO', 'PRIMEMMCIR', 'PRIMEMMDALEPO']

# Generate sample data
num_records = 500
data = {
    'CLIENT ID': np.random.choice(facility_ids, num_records),
    'PLAN': np.random.choice(plan_codes, num_records),
    'SEQ. #': np.random.choice([0, 1, 2, 3], num_records, p=[0.6, 0.2, 0.1, 0.1]),  # 0 for subscribers
    'CONTRACT NUMBER': [f'CN{i:05d}' for i in range(1, num_records + 1)],
    'MEMBER NAME': [f'Member {i}' for i in range(1, num_records + 1)],
    'PREMIUM': np.random.uniform(100, 500, num_records)
}

df = pd.DataFrame(data)

# Create Excel file with multiple sheets
with pd.ExcelWriter('Prime_Enrollment_Sample.xlsx', engine='openpyxl') as writer:
    # Main cleaned sheet with header starting at row 5
    # Write with startrow=4 to leave space for headers
    df.to_excel(writer, sheet_name='Cleaned use this one', index=False, startrow=4)
    
    # Additional facility-specific sheets
    for facility_id in facility_ids[:3]:
        facility_data = df[df['CLIENT ID'] == facility_id].copy()
        facility_data.to_excel(writer, sheet_name=f'Facility_{facility_id}', index=False)

print("Sample Excel file 'Prime_Enrollment_Sample.xlsx' created successfully!")
print(f"Total records: {num_records}")
print(f"Sheets created: 'Cleaned use this one' + {len(facility_ids[:3])} facility sheets")