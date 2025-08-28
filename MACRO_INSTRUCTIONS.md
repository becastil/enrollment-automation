# VBA Macro Instructions for Enrollment Updates

## Overview
This solution uses a VBA macro to update enrollment counts in your Excel template, avoiding the file corruption issues experienced with the Python/openpyxl approach.

## Components

### 1. CSV Export Script (`scripts/export_enrollment_to_csv.py`)
- Exports enrollment data from source to a CSV file
- Creates `enrollment_data.csv` in the Prime_EFR folder
- Aggregates data by Tab, ClientID, PlanType, and Tier

### 2. VBA Macro Module (`UpdateEnrollmentCounts.bas`)
- Reads the CSV data
- Finds Client IDs in the Excel template
- Updates enrollment values in the correct cells
- Provides status updates and error handling

## Installation Steps

### Step 1: Generate the CSV Data
```powershell
# In PowerShell, navigate to scripts folder
cd C:\Users\becas\Prime_EFR\scripts

# Run the export script
python export_enrollment_to_csv.py
```

This will create `enrollment_data.csv` with your enrollment data.

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
3. **Match Tiers**: Normalizes tier names to match (handles variations like "EE Only" vs "EMP")
4. **Update Values**: Writes the enrollment count to the appropriate cell

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

- [ ] Run `export_enrollment_to_csv.py` to generate CSV
- [ ] Open Excel template
- [ ] Import VBA macro module
- [ ] Save as .xlsm file
- [ ] Run `UpdateEnrollmentFromCSV` macro
- [ ] Verify values updated correctly

## Support

If you encounter issues:
1. Check the CSV file exists at `C:\Users\becas\Prime_EFR\enrollment_data.csv`
2. Verify the Excel file has the expected tab names
3. Run `TestSingleUpdate` to test basic functionality
4. Review debug output in VBA Immediate Window