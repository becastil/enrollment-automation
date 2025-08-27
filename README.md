# Prime Employee Enrollment Data Processing System

A robust Python-based solution for processing and analyzing Prime employee enrollment data from Excel files, with automated validation, mapping, and reporting capabilities.

## 🚀 Quick Start

```bash
# 1. Install Python 3.8+ (if not already installed)
python --version

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the enrollment automation
python enrollment_automation_complete.py

# 4. Or use the convenience script (Windows)
run.bat
```

### ✨ Latest Version (v3.3.0)
- All critical fixes integrated into single main script
- 741 missing employees issue resolved
- Tier collapse bug fixed
- Cleaner directory structure

## 📋 Prerequisites

- **Python**: 3.8 or higher
- **Operating System**: Windows 10/11 (WSL supported)
- **RAM**: Minimum 4GB (8GB recommended for large datasets)
- **Disk Space**: 100MB free space for processing

## 🛠️ Installation

### Step 1: Clone or Download the Project
```bash
# If using git (optional)
git clone <repository-url>
cd enrollment-automation

# Or simply extract the ZIP file
```

### Step 2: Set Up Python Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Activate it (Linux/Mac/WSL)
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Verify Installation
```bash
python -c "import pandas; import openpyxl; import numpy; print('All dependencies installed!')"
```

## 📁 Project Structure

```
Prime_EFR/
├── enrollment_automation_complete.py    # Main script with all fixes integrated
├── src/                                 # Core application modules
│   ├── enrollment_data_processing.py    # Main processing engine
│   ├── enrollment_validator.py          # Data validation module
│   ├── enrollment_analytics.py          # Analytics and reporting
│   └── update_output_file.py           # Excel column updater
│
├── data/
│   ├── reference/                   # Static reference data
│   │   ├── facility_mapping_complete.csv  # 76 facility mappings
│   │   └── plan_mapping_complete.csv      # 54 plan type mappings
│   ├── input/                       # Input data files
│   │   ├── source_data.xlsx            # Source enrollment data
│   │   └── template_file.xlsx          # Target template file
│   └── samples/                     # Sample data for testing
│       └── enrollment_sample.xlsx
│
├── scripts/                         # Utility scripts
│   ├── populate_tiered_enrollment.py   # Populate enrollment tiers
│   ├── check_excel_columns.py          # Verify Excel structure
│   └── create_sample_excel.py          # Generate test data
│
├── tests/                           # Test files
│   └── enrollment_processing_demo.py   # Usage examples
│
├── docs/                            # Documentation
│   ├── implementation-guide.md         # Detailed implementation guide
│   └── CLEANUP_REPORT.md              # Repository cleanup report
│
├── output/                          # Generated output (auto-created)
│   └── [Generated files will appear here]
│
├── scripts/                         # Utility scripts
│   ├── legacy/                     # Archived older versions
│   │   ├── enrollment_automation.py
│   │   ├── enrollment_automation_fixed.py
│   │   └── enrollment_fixes_patch.py
│   ├── populate_tiered_enrollment.py
│   ├── check_excel_columns.py
│   └── create_sample_excel.py
│
├── config.json                      # Configuration settings
├── requirements.txt                 # Python dependencies
├── run.bat                         # Windows convenience script
├── CHANGELOG.md                    # Version history and fixes
├── .gitignore                      # Git ignore rules
└── README.md                       # This file
```

## 💻 Usage Guide

### Main Enrollment Automation Script

The `enrollment_automation_complete.py` script provides complete end-to-end enrollment processing with all fixes:

```bash
# Run the complete automation with all fixes
python enrollment_automation_complete.py

# What it does:
# 1. Reads source_data.xlsx from data/input/
# 2. Filters to active subscribers (STATUS == 'A')
# 3. Maps 82 facilities using CLIENT ID (prioritized over DEPT #)
# 4. Calculates enrollment tiers based on family composition
# 5. Categorizes plans as EPO/PPO/VALUE with pattern fallback
# 6. Generates enrollment_summary.csv in output/
# 7. Creates enrollment_updated.xlsx with all data
```

**Key Features:**
- ✅ Processes 44,000+ enrollment records automatically
- ✅ Filters to active subscribers only (STATUS == 'A')
- ✅ Prioritizes CLIENT ID column for facility matching
- ✅ Built-in TPA to Facility/Legacy/California mappings (82 facilities)
- ✅ Automatic tier calculation (EE, EE+Spouse, EE+Children, etc.)
- ✅ Plan categorization with 70+ plan code mappings + pattern fallback
- ✅ Unified section finding for EPO/PPO/VALUE in templates
- ✅ Advanced pandas optimizations for performance
- ✅ Comprehensive data validation and error handling

### Basic Workflow (Legacy Method)

