# Prime Employee Enrollment Data Processing System

A robust Python-based solution for processing and analyzing Prime employee enrollment data with declarative block aggregations, comprehensive tier reconciliation, validation, and automated write-back to Excel templates.

## 🚀 Quick Start

```bash
# Run the latest version with declarative aggregations:
python enrollment_automation_v6.py

# Or use the Python runner:
python run_enrollment.py
```

## ✨ Features

### Version 6.0.0 - Declarative Block Aggregations
- ✅ **Exact Control Totals**: 24,708 enrollments (14,533 EE / 2,639 Spouse / 4,413 Children / 3,123 Family)
- ✅ **Comprehensive Validation**: Pre-write control assertions ensure data integrity
- ✅ **Full Audit Trail**: CSV write log with all operations
- ✅ **Post-Write Verification**: Automatic validation of written values
- ✅ **Windows Native**: Fully compatible with Windows, no WSL required
- ✅ **32 Excel Sheets**: Automated write-back to all facility sheets
- ✅ **Deduplication Logic**: Prevents double-counting with first-only policy
- ✅ **Zero-Fill Protection**: Clears stale values before writing

## 📋 Prerequisites

- **Python**: 3.8 or higher (Render deployment: pin `runtime.txt` to `python-3.11.9` to avoid
  Python 3.13 builder issues)
- **Operating System**: Windows 10/11, macOS, Linux
- **Required Packages**: pandas, openpyxl, numpy

## 🛠️ Installation

### 1. Clone or Download
```bash
git clone https://github.com/becastil/enrollment-automation.git
cd enrollment-automation
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Verify Installation
```bash
python -c "import pandas; import openpyxl; import numpy; print('✓ All dependencies installed!')"
```

## 📁 Project Structure

```
Prime_EFR/
├── enrollment_automation_v6.py             # Main script with declarative aggregations
├── write_maps.py                          # Write map definitions for all 29 sheets
├── run_enrollment.py                      # Cross-platform Python runner
├── Prime Enrollment Funding by Facility for August.xlsx  # Excel template
│
├── config/                                # Configuration files
│   ├── block_aggregations.json           # Declarative block routing
│   └── plan_mappings.json                # PLAN code to EPO/VALUE mappings
│
├── data/
│   ├── input/
│   │   └── source_data.xlsx             # Source enrollment data
│   └── reference/                        # Facility mappings
│
├── output/                                # Generated reports and logs
│   ├── write_log.csv                     # Detailed write operations
│   ├── tier_reconciliation_report.csv    # Tier validation report
│   └── archive/                          # Old output files
│
├── scripts/
│   └── versions/                         # Previous versions (archived)
│       ├── enrollment_automation_tier_reconciled.py
│       └── enrollment_automation_v5.py
│
├── tests/                                   # Test files
├── docs/                                    # Documentation
├── config.json                             # Configuration settings
└── requirements.txt                        # Python dependencies
```

## 💻 Usage

### Running the Main Script

The `enrollment_automation_v6.py` script handles everything:

```bash
python enrollment_automation_v6.py
```

**What it does:**
1. Reads source data from `data/input/source_data.xlsx`
2. Applies waterfall filtering (Active status, Subscribers only)
3. Maps 82 facilities using CLIENT ID → TPA_TO_FACILITY mapping
4. Normalizes tiers: EE Only, EE+Spouse, EE+Child(ren), EE+Family
5. Validates against control totals (pre-write assertion)
6. Writes to 32 Excel sheets with exact cell placement
7. Generates comprehensive audit trail in `output/write_log.csv`
8. Performs post-write verification

### Output Files

After running, check the `output/` directory for:
- `write_log.csv` - Every cell written with values
- `tier_reconciliation_report.csv` - Detailed tier analysis
- `Prime Enrollment Funding by Facility for August_updated.xlsx` - Updated Excel file

## ⚙️ Configuration

### Control Totals (Built-in Validation)
```python
CONTROL_TOTALS = {
    "EE Only": 14533,
    "EE+Spouse": 2639,
    "EE+Child(ren)": 4413,
    "EE+Family": 3123
}
```

### Key Settings in Script
- `STRICT_CONTROL_CHECK = True` - Enforce control total validation
- `DRY_RUN_WRITE = False` - Set True to test without saving Excel
- `DRY_RUN = False` - Set True for preview mode

## 📊 Processing Pipeline

### 1. **Waterfall Tracking** (8 stages)
   - Raw data load
   - Key cleaning
   - Active status filter
   - Subscriber filter
   - Facility mapping
   - Plan mapping
   - Tier normalization
   - Final validation

### 2. **Tier Reconciliation**
   - Maps BEN CODE → Standard Tiers
   - Combines EE+Child and EE+Children
   - Tracks UNKNOWN tiers for visibility
   - Validates totals at each stage

### 3. **Write-Back Process**
   - Pre-write control assertion
   - Zero-fills cells before writing
   - Deduplication for multi-block sheets
   - Comprehensive logging
   - Post-write verification

## 🔧 Troubleshooting

### Common Issues

#### Excel Template Not Found
```bash
# Ensure template is in project root:
ls "Prime Enrollment Funding by Facility for August.xlsx"
```

#### Source Data Missing
```bash
# Check data directory:
ls data/input/source_data.xlsx
```

#### Control Totals Don't Match
- Review `output/tier_reconciliation_report.csv`
- Check for UNKNOWN tiers/plans
- Verify source data filters

#### Permission Errors
- Close Excel if template is open
- Ensure output directory exists
- Check file write permissions

## 📈 Performance

- **Processing Speed**: ~15,000 rows/second
- **Memory Usage**: ~100MB for 45,000 records
- **Sheets Processed**: 32 facility sheets
- **Write Operations**: ~600 cell writes
- **Total Runtime**: < 10 seconds typical

## 🔄 Recent Updates

### Version 6.0.0 (Latest)
- Declarative block aggregations via JSON config
- Multi-block dedupe fixes using (client_id, plan, label) key
- PLAN code to block routing with sum_of lists
- 29-sheet allowlist with Alvarado exclusion
- Config-driven aggregations in `config/block_aggregations.json`

## 🧭 Dashboard Prompts

- Universal, stack-agnostic dashboard prompts live in `docs/universal_dashboard_prompts.md`. Each entry includes implementation guidance and acceptance criteria.

### Version 5.0.0 
- Fixed 17 critical issues including multi-block bugs
- Added CLI arguments and config persistence
- Enhanced logging with block_id and reason tracking

## 📌 Best Practices

1. **Always backup** the Excel template before running
2. **Review write_log.csv** after each run
3. **Check control totals** match before proceeding
4. **Use DRY_RUN modes** for testing
5. **Keep source data** in standard format

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Test thoroughly
4. Update documentation
5. Submit pull request

## 📄 License

Proprietary - Prime Healthcare

---

**Version:** 6.0.0  
**Last Updated:** 2025-08-28  
**Maintainer:** Data Analytics Team  
**Status:** Production Ready
