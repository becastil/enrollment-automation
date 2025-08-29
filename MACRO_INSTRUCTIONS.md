# VBA Macro Instructions for Enrollment Updates

## Overview
This solution uses a VBA macro to update enrollment counts in your Excel template, avoiding the file corruption issues experienced with the Python/openpyxl approach.

## Components

### 1. CSV Export Script (`scripts/export_enrollment_to_csv_with_names.py`)
- Exports enrollment data from source to a CSV file
- Creates `enrollment_data_detailed.csv` in the Prime_EFR folder
- Aggregates data by Tab, ClientID, PlanType, PlanName (with block labels), and Tier
- Includes specific plan block labels from configuration for precise matching

### 2. VBA Macro Module (`UpdateEnrollmentCounts.bas`)
- Reads the CSV data including plan names
- Finds Client IDs in the Excel template
- Updates enrollment values in the correct cells
- Uses block labels for facilities with multiple plan blocks
- Provides status updates and error handling

## Installation Steps

### Step 1: Generate the CSV Data
```powershell
# In PowerShell, navigate to Prime_EFR folder
cd C:\Users\becas\Prime_EFR

# Run the export script
python scripts\export_enrollment_to_csv_with_names.py
```

This will create `enrollment_data_detailed.csv` with your enrollment data, including specific plan block labels for facilities that have multiple plan configurations.

### Step 2: Import the VBA Macro

1. Open your Excel template file:
   `Prime Enrollment Funding by Facility for August.xlsx`

2. Press `Alt + F11` to open the VBA Editor

3. In the VBA Editor:
   - Go to `File` → `Import File...`
   - Navigate to `C:\Users\becas\Prime_EFR`
   - Select `UpdateEnrollmentCounts.bas`
   - Click `Open`

4. Save the workbook as a macro-enabled file:
   - File → Save As
   - Choose file type: `Excel Macro-Enabled Workbook (*.xlsm)`
   - Save as: `Prime Enrollment Funding by Facility for August.xlsm`

## Usage

### Running the Main Update

1. In Excel, press `Alt + F8` to open the Macro dialog
2. Select `UpdateEnrollmentFromCSV`
3. Click `Run`

The macro will:
- Load data from the CSV file
- Update all enrollment values
- Show a summary of successful/failed updates

### Available Macros

#### `UpdateEnrollmentFromCSV`
Main macro that updates all enrollment values from the CSV file.

#### `ShowEnrollmentStatus`
Shows how many records are ready to be updated from the CSV.

#### `TestSingleUpdate`
Tests updating a single known value (Monroe facility).

## How It Works

The macro uses a smart search algorithm:

1. **Find Client IDs**: Searches columns A-E for Client IDs (e.g., H3397)
2. **Locate Plan Type**: Finds the EPO or VALUE plan section below the Client ID
3. **Use Block Labels**: For facilities with multiple plan blocks (e.g., Lower Bucks, St. Francis), the CSV contains specific block labels like "PRIME EPO PLAN (Self-Insured) - IUOE" to ensure accurate matching
4. **Match Tiers**: Normalizes tier names to match (handles variations like "EE Only" vs "EMP")
5. **Update Values**: Writes the enrollment count to the appropriate cell

## Block Labels Feature

The enhanced CSV export includes specific plan block labels from the configuration. This is especially important for facilities that have multiple plan blocks:

### Examples of Block Labels:
- **Lower Bucks (H3330)**:
  - "PRIME EPO PLAN (Self-Insured) - IUOE"
  - "PRIME EPO PLAN (Self-Insured) - PASNAP & Non-Union"
  - "PRIME VALUE PLAN (Self-Insured) - Union & Non-Union"

- **St. Francis (H3275)**:
  - "PRIME SEIU 2020 D1 UNIFIED EPO PLAN (Self-Insured)"
  - "PRIME UNAC D1 UNIFIED EPO PLAN (Self-Insured)"
  - "PRIME Non-Union D1 UNIFIED EPO PLAN (Self-Insured)"

Facilities without specific block configurations will show default labels like "EPO (Default)" or "VALUE (Default)".

## Tier Name Normalization

The macro handles various tier name formats:
- "EE Only", "EMP", "Employee Only" → All map to "EE Only"
- "EE+Spouse", "ESP", "Employee + Spouse" → All map to "EE+Spouse"
- "EE+Child(ren)", "ECH", "Employee + Child" → All map to "EE+Child(ren)"
- "EE+Family", "FAM", "Family" → All map to "EE+Family"
- "EE+1 Dep", "E1D", "Employee + 1" → All map to "EE+1 Dep"

## Troubleshooting

### If the macro can't find Client IDs:
- Check that Client IDs are visible in columns A-E
- Ensure Client ID format matches (e.g., H3397)
- Verify the tab names match between CSV and Excel

### If values aren't updating:
- Run `ShowEnrollmentStatus` to verify CSV data loaded
- Check that the CSV file is `enrollment_data_detailed.csv` (not the old `enrollment_data.csv`)
- Ensure you've run the new export script: `scripts\export_enrollment_to_csv_with_names.py`
- Check that tier names in Excel match expected formats
- Use Debug mode (F8 in VBA Editor) to step through the code

### To view detailed logs:
1. In VBA Editor, open the Immediate Window (Ctrl+G)
2. Run the macro
3. Check the Immediate Window for debug messages

## Customization

### Adjusting Column Positions
If your template has different column layouts, modify these lines in the VBA code:

```vba
' In FindTierCell function
tierColumn = 3  ' Column C for tier names
valueColumn = 4  ' Column D for values
```

### Adding New Tier Mappings
Add new tier name variations in the `NormalizeTierName` function.

## Benefits of This Approach

1. **No File Corruption**: Works directly within Excel
2. **Preserves Formatting**: Doesn't modify Excel structure
3. **Fast Updates**: Processes hundreds of values in seconds
4. **Error Handling**: Shows which updates succeeded/failed
5. **Flexible Matching**: Handles tier name variations

## Quick Start Checklist

- [ ] Run `scripts\export_enrollment_to_csv_with_names.py` to generate CSV
- [ ] Verify `enrollment_data_detailed.csv` was created
- [ ] Open Excel template
- [ ] Import VBA macro module (`UpdateEnrollmentCounts.bas`)
- [ ] Save as .xlsm file
- [ ] Run `UpdateEnrollmentFromCSV` macro
- [ ] Verify values updated correctly

## Support

If you encounter issues:
1. Check the CSV file exists at `C:\Users\becas\Prime_EFR\enrollment_data_detailed.csv`
2. Verify the CSV contains the PlanName column with block labels
3. Ensure the Excel file has the expected tab names
4. Run `TestSingleUpdate` to test basic functionality
5. Review debug output in VBA Immediate Window