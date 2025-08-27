# Migration Guide: v3.1.0 to v3.2.0

## Overview
Version 3.2.0 fixes a critical tier collapse bug that was causing enrollment counts to be incorrectly consolidated into single tiers (often EE+Family). This guide will help you migrate to the fixed version.

## Impact Assessment

### Who is affected?
- All users processing enrollment data with tier/coverage level breakdowns
- Reports showing only EE+Family when multiple tiers should exist
- Facilities with suspiciously uniform tier distributions

### Symptoms of the bug:
- San Dimas (H3170) showing all enrollments as EE+Family
- Lower Bucks (H3330) not showing separate EPO variants
- Any facility where all employees appear in one tier despite varied family compositions

## Migration Options

### Option 1: Use the Fixed Script (Recommended)
```bash
# Simply run the new fixed version
python enrollment_automation_fixed.py

# This script includes:
# - Direct tier normalization from BEN CODE
# - Plan variant tracking
# - Integrity checks
# - UNKNOWN auditing
```

### Option 2: Patch Your Existing Script
If you have customizations in your current enrollment_automation.py:

1. **Review the patch file:**
```bash
# Open and review the changes
cat enrollment_fixes_patch.py
```

2. **Apply the changes manually:**
- Add the `normalize_tier()` function after line 449
- Replace the entire `process_enrollment_data()` function
- Optionally add `create_variant_pivot()` for variant tracking

3. **Key changes to make:**
```python
# ADD this function after BEN_CODE_TO_TIER dictionary:
def normalize_tier(raw_tier):
    """Normalize raw tier text to standardized format"""
    # See enrollment_fixes_patch.py for full implementation
    
# MODIFY process_enrollment_data():
# - Remove call to calculate_helper_columns()
# - Use BEN CODE directly: subscribers_df['tier'] = subscribers_df['BEN CODE'].apply(normalize_tier)
# - Add integrity checks and UNKNOWN auditing
```

### Option 3: Gradual Migration
If you need to validate changes:

1. **Run both versions and compare:**
```bash
# Run original
python enrollment_automation.py
mv output/enrollment_summary.csv output/enrollment_summary_old.csv

# Run fixed version
python enrollment_automation_fixed.py
mv output/enrollment_pivot_grouped.csv output/enrollment_summary_new.csv

# Compare results
```

2. **Test with specific facilities:**
```python
# Test San Dimas (H3170) for tier distribution
# Test Lower Bucks (H3330) for EPO variants
```

## Validation Checklist

After migration, verify:

- [ ] San Dimas (H3170) shows multiple tiers, not just EE+Family
- [ ] Lower Bucks (H3330) shows separate EPO variants
- [ ] Total enrollment counts match between old and new (should be same total, different distribution)
- [ ] No facilities have 100% of enrollments in single tier (unless genuinely true)
- [ ] UNKNOWN audit shows any unmapped BEN CODEs that need attention

## New Features in v3.2.0

### 1. Two Output Files
```bash
# Variant-level detail (shows each plan variant separately)
output/enrollment_pivot_variants.csv

# Grouped summary (sums variants by EPO/PPO/VALUE)
output/enrollment_pivot_grouped.csv
```

### 2. Integrity Checks
The script now validates that tier sums equal total subscribers:
```
=== INTEGRITY CHECKS ===
✓ All integrity checks passed!
```

### 3. Unknown Auditing
See unmapped values that need mapping updates:
```
=== UNKNOWN AUDIT ===
Found 5 UNKNOWN tiers
Top unmapped tier values:
  EMPLOYEE_PLUS: 3
  EMP+1: 2
```

## Rollback Plan

If you need to rollback:

1. **Keep using enrollment_automation.py** (has the bug but is stable)
2. **Document known issues** in your reports
3. **Plan migration** when ready

## Data Mapping Updates

If you see many UNKNOWN values after migration:

1. **Update tier mappings in normalize_tier():**
```python
# Add new variants like:
if tier_str in ['YOUR_VARIANT', 'ANOTHER_VARIANT']:
    return 'EE+Spouse'
```

2. **Update plan mappings in PLAN_TO_TYPE dictionary:**
```python
PLAN_TO_TYPE['NEWPLANCODE'] = 'EPO'
```

## Support

If you encounter issues:

1. Run the test script: `python test_enrollment_fix.py`
2. Review ENROLLMENT_FIX_SUMMARY.md for technical details
3. Check the UNKNOWN audit output for mapping gaps
4. Review the integrity check results

## Timeline Recommendation

- **Immediate:** Review this guide and test with sample data
- **This week:** Run parallel comparison of old vs new
- **Next week:** Deploy fixed version to production
- **Ongoing:** Monitor UNKNOWN audits and update mappings as needed