#### 1. Process Enrollment Data
```python
from src.enrollment_data_processing import build_facility_summary
import pandas as pd

# Load reference data
facility_map = pd.read_csv('data/reference/facility_mapping_complete.csv')
plan_map = pd.read_csv('data/reference/plan_mapping_complete.csv')

# Process enrollment data
enriched, summary, filtered = build_facility_summary(
    excel_path="data/input/source_data.xlsx",
    sheet_name="Sheet1",
    facility_key_col="CLIENT ID",
    plan_type_col="PLAN",
    facility_map=facility_map,
    plan_map=plan_map
)

# Save results
summary.to_csv('output/enrollment_summary.csv', index=False)
print(f"Processed {len(summary)} facility/plan combinations")
```

#### 2. Update Output File
```bash
# Update Column D with employee counts
python src/update_output_file.py \
    --source "data/input/source_data.xlsx" \
    --target "data/input/template_file.xlsx" \
    --dry-run  # Remove --dry-run to apply changes
```

#### 3. Run Analytics
```python
python src/enrollment_analytics.py

# Generates:
# - analytics_report.xlsx (multi-sheet Excel report)
# - analytics_metrics.json (key metrics)
```

#### 4. Validate Data Quality
```python
python src/enrollment_validator.py

# Output: validation_report.csv with quality checks
```

## ⚙️ Configuration

### config.json Structure
```json
{
    "excel_settings": {
        "default_sheet": "Sheet1",
        "header_row": 5,
        "data_start_row": 6
    },
    "column_mappings": {
        "facility_id": "CLIENT ID",
        "plan_code": "PLAN",
        "sequence": "SEQ. #",
        "employee_name": "EMPLOYEE NAME",
        "relation": "RELATION"
    },
    "processing_options": {
        "filter_subscribers_only": true,
        "aggregate_by_facility": true,
        "include_unmapped": false
    },
    "output_settings": {
        "output_directory": "./output",
        "timestamp_files": true,
        "formats": ["csv", "xlsx"]
    }
}
```

### Environment Variables (.env)
```bash
# Data paths
INPUT_DATA_PATH=./data/input/
OUTPUT_DATA_PATH=./output/
REFERENCE_DATA_PATH=./data/reference/

# Processing options
LOG_LEVEL=INFO
MAX_WORKERS=4
BATCH_SIZE=1000

# Excel settings
DEFAULT_SHEET_NAME=Sheet1
HEADER_ROW=5
```

## 📊 Data Processing Pipeline

### 1. **Input Stage**
- Read Excel file with dynamic header detection
- Handle multiple sheets and formats
- Clean and normalize data

### 2. **Mapping Stage**
- Map facility IDs to standard names
- Categorize plans (EPO, PPO, VALUE)
- Validate reference data completeness

### 3. **Filtering Stage**
- Filter to active records (STATUS == 'A')
- Filter to subscriber records (RELATION == 'SELF')
- Remove duplicates
- Apply business rules

### 4. **Aggregation Stage**
- Group by facility and plan type
- Calculate enrollment counts
- Generate summary statistics

### 5. **Validation Stage**
- Check for missing mappings
- Identify data quality issues
- Generate validation report

### 6. **Output Stage**
- Export to multiple formats (CSV, Excel, JSON)
- Create analytics dashboards
- Generate documentation

## 📝 Scripts Reference

### Core Modules

| Script | Purpose | Usage |
|--------|---------|-------|
| **`enrollment_automation_complete.py`** | **Main script with all fixes integrated** | **`python enrollment_automation_complete.py`** |
| `enrollment_data_processing.py` | Main processing engine | `python src/enrollment_data_processing.py` |
| `enrollment_validator.py` | Data validation | `python src/enrollment_validator.py` |
| `enrollment_analytics.py` | Generate analytics | `python src/enrollment_analytics.py` |
| `update_output_file.py` | Update Excel columns | `python src/update_output_file.py --help` |

### Utility Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `populate_tiered_enrollment.py` | Populate enrollment tiers | `python scripts/populate_tiered_enrollment.py` |
| `check_excel_columns.py` | Verify Excel structure | `python scripts/check_excel_columns.py` |
| `create_sample_excel.py` | Generate test data | `python scripts/create_sample_excel.py` |

## 🧪 Testing

### Run Demo Script
```bash
cd tests
python enrollment_processing_demo.py
```

### Expected Output
```
✓ Facility mapping loaded: 76 facilities
✓ Plan mapping loaded: 54 plan types
✓ Processed 25,013 contracts
✓ Generated summary for 165 facility/plan combinations
✓ All tests passed
```

## 🔧 Troubleshooting

### Common Issues and Solutions

#### 1. "CLIENT ID" column not found
**Solution:** Check Excel header row (default: row 5). Update in config.json:
```json
"header_row": 5
```

