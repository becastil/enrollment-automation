"""
Enrollment Reconciliation Report Generator
==========================================

This script generates detailed reconciliation reports comparing source data
to generated output, identifying discrepancies and their root causes.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import json
import os
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

class EnrollmentReconciliation:
    """Generate reconciliation reports for enrollment data"""
    
    def __init__(self, source_file: str, output_file: str):
        """Initialize with source and output file paths"""
        self.source_file = source_file
        self.output_file = output_file
        self.discrepancies = []
        self.facility_variances = {}
        
    def load_source_data(self) -> pd.DataFrame:
        """Load source enrollment data"""
        try:
            df = pd.read_excel(self.source_file, sheet_name="Cleaned use this one", header=4)
            return df
        except Exception as e:
            print(f"Error loading source data: {e}")
            return pd.DataFrame()
            
    def load_output_data(self) -> Dict:
        """Load generated output data from all facility tabs"""
        output_data = {}
        try:
            xl = pd.ExcelFile(self.output_file)
            for sheet in xl.sheet_names:
                if sheet in FACILITY_TABS:
                    df = pd.read_excel(xl, sheet_name=sheet)
                    output_data[sheet] = self.extract_enrollment_counts(df)
        except Exception as e:
            print(f"Error loading output data: {e}")
        return output_data
        
    def extract_enrollment_counts(self, df: pd.DataFrame) -> Dict:
        """Extract enrollment counts from a facility tab"""
        counts = {
            "EMP": 0, "ESP": 0, "ECH": 0, "FAM": 0
        }
        
        # Logic to extract counts from specific cells based on tab structure
        # This would need to be customized per tab format
        return counts
        
    def calculate_source_totals(self, df: pd.DataFrame) -> Dict:
        """Calculate totals from source data by facility"""
        facility_totals = {}
        
        # Group by CLIENT ID and BEN CODE
        if 'CLIENT ID' in df.columns and 'BEN CODE' in df.columns:
            grouped = df.groupby(['CLIENT ID', 'BEN CODE']).size().reset_index(name='count')
            
            for client_id in grouped['CLIENT ID'].unique():
                client_data = grouped[grouped['CLIENT ID'] == client_id]
                facility_totals[client_id] = {
                    'EMP': int(client_data[client_data['BEN CODE'] == 'EMP']['count'].sum()),
                    'ESP': int(client_data[client_data['BEN CODE'] == 'ESP']['count'].sum()),
                    'ECH': int(client_data[client_data['BEN CODE'] == 'ECH']['count'].sum()),
                    'E1D': int(client_data[client_data['BEN CODE'] == 'E1D']['count'].sum()),
                    'FAM': int(client_data[client_data['BEN CODE'] == 'FAM']['count'].sum())
                }
                
        return facility_totals
        
    def identify_discrepancies(self, source_totals: Dict, output_totals: Dict) -> List[Dict]:
        """Identify and categorize discrepancies"""
        discrepancies = []
        
        # Define thresholds for different severity levels
        VARIANCE_THRESHOLDS = {
            'critical': 100,  # >100 difference
            'major': 50,      # 50-100 difference  
            'minor': 10,      # 10-50 difference
            'acceptable': 5   # <10 difference
        }
        
        for facility, source_counts in source_totals.items():
            if facility in output_totals:
                output_counts = output_totals[facility]
                
                for tier in ['EMP', 'ESP', 'ECH', 'FAM']:
                    source_val = source_counts.get(tier, 0)
                    # Handle E1D + ECH combination for 4-tier
                    if tier == 'ECH':
                        source_val += source_counts.get('E1D', 0)
                    
                    output_val = output_counts.get(tier, 0)
                    variance = output_val - source_val
                    
                    if abs(variance) > 0:
                        severity = self.categorize_variance(abs(variance), VARIANCE_THRESHOLDS)
                        
                        discrepancy = {
                            'facility': facility,
                            'tier': tier,
                            'source': source_val,
                            'output': output_val,
                            'variance': variance,
                            'variance_pct': (variance / source_val * 100) if source_val > 0 else 0,
                            'severity': severity,
                            'probable_cause': self.identify_probable_cause(facility, tier, variance)
                        }
                        discrepancies.append(discrepancy)
                        
        return discrepancies
        
    def categorize_variance(self, variance: int, thresholds: Dict) -> str:
        """Categorize variance severity"""
        if variance >= thresholds['critical']:
            return 'CRITICAL'
        elif variance >= thresholds['major']:
            return 'MAJOR'
        elif variance >= thresholds['minor']:
            return 'MINOR'
        else:
            return 'ACCEPTABLE'
            
    def identify_probable_cause(self, facility: str, tier: str, variance: int) -> str:
        """Identify probable cause of discrepancy based on patterns"""
        causes = []
        
        # Known issue patterns
        if facility in ['H3250', 'H3260'] and variance > 100:
            causes.append("5-tier structure miscalculation")
            
        if facility == 'H3530' and variance > 100:
            causes.append("Multi-block aggregation error")
            
        if facility in ['H3395', 'H3396', 'H3394'] and tier == 'ECH':
            causes.append("E1D/ECH tier misclassification")
            
        if facility.startswith('H36'):  # Illinois facilities
            causes.append("Incomplete facility mapping")
            
        if tier == 'ECH' and variance > 50:
            causes.append("Child tier aggregation issue")
            
        return "; ".join(causes) if causes else "Unknown"
        
    def generate_summary_report(self, discrepancies: List[Dict]) -> pd.DataFrame:
        """Generate summary report of discrepancies"""
        if not discrepancies:
            return pd.DataFrame()
            
        df = pd.DataFrame(discrepancies)
        
        # Add facility name mapping
        df['facility_name'] = df['facility'].map(FACILITY_NAMES)
        
        # Sort by severity and variance magnitude
        severity_order = {'CRITICAL': 0, 'MAJOR': 1, 'MINOR': 2, 'ACCEPTABLE': 3}
        df['severity_rank'] = df['severity'].map(severity_order)
        df = df.sort_values(['severity_rank', 'variance'], ascending=[True, False])
        
        return df
        
    def generate_detailed_report(self) -> Dict:
        """Generate comprehensive reconciliation report"""
        report = {
            'generated_at': datetime.now().isoformat(),
            'source_file': self.source_file,
            'output_file': self.output_file,
            'summary': {},
            'critical_issues': [],
            'recommendations': []
        }
        
        # Load data
        source_df = self.load_source_data()
        source_totals = self.calculate_source_totals(source_df)
        output_totals = self.load_output_data()
        
        # Identify discrepancies
        discrepancies = self.identify_discrepancies(source_totals, output_totals)
        
        # Generate summary statistics
        if discrepancies:
            df = pd.DataFrame(discrepancies)
            report['summary'] = {
                'total_discrepancies': len(discrepancies),
                'critical_count': len(df[df['severity'] == 'CRITICAL']),
                'major_count': len(df[df['severity'] == 'MAJOR']),
                'minor_count': len(df[df['severity'] == 'MINOR']),
                'total_variance': df['variance'].sum(),
                'affected_facilities': df['facility'].nunique()
            }
            
            # Identify critical issues
            critical = df[df['severity'] == 'CRITICAL']
            for _, row in critical.iterrows():
                issue = {
                    'facility': row['facility'],
                    'facility_name': FACILITY_NAMES.get(row['facility'], 'Unknown'),
                    'tier': row['tier'],
                    'variance': row['variance'],
                    'probable_cause': row['probable_cause']
                }
                report['critical_issues'].append(issue)
                
        # Generate recommendations
        report['recommendations'] = self.generate_recommendations(discrepancies)
        
        return report
        
    def generate_recommendations(self, discrepancies: List[Dict]) -> List[str]:
        """Generate actionable recommendations based on discrepancy patterns"""
        recommendations = []
        
        if not discrepancies:
            return ["No discrepancies found - system operating correctly"]
            
        df = pd.DataFrame(discrepancies)
        
        # Check for 5-tier issues
        five_tier_facilities = ['H3250', 'H3260', 'H3398']
        if df[df['facility'].isin(five_tier_facilities)]['variance'].abs().sum() > 500:
            recommendations.append(
                "URGENT: Review 5-tier structure implementation for Encino-Garden Grove and North Vista. "
                "Ensure CALCULATED BEN CODE is properly used and E1D tier is correctly handled."
            )
            
        # Check for multi-block issues
        if 'H3530' in df['facility'].values and df[df['facility'] == 'H3530']['variance'].abs().sum() > 500:
            recommendations.append(
                "URGENT: Audit St. Michael's multi-block aggregation configuration. "
                "Verify no duplicate PLAN codes exist across EPO blocks."
            )
            
        # Check for tier classification issues
        ech_issues = df[df['tier'] == 'ECH']['variance'].abs().sum()
        if ech_issues > 200:
            recommendations.append(
                "Review child tier classification logic. Ensure E1D and ECH are properly "
                "distinguished in 5-tier tabs and combined in 4-tier tabs."
            )
            
        # Check for missing configurations
        if any(df['probable_cause'].str.contains('Incomplete facility mapping')):
            recommendations.append(
                "Complete facility mapping configurations for Illinois tab. "
                "Ensure all 12 facilities have proper cell mappings."
            )
            
        return recommendations
        
    def export_report(self, output_dir: str = "reports"):
        """Export reconciliation report to files"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate reports
        detailed_report = self.generate_detailed_report()
        discrepancies = self.identify_discrepancies(
            self.calculate_source_totals(self.load_source_data()),
            self.load_output_data()
        )
        summary_df = self.generate_summary_report(discrepancies)
        
        # Export JSON report
        json_path = os.path.join(output_dir, f"reconciliation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(json_path, 'w') as f:
            json.dump(detailed_report, f, indent=2, default=str)
        print(f"JSON report saved to: {json_path}")
        
        # Export CSV summary
        if not summary_df.empty:
            csv_path = os.path.join(output_dir, f"discrepancies_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
            summary_df.to_csv(csv_path, index=False)
            print(f"CSV summary saved to: {csv_path}")
            
        # Print critical issues to console
        if detailed_report['critical_issues']:
            print("\n" + "="*60)
            print("CRITICAL ISSUES REQUIRING IMMEDIATE ATTENTION:")
            print("="*60)
            for issue in detailed_report['critical_issues']:
                print(f"\nFacility: {issue['facility_name']} ({issue['facility']})")
                print(f"Tier: {issue['tier']}, Variance: {issue['variance']:+d}")
                print(f"Probable Cause: {issue['probable_cause']}")
                
        # Print recommendations
        if detailed_report['recommendations']:
            print("\n" + "="*60)
            print("RECOMMENDATIONS:")
            print("="*60)
            for i, rec in enumerate(detailed_report['recommendations'], 1):
                print(f"\n{i}. {rec}")
                

# Facility tab names
FACILITY_TABS = [
    "Centinela", "Coshocton", "Dallas Medical Center", "Dallas Regional",
    "East Liverpool", "Encino-Garden Grove", "Garden City", "Harlingen",
    "Illinois", "Knapp", "Lake Huron", "Landmark", "Legacy", "Lower Bucks",
    "Mission", "Monroe", "North Vista", "Pampa", "Providence & St John",
    "Riverview & Gadsden", "Roxborough", "Saint Clare's", "Saint Mary's Passaic",
    "Saint Mary's Reno", "Southern Regional", "St Joe & St Mary's",
    "St Michael's", "St. Francis", "Suburban"
]

# Facility name mapping (partial list)
FACILITY_NAMES = {
    'H3250': 'Encino Hospital Medical Center',
    'H3260': 'Garden Grove Hospital',
    'H3530': "St. Michael's Medical Center",
    'H3395': "Saint Mary's Regional Medical Center",
    'H3398': 'North Vista Hospital',
    'H3605': 'Glendora Community Hospital',
    # Add more mappings as needed
}


def main():
    """Main execution function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate enrollment reconciliation report')
    parser.add_argument('--source', required=True, help='Path to source data Excel file')
    parser.add_argument('--output', required=True, help='Path to generated output Excel file')
    parser.add_argument('--report-dir', default='reports', help='Directory for report output')
    
    args = parser.parse_args()
    
    print("Generating Enrollment Reconciliation Report...")
    print("=" * 60)
    
    reconciler = EnrollmentReconciliation(args.source, args.output)
    reconciler.export_report(args.report_dir)
    
    print("\n" + "=" * 60)
    print("Reconciliation report generation complete!")
    

if __name__ == "__main__":
    main()