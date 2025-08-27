# Changelog

All notable changes to the Prime Employee Enrollment Data Processing System are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.3.0] - 2025-08-27

### Added
- Comprehensive directory cleanup and reorganization
- Legacy scripts archive directory (`scripts/legacy/`) for version history
- Proper .gitignore file for Python projects
- Consolidated documentation into single CHANGELOG.md

### Changed
- **Main script is now `enrollment_automation_complete.py`** with all fixes integrated
- Moved all test files to `tests/` directory  
- Moved all Excel data files to `data/input/` directory
- Updated README to reflect new simplified structure
- Archived older script versions to `scripts/legacy/`

### Removed
- Redundant backup scripts and diagnostic files
- Duplicate fix summary documentation files (consolidated here)
- Loose Excel files from root directory

## [3.2.1] - 2025-08-27

### Fixed
- **741 Missing Employees Issue**: Resolved silent data drops in enrollment pipeline
  - Fixed strict STATUS filter (now accepts 'A', 'ACTIVE', 'ACT', etc.)
  - Fixed strict RELATION filter (now accepts 'SELF', 'EE', 'EMPLOYEE', 'SUBSCRIBER', etc.)
  - Fixed unmapped facilities being dropped (now preserved as UNKNOWN)
  - Fixed key cleaning issues causing mismatches

### Added
- Row-loss waterfall tracking at 8 pipeline stages
- Flexible filtering helper functions (`is_active()`, `is_subscriber()`)
- `clean_key()` function for consistent key normalization
- Comprehensive diagnostic reporting with sample dropped rows

### Changed
- Improved data preservation: 44,500 rows out from 45,000 in (vs 43,759 before)
- Row recovery: 741 employees no longer silently dropped

## [3.2.0] - 2025-08-27

### 🔧 Fixed
- **Critical Tier Collapse Bug** - Enrollment counts were incorrectly collapsing into single tiers (often EE+Family)
  - Root cause: `calculate_helper_columns()` function incorrectly inferred tiers from family composition
  - Impact: All facilities showing incorrect tier distributions
  - Files affected: San Dimas (H3170), Lower Bucks (H3330), and others

### ✨ Added
- `enrollment_automation_fixed.py` - Complete fixed version with proper tier normalization
- `enrollment_fixes_patch.py` - Patch instructions to fix existing enrollment_automation.py
- `test_enrollment_fix.py` - Test script demonstrating the fix with before/after comparison
- `ENROLLMENT_FIX_SUMMARY.md` - Comprehensive documentation of the fix
- Direct tier normalization from BEN CODE column
- Plan variant tracking (shows multiple EPO/PPO/VALUE variants separately)
- Integrity checks to ensure tier sums match total subscriber counts
- UNKNOWN tier and plan auditing for visibility

### 📊 Improved
- Tier distribution accuracy - now correctly splits across EE, EE+Spouse, EE+Child(ren), EE+Family
- Data integrity validation with assertion checks
- Comprehensive logging of processing steps and unknowns

### 🔄 Changed
- Removed dependency on flawed `calculate_helper_columns()` logic
- Now uses raw BEN CODE data directly instead of inferring from relations
- Unknown tiers stay as "UNKNOWN" instead of defaulting to EE+Family

## [3.1.0] - 2025-08-27

### Added
- Enhanced enrollment_automation.py with active subscriber filtering
- CLIENT ID prioritization over DEPT #
- Unified section finding for EPO/PPO/VALUE in templates
- Built-in TPA to Facility/Legacy/California mappings (82 facilities)
- Automatic tier calculation
- Plan categorization with 70+ plan code mappings

### Improved
- Processing speed: ~15,000 rows/second
- Memory usage: ~46MB for 44,000 records
- Comprehensive data validation and error handling

## [3.0.0] - 2025-08-26

### Added
- Complete enrollment automation script (enrollment_automation.py)
- Facility mapping for 76 facilities
- Plan mapping for 54 plan types
- Analytics and reporting modules
- Data validation framework

### Changed
- Restructured project for better modularity
- Enhanced Excel processing capabilities
- Improved error handling and logging

## [2.0.0] - 2025-08-25

### Added
- Core enrollment data processing engine
- Excel column updater utility
- Reference data management
- Sample data for testing

### Changed
- Migrated from legacy scripts to modular architecture
- Standardized data pipeline

## [1.0.0] - 2025-08-24

### Added
- Initial release
- Basic enrollment data processing
- CSV export functionality
- Simple validation checks