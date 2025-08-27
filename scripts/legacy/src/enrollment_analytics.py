#!/usr/bin/env python3
"""
Advanced analytics and reporting module for enrollment data
Generates insights, trends, and comprehensive reports
"""

import pandas as pd
import numpy as np
import json
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class EnrollmentAnalytics:
    """Generate advanced analytics and insights from enrollment data"""
    
    def __init__(self, config_path='config.json'):
        """Initialize analytics engine"""
        with open(config_path, 'r') as f:
            self.config = json.load(f)['enrollment_processing']
        
        self.analytics_results = {}
    
    def analyze_summary_data(self, summary_df):
        """Perform comprehensive analysis on summary data"""
        
        print("=" * 80)
        print("ENROLLMENT ANALYTICS REPORT")
        print("=" * 80)
        print(f"Analyzing {len(summary_df)} summary records...")
        print()
        
        # Perform analyses
        self._analyze_overall_metrics(summary_df)
        self._analyze_facility_performance(summary_df)
        self._analyze_plan_distribution(summary_df)
        self._analyze_facility_plan_mix(summary_df)
        self._identify_outliers(summary_df)
        self._generate_recommendations(summary_df)
        
        return self.analytics_results
    
    def _analyze_overall_metrics(self, df):
        """Calculate overall enrollment metrics"""
        
        print("OVERALL METRICS")
        print("-" * 40)
        
        metrics = {}
        
        # Total enrollment
        if 'contract_count' in df.columns:
            metrics['total_contracts'] = df['contract_count'].sum()
            metrics['avg_contracts_per_facility'] = df.groupby('facility_name')['contract_count'].sum().mean()
            metrics['median_contracts_per_facility'] = df.groupby('facility_name')['contract_count'].sum().median()
        
        # Facility metrics
        metrics['total_facilities'] = df['facility_name'].nunique()
        metrics['facilities_with_multiple_plans'] = (df.groupby('facility_name')['plan_group'].nunique() > 1).sum()
        
        # Plan metrics
        metrics['total_plan_groups'] = df['plan_group'].nunique()
        
        # Store and display
        self.analytics_results['overall_metrics'] = metrics
        
        for key, value in metrics.items():
            if isinstance(value, float):
                print(f"  {key.replace('_', ' ').title()}: {value:.1f}")
            else:
                print(f"  {key.replace('_', ' ').title()}: {value}")
        
        print()
    
    def _analyze_facility_performance(self, df):
        """Analyze facility-level performance"""
        
        print("FACILITY PERFORMANCE")
        print("-" * 40)
        
        if 'contract_count' not in df.columns:
            print("  No contract count data available")
            return
        
        # Aggregate by facility
        facility_stats = df.groupby('facility_name').agg({
            'contract_count': 'sum',
            'plan_group': 'nunique',
            'client_id': 'first'
        }).rename(columns={
            'contract_count': 'total_contracts',
            'plan_group': 'plan_groups_offered'
        })
        
        facility_stats = facility_stats.sort_values('total_contracts', ascending=False)
        
        # Categorize facilities
        total_contracts = facility_stats['total_contracts'].sum()
        facility_stats['pct_of_total'] = (facility_stats['total_contracts'] / total_contracts * 100)
        
        # Identify tiers
        facility_stats['tier'] = pd.cut(facility_stats['total_contracts'],
                                       bins=[0, 100, 500, 1000, np.inf],
                                       labels=['Small', 'Medium', 'Large', 'Enterprise'])
        
        # Top performers
        print("  Top 5 Facilities by Enrollment:")
        for idx, row in facility_stats.head(5).iterrows():
            print(f"    {idx}: {row['total_contracts']} contracts ({row['pct_of_total']:.1f}%)")
        
        print("\n  Facility Tiers:")
        tier_summary = facility_stats.groupby('tier').agg({
            'total_contracts': ['count', 'sum', 'mean']
        })
        print(tier_summary)
        
        self.analytics_results['facility_performance'] = facility_stats.to_dict()
        print()
    
    def _analyze_plan_distribution(self, df):
        """Analyze plan type distribution"""
        
        print("PLAN DISTRIBUTION ANALYSIS")
        print("-" * 40)
        
        if 'contract_count' not in df.columns:
            print("  No contract count data available")
            return
        
        # Aggregate by plan group
        plan_stats = df.groupby('plan_group').agg({
            'contract_count': 'sum',
            'facility_name': 'nunique'
        }).rename(columns={
            'contract_count': 'total_contracts',
            'facility_name': 'facilities_offering'
        })
        
        plan_stats['pct_of_total'] = (plan_stats['total_contracts'] / plan_stats['total_contracts'].sum() * 100)
        plan_stats['avg_per_facility'] = plan_stats['total_contracts'] / plan_stats['facilities_offering']
        
        print("  Plan Group Distribution:")
        for idx, row in plan_stats.iterrows():
            print(f"    {idx}: {row['total_contracts']} contracts ({row['pct_of_total']:.1f}%), "
                  f"offered by {row['facilities_offering']} facilities")
        
        # EPO vs PPO vs VALUE analysis
        if 'EPO' in plan_stats.index and 'VALUE' in plan_stats.index:
            epo_value_ratio = plan_stats.loc['EPO', 'total_contracts'] / plan_stats.loc['VALUE', 'total_contracts']
            print(f"\n  EPO to VALUE ratio: {epo_value_ratio:.2f}:1")
        
        self.analytics_results['plan_distribution'] = plan_stats.to_dict()
        print()
    
    def _analyze_facility_plan_mix(self, df):
        """Analyze the mix of plans at each facility"""
        
        print("FACILITY PLAN MIX ANALYSIS")
        print("-" * 40)
        
        if 'contract_count' not in df.columns:
            print("  No contract count data available")
            return
        
        # Pivot to see plan mix by facility
        plan_mix = df.pivot_table(
            index='facility_name',
            columns='plan_group',
            values='contract_count',
            fill_value=0,
            aggfunc='sum'
        )
        
        # Calculate percentages
        plan_mix_pct = plan_mix.div(plan_mix.sum(axis=1), axis=0) * 100
        
        # Identify facilities with heavy concentration in one plan
        max_concentration = plan_mix_pct.max(axis=1)
        concentrated_facilities = max_concentration[max_concentration > 90]
        
        if len(concentrated_facilities) > 0:
            print(f"  Facilities with >90% concentration in single plan type: {len(concentrated_facilities)}")
            for facility in concentrated_facilities.head(5).index:
                dominant_plan = plan_mix_pct.loc[facility].idxmax()
                concentration = plan_mix_pct.loc[facility, dominant_plan]
                print(f"    {facility}: {concentration:.1f}% in {dominant_plan}")
        
        # Balanced facilities (offering multiple plans with reasonable distribution)
        if len(plan_mix.columns) > 1:
            std_dev = plan_mix_pct.std(axis=1)
            balanced_facilities = std_dev[std_dev < 30]
            
            if len(balanced_facilities) > 0:
                print(f"\n  Well-balanced facilities (std dev < 30%): {len(balanced_facilities)}")
                for facility in balanced_facilities.head(3).index:
                    mix = plan_mix_pct.loc[facility]
                    mix_str = ", ".join([f"{plan}: {pct:.0f}%" for plan, pct in mix.items() if pct > 0])
                    print(f"    {facility}: {mix_str}")
        
        self.analytics_results['plan_mix'] = plan_mix_pct.to_dict()
        print()
    
    def _identify_outliers(self, df):
        """Identify statistical outliers and anomalies"""
        
        print("OUTLIER ANALYSIS")
        print("-" * 40)
        
        if 'contract_count' not in df.columns:
            print("  No contract count data available")
            return
        
        outliers = []
        
        # Facility-level outliers
        facility_totals = df.groupby('facility_name')['contract_count'].sum()
        q1 = facility_totals.quantile(0.25)
        q3 = facility_totals.quantile(0.75)
        iqr = q3 - q1
        
        # High outliers (unusually high enrollment)
        high_outliers = facility_totals[facility_totals > q3 + 1.5 * iqr]
        if len(high_outliers) > 0:
            print(f"  High enrollment outliers (>{q3 + 1.5 * iqr:.0f} contracts):")
            for facility, count in high_outliers.items():
                print(f"    {facility}: {count} contracts")
                outliers.append({'type': 'high_enrollment', 'facility': facility, 'value': count})
        
        # Low outliers (unusually low enrollment)
        low_outliers = facility_totals[facility_totals < q1 - 1.5 * iqr]
        if len(low_outliers) > 0 and q1 - 1.5 * iqr > 0:
            print(f"\n  Low enrollment outliers (<{q1 - 1.5 * iqr:.0f} contracts):")
            for facility, count in low_outliers.items():
                print(f"    {facility}: {count} contracts")
                outliers.append({'type': 'low_enrollment', 'facility': facility, 'value': count})
        
        # Facilities with single plan group only
        single_plan_facilities = df.groupby('facility_name')['plan_group'].nunique()
        single_plan_facilities = single_plan_facilities[single_plan_facilities == 1]
        
        if len(single_plan_facilities) > 0:
            print(f"\n  Facilities offering only one plan type: {len(single_plan_facilities)}")
            for facility in single_plan_facilities.head(5).index:
                plan = df[df['facility_name'] == facility]['plan_group'].iloc[0]
                print(f"    {facility}: {plan} only")
        
        self.analytics_results['outliers'] = outliers
        print()
    
    def _generate_recommendations(self, df):
        """Generate actionable recommendations based on analysis"""
        
        print("RECOMMENDATIONS")
        print("-" * 40)
        
        recommendations = []
        
        if 'contract_count' not in df.columns:
            print("  No contract count data available for recommendations")
            return
        
        # Check plan diversity
        facilities_single_plan = df.groupby('facility_name')['plan_group'].nunique()
        facilities_single_plan = facilities_single_plan[facilities_single_plan == 1]
        
        if len(facilities_single_plan) > 5:
            recommendations.append({
                'priority': 'HIGH',
                'category': 'Plan Diversity',
                'recommendation': f"Consider expanding plan offerings at {len(facilities_single_plan)} single-plan facilities",
                'impact': 'Could increase enrollment options and member satisfaction'
            })
        
        # Check for underperforming facilities
        facility_totals = df.groupby('facility_name')['contract_count'].sum()
        bottom_quartile = facility_totals.quantile(0.25)
        underperformers = facility_totals[facility_totals < bottom_quartile]
        
        if len(underperformers) > 0:
            recommendations.append({
                'priority': 'MEDIUM',
                'category': 'Facility Performance',
                'recommendation': f"Review enrollment strategies for {len(underperformers)} facilities in bottom quartile",
                'impact': f"Potential to increase enrollment by targeting facilities below {bottom_quartile:.0f} contracts"
            })
        
        # Check EPO/PPO/VALUE balance
        plan_totals = df.groupby('plan_group')['contract_count'].sum()
        if 'VALUE' in plan_totals.index:
            value_pct = plan_totals['VALUE'] / plan_totals.sum() * 100
            if value_pct < 10:
                recommendations.append({
                    'priority': 'LOW',
                    'category': 'Plan Balance',
                    'recommendation': f"VALUE plans represent only {value_pct:.1f}% of enrollment",
                    'impact': 'Consider promoting VALUE plans for cost-conscious members'
                })
        
        # Display recommendations
        for rec in recommendations:
            print(f"  [{rec['priority']}] {rec['category']}")
            print(f"    {rec['recommendation']}")
            print(f"    Impact: {rec['impact']}")
            print()
        
        self.analytics_results['recommendations'] = recommendations
    
    def export_analytics_report(self, summary_df, output_prefix='analytics'):
        """Export comprehensive analytics report"""
        
        # Create multi-sheet Excel file
        with pd.ExcelWriter(f'{output_prefix}_report.xlsx', engine='openpyxl') as writer:
            
            # Summary statistics
            summary_df.to_excel(writer, sheet_name='Summary Data', index=False)
            
            # Facility performance
            if 'facility_performance' in self.analytics_results:
                facility_df = pd.DataFrame(self.analytics_results['facility_performance'])
                facility_df.to_excel(writer, sheet_name='Facility Performance')
            
            # Plan distribution
            if 'plan_distribution' in self.analytics_results:
                plan_df = pd.DataFrame(self.analytics_results['plan_distribution'])
                plan_df.to_excel(writer, sheet_name='Plan Distribution')
            
            # Recommendations
            if 'recommendations' in self.analytics_results:
                rec_df = pd.DataFrame(self.analytics_results['recommendations'])
                rec_df.to_excel(writer, sheet_name='Recommendations', index=False)
        
        print(f"\nAnalytics report exported: {output_prefix}_report.xlsx")
        
        # Also export key metrics as JSON
        metrics = self.analytics_results.get('overall_metrics', {})
        # Convert numpy types to Python types for JSON serialization
        metrics_json = {k: float(v) if isinstance(v, (np.integer, np.floating)) else v 
                       for k, v in metrics.items()}
        with open(f'{output_prefix}_metrics.json', 'w') as f:
            json.dump(metrics_json, f, indent=2)
        
        print(f"Key metrics exported: {output_prefix}_metrics.json")