#### 2. ModuleNotFoundError: No module named 'pandas'
**Solution:** Install dependencies:
```bash
pip install -r requirements.txt
```

#### 3. PermissionError when writing files
**Solution:** Ensure output directory exists and has write permissions:
```bash
mkdir output
```

#### 4. Excel file not found
**Solution:** Verify file paths in config.json or use absolute paths:
```python
excel_path = r"C:\Users\your_user\enrollment-automation\data\input\source_data.xlsx"
```

#### 5. Memory error with large files
**Solution:** Process in chunks:
```python
for chunk in pd.read_excel(file, chunksize=10000):
    process(chunk)
```

#### 6. Missing facility/plan mappings
**Solution:** Check validation report and update reference CSVs:
```bash
python src/enrollment_validator.py
# Review output/validation_report.csv
```

#### 7. ImportError: cannot import name 'build_facility_summary'
**Solution:** Ensure you're in the project root directory:
```bash
cd enrollment-automation
python src/enrollment_data_processing.py
```

#### 8. Excel file is corrupted or locked
**Solution:** Close Excel and ensure file isn't open elsewhere:
```bash
# Windows: Check Task Manager for EXCEL.EXE
taskkill /f /im excel.exe
```

#### 9. Different Excel structure
**Solution:** Update column mappings in config.json to match your Excel:
```json
"column_mappings": {
    "facility_id": "YOUR_FACILITY_COLUMN",
    "plan_code": "YOUR_PLAN_COLUMN"
}
```

#### 10. Slow processing performance
**Solution:** Enable multiprocessing in config:
```json
"processing_options": {
    "use_multiprocessing": true,
    "max_workers": 4
}
```

## 📈 Performance Metrics

### enrollment_automation.py (NEW)
- **Processing Speed**: ~15,000 rows/second (with pandas optimizations)
- **Memory Usage**: ~46MB for 44,000 records
- **Total Processing Time**: <5 seconds for complete pipeline
- **Active Records**: 44,590 filtered from 44,741 total (STATUS == 'A')
- **Facilities Mapped**: 82 facilities across 30 groups (including Alvarado)
- **Plan Mappings**: 70+ plan codes to EPO/PPO/VALUE with pattern fallback
- **Enrollments Processed**: 24,282 subscriber records

### Legacy Scripts
- **Processing Speed**: ~2,300 rows/second
- **Memory Usage**: ~200MB for 50,000 records
- **File Size Limits**: Tested up to 100MB Excel files
- **Supported Formats**: .xlsx, .xls, .csv

## 🔄 Data Dictionary

### Input Columns
| Column | Description | Type | Required |
|--------|-------------|------|----------|
| CLIENT ID | Facility identifier (prioritized) | String | Yes |
| PLAN | Plan code | String | Yes |
| STATUS | Active/Inactive status (A/I) | String | Yes |
| SEQ. # | Sequence number (0=subscriber) | Integer | Yes |
| EMPLOYEE NAME | Employee full name | String | Yes |
| RELATION | Relationship (SELF, SPOUSE, CHILD) | String | Yes |
| EPO-PPO-VAL | Plan category | String | No |
| EFF. DATE | Effective date | Date | No |
| TERM | Termination date | Date | No |
| DEPT # | Alternative facility identifier | String | No |

### Output Columns
| Column | Description | Type |
|--------|-------------|------|
| CLIENT ID | Facility identifier | String |
| Facility | Facility name | String |
| Plan Type | EPO/PPO/VALUE | String |
| Enrollment Count | Number of contracts | Integer |
| Percentage | Percent of total | Float |

## 🚧 Maintenance

### Update Reference Data
1. Export new mappings to CSV
2. Place in `data/reference/` folder
3. Ensure headers match:
   - facility_mapping: CLIENT ID, Facility
   - plan_mapping: Plan Code, Plan Type

### Add New Facilities
```csv
CLIENT ID,Facility
H3XXX,New Facility Name
```

### Add New Plans
```csv
Plan Code,Plan Type
NEWPLAN,EPO
```

## 📌 Best Practices

1. **Always backup data** before processing
2. **Run validation** after updates
3. **Use dry-run mode** for testing
4. **Keep reference data updated**
5. **Review logs** for warnings
6. **Test with samples** before full processing

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Update documentation
5. Submit for review

## 📞 Support

For questions or issues:
1. Check the troubleshooting section
2. Review `docs/implementation-guide.md`
3. Check `output/validation_report.csv` for data issues
4. Contact the Data Analytics team

## 📄 License

Proprietary

---

**Last Updated:** 2025-08-27  
**Version:** 3.3.0  
**Maintainer:** Data Analytics Team  
**Status:** Production Ready - All critical fixes integrated into `enrollment_automation_complete.py`