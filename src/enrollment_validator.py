#!/usr/bin/env python3
"""
Data validation module for enrollment processing
Performs comprehensive data quality checks and generates validation reports
"""

import pandas as pd
import numpy as np
import json
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class EnrollmentValidator:
    """Validates enrollment data quality and completeness"""
    
    def __init__(self, config_path='config.json'):
        """Initialize validator with configuration"""
        with open(config_path, 'r') as f:
            self.config = json.load(f)['enrollment_processing']
        
        self.validation_results = []
        self.issues_found = []
    
    def validate_enriched_data(self, enriched_df):
        """Validate enriched enrollment data"""
        
        print("=" * 80)
        print("DATA VALIDATION REPORT")
        print("=" * 80)
        print(f"Validating {len(enriched_df)} records...")
        print()
        
        # Run validation checks
        self._check_missing_mappings(enriched_df)
        self._check_duplicate_contracts(enriched_df)
        self._check_data_completeness(enriched_df)
        self._check_sequence_integrity(enriched_df)
        self._check_plan_distribution(enriched_df)
        self._check_facility_distribution(enriched_df)
        
        # Generate summary
        self._generate_validation_summary()
        
        return self.validation_results, self.issues_found
    
    def _check_missing_mappings(self, df):
        """Check for records with missing facility or plan mappings"""
        
        results = {}
        
        # Check facility mappings
        if 'missing_facility_flag' in df.columns:
            missing_fac = df['missing_facility_flag'].sum()
            results['missing_facilities'] = missing_fac
            
            if missing_fac > 0:
                self._log_issue("WARNING", f"{missing_fac} records missing facility mapping",
                              df[df['missing_facility_flag']]['CLIENT ID'].unique()[:5].tolist())
        
        # Check plan mappings
        if 'missing_plan_flag' in df.columns:
            missing_plan = df['missing_plan_flag'].sum()
            results['missing_plans'] = missing_plan
            
            if missing_plan > 0:
                self._log_issue("WARNING", f"{missing_plan} records missing plan mapping",
                              df[df['missing_plan_flag']]['PLAN'].unique()[:5].tolist())
        
        if not results or (results.get('missing_facilities', 0) == 0 and 
                          results.get('missing_plans', 0) == 0):
            self._log_validation("Mapping Completeness", "PASS", 
                               "All records have valid facility and plan mappings")
        else:
            self._log_validation("Mapping Completeness", "WARN",
                               f"Missing: {results.get('missing_facilities', 0)} facilities, "
                               f"{results.get('missing_plans', 0)} plans")
    
    def _check_duplicate_contracts(self, df):
        """Check for duplicate contract IDs"""
        
        alt_id_col = self.config['column_mappings'].get('alt_id_col', 'ALT ID')
        
        if alt_id_col in df.columns:
            # Check for duplicates
            duplicates = df[alt_id_col].duplicated()
            num_duplicates = duplicates.sum()
            
            if num_duplicates > 0:
                # Find duplicate IDs
                duplicate_ids = df[duplicates][alt_id_col].unique()[:10]
                
                self._log_validation("Contract Uniqueness", "INFO",
                                   f"{num_duplicates} duplicate records found (expected for dependents)")
                
                # Check if duplicates are properly sequenced
                seq_col = self.config['column_mappings'].get('sequence_col', 'SEQ. #')
                if seq_col in df.columns:
                    for dup_id in duplicate_ids[:3]:  # Check first 3 duplicates
                        dup_records = df[df[alt_id_col] == dup_id]
                        seq_values = sorted(dup_records[seq_col].unique())
                        if seq_values[0] != 0:
                            self._log_issue("ERROR", f"Contract {dup_id} missing subscriber (SEQ=0)")
            else:
                self._log_validation("Contract Uniqueness", "PASS",
                                   "No unexpected duplicates found")
    
    def _check_data_completeness(self, df):
        """Check for missing required fields"""
        
        required_fields = {
            'CLIENT ID': self.config['column_mappings']['facility_key_col'],
            'PLAN': self.config['column_mappings']['plan_type_col'],
            'ALT ID': self.config['column_mappings'].get('alt_id_col', 'ALT ID')
        }
        
        missing_data = {}
        for field_name, col_name in required_fields.items():
            if col_name in df.columns:
                missing_count = df[col_name].isna().sum()
                if missing_count > 0:
                    missing_data[field_name] = missing_count
        
        if missing_data:
            self._log_validation("Data Completeness", "WARN",
                               f"Missing values: {missing_data}")
        else:
            self._log_validation("Data Completeness", "PASS",
                               "All required fields populated")
    
    def _check_sequence_integrity(self, df):
        """Check sequence number integrity for contracts"""
        
        seq_col = self.config['column_mappings'].get('sequence_col', 'SEQ. #')
        alt_id_col = self.config['column_mappings'].get('alt_id_col', 'ALT ID')
        
        if seq_col in df.columns and alt_id_col in df.columns:
            # Group by contract and check sequence
            contract_groups = df.groupby(alt_id_col)[seq_col].agg(['min', 'max', 'count', 'nunique'])
            
            # Check for contracts without subscriber (SEQ=0)
            no_subscriber = contract_groups[contract_groups['min'] > 0]
            if len(no_subscriber) > 0:
                self._log_issue("ERROR", f"{len(no_subscriber)} contracts missing subscriber record",
                              no_subscriber.index[:5].tolist())
            
            # Check for sequence gaps
            contracts_with_gaps = []
            for contract_id in contract_groups.index[:100]:  # Check first 100 contracts
                sequences = sorted(df[df[alt_id_col] == contract_id][seq_col].unique())
                expected = list(range(int(min(sequences)), int(max(sequences)) + 1))
                if sequences != expected and len(sequences) > 1:
                    contracts_with_gaps.append(contract_id)
            
            if contracts_with_gaps:
                self._log_issue("WARNING", f"{len(contracts_with_gaps)} contracts have sequence gaps",
                              contracts_with_gaps[:5])
            
            # Summary
            total_contracts = contract_groups.shape[0]
            single_member = (contract_groups['count'] == 1).sum()
            multi_member = (contract_groups['count'] > 1).sum()
            
            self._log_validation("Sequence Integrity", "PASS",
                               f"{total_contracts} contracts: {single_member} single, {multi_member} multi-member")
    
    def _check_plan_distribution(self, df):
        """Analyze plan type distribution"""
        
        plan_col = self.config['column_mappings']['plan_type_col']
        
        if plan_col in df.columns:
            plan_dist = df[plan_col].value_counts()
            
            # Check for unusual distributions
            total_records = len(df)
            top_plan_pct = (plan_dist.iloc[0] / total_records) * 100
            
            if top_plan_pct > 80:
                self._log_issue("INFO", f"High concentration in single plan: {plan_dist.index[0]} ({top_plan_pct:.1f}%)")
            
            # EPO/PPO/VALUE distribution
            if 'plan_group' in df.columns:
                group_dist = df['plan_group'].value_counts()
                self._log_validation("Plan Distribution", "INFO",
                                   f"Plan groups: {dict(group_dist)}")
            else:
                self._log_validation("Plan Distribution", "INFO",
                                   f"{len(plan_dist)} unique plans, top 3: {dict(plan_dist.head(3))}")
    
    def _check_facility_distribution(self, df):
        """Analyze facility distribution"""
        
        facility_col = self.config['column_mappings']['facility_key_col']
        
        if facility_col in df.columns:
            facility_dist = df[facility_col].value_counts()
            
            # Check for facilities with very few enrollments
            small_facilities = facility_dist[facility_dist < 10]
            if len(small_facilities) > 0:
                self._log_issue("INFO", f"{len(small_facilities)} facilities with <10 enrollments",
                              small_facilities.index[:5].tolist())
            
            # Summary statistics
            stats = {
                'total_facilities': len(facility_dist),
                'avg_enrollment': facility_dist.mean(),
                'max_enrollment': facility_dist.max(),
                'min_enrollment': facility_dist.min()
            }
            
            self._log_validation("Facility Distribution", "INFO",
                               f"{stats['total_facilities']} facilities, "
                               f"avg: {stats['avg_enrollment']:.0f}, "
                               f"range: {stats['min_enrollment']}-{stats['max_enrollment']}")
    
    def _log_validation(self, check_name, status, message):
        """Log validation result"""
        self.validation_results.append({
            'check': check_name,
            'status': status,
            'message': message,
            'timestamp': datetime.now().isoformat()
        })
        
        # Print result
        status_symbol = "✓" if status == "PASS" else "⚠" if status in ["WARN", "INFO"] else "✗"
        print(f"{status_symbol} {check_name}: {message}")
    
    def _log_issue(self, severity, description, examples=None):
        """Log data quality issue"""
        issue = {
            'severity': severity,
            'description': description,
            'timestamp': datetime.now().isoformat()
        }
        
        if examples:
            issue['examples'] = examples
        
        self.issues_found.append(issue)
        
        # Print issue
        severity_symbol = "✗" if severity == "ERROR" else "⚠" if severity == "WARNING" else "ℹ"
        print(f"{severity_symbol} {severity}: {description}")
        if examples:
            print(f"  Examples: {examples}")
    
    def _generate_validation_summary(self):
        """Generate validation summary"""
        
        print("\n" + "=" * 80)
        print("VALIDATION SUMMARY")
        print("=" * 80)
        
        # Count by status
        status_counts = {}
        for result in self.validation_results:
            status = result['status']
            status_counts[status] = status_counts.get(status, 0) + 1
        
        print(f"Checks performed: {len(self.validation_results)}")
        for status, count in status_counts.items():
            print(f"  {status}: {count}")
        
        # Count issues by severity
        if self.issues_found:
            severity_counts = {}
            for issue in self.issues_found:
                severity = issue['severity']
                severity_counts[severity] = severity_counts.get(severity, 0) + 1
            
            print(f"\nIssues found: {len(self.issues_found)}")
            for severity, count in severity_counts.items():
                print(f"  {severity}: {count}")
        else:
            print("\nNo critical issues found")
    
    def export_validation_report(self, output_path='validation_report.csv'):
        """Export validation results to CSV"""
        
        # Create report dataframe
        report_df = pd.DataFrame(self.validation_results)
        report_df.to_csv(output_path, index=False)
        
        # Export issues if any
        if self.issues_found:
            issues_df = pd.DataFrame(self.issues_found)
            issues_path = output_path.replace('.csv', '_issues.csv')
            issues_df.to_csv(issues_path, index=False)
            print(f"\nValidation reports exported:")
            print(f"  - {output_path}")
            print(f"  - {issues_path}")
        else:
            print(f"\nValidation report exported: {output_path}")


def validate_enrollment_data(enriched_df, config_path='config.json'):
    """Convenience function to validate enrollment data"""
    
    validator = EnrollmentValidator(config_path)
    results, issues = validator.validate_enriched_data(enriched_df)
    validator.export_validation_report()
    
    return results, issues


if __name__ == "__main__":
    # Example usage
    print("Loading enrollment data for validation...")
    
    import json
    from enrollment_data_processing import build_facility_summary
    
    # Load config
    with open('config.json', 'r') as f:
        config = json.load(f)['enrollment_processing']
    
    # Load mappings
    facility_map = pd.read_csv(config['reference_files']['facility_mapping'])
    plan_map = pd.read_csv(config['reference_files']['plan_mapping'])
    
    # Process data
    enriched, _, _ = build_facility_summary(
        excel_path=config['excel_file']['path'],
        sheet_name=config['excel_file']['main_sheet'],
        facility_key_col=config['column_mappings']['facility_key_col'],
        plan_type_col=config['column_mappings']['plan_type_col'],
        facility_map=facility_map,
        plan_map=plan_map
    )
    
    # Validate
    validator = EnrollmentValidator()
    results, issues = validator.validate_enriched_data(enriched)
    validator.export_validation_report()
    
    print("\n✓ Validation complete!")