def generate_analytics_report(summary_df, config_path='config.json'):
    """Convenience function to generate analytics report"""
    
    analytics = EnrollmentAnalytics(config_path)
    results = analytics.analyze_summary_data(summary_df)
    analytics.export_analytics_report(summary_df)
    
    return results


if __name__ == "__main__":
    # Example usage
    print("Loading enrollment summary for analysis...")
    
    # Try to load existing summary
    try:
        summary_df = pd.read_csv('enrollment_summary_cleaned_sheet.csv')
    except:
        # Generate summary if not exists
        import json
        from enrollment_data_processing import build_facility_summary
        
        with open('config.json', 'r') as f:
            config = json.load(f)['enrollment_processing']
        
        facility_map = pd.read_csv(config['reference_files']['facility_mapping'])
        plan_map = pd.read_csv(config['reference_files']['plan_mapping'])
        
        _, summary_df, _ = build_facility_summary(
            excel_path=config['excel_file']['path'],
            sheet_name=config['excel_file']['main_sheet'],
            facility_key_col=config['column_mappings']['facility_key_col'],
            plan_type_col=config['column_mappings']['plan_type_col'],
            facility_map=facility_map,
            plan_map=plan_map
        )
    
    # Generate analytics
    analytics = EnrollmentAnalytics()
    results = analytics.analyze_summary_data(summary_df)
    analytics.export_analytics_report(summary_df)
    
    print("\n✓ Analytics report complete!")