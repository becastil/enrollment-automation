import { useMemo } from 'react';
import { useSelector } from 'react-redux';
import type { RootState } from '../store';
import { CheckCircle, XCircle, AlertTriangle, Info } from 'lucide-react';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';
import { useTheme } from '../theme/ThemeProvider';
import { getChartPalette } from '../utils/theme';

export default function ValidationDashboard() {
  const { theme } = useTheme();
  const { controlTotals, tabData } = useSelector((state: RootState) => state.enrollment);
  const { summary, issues } = useSelector((state: RootState) => state.validation);

  const tierData = Object.entries(controlTotals).map(([tier, count]) => ({
    name: tier,
    value: count,
  }));

  const COLORS = useMemo(() => getChartPalette(), [theme]);

  const getIssueIcon = (type: string) => {
    switch (type) {
      case 'error':
        return <XCircle className="h-5 w-5 text-danger" />;
      case 'warning':
        return <AlertTriangle className="h-5 w-5 text-warning" />;
      case 'info':
        return <Info className="h-5 w-5 text-primary" />;
      default:
        return null;
    }
  };

  return (
    <div className="space-y-lg">
      <div className="card">
        <h2 className="text-xl font-semibold mb-md">Control Totals</h2>
        
        <div className="grid grid-cols-1 gap-lg lg:grid-cols-2">
          <div>
            <h3 className="text-sm font-medium text-text-muted mb-sm">Tier Distribution</h3>
            <div className="space-y-xs">
              {Object.entries(controlTotals).map(([tier, count]) => (
                <div key={tier} className="flex justify-between items-center">
                  <span className="text-sm text-text-muted">{tier}:</span>
                  <span className="font-semibold">{count.toLocaleString()}</span>
                </div>
              ))}
              <div className="pt-xs border-t border-border">
                <div className="flex justify-between items-center">
                  <span className="text-sm font-medium text-text">Total:</span>
                  <span className="font-bold text-lg">
                    {Object.values(controlTotals).reduce((a, b) => a + b, 0).toLocaleString()}
                  </span>
                </div>
              </div>
            </div>
          </div>
          
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={tierData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  outerRadius={80}
                  fill="var(--color-primary)"
                  dataKey="value"
                >
                  {tierData.map((_, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      <div className="card">
        <h2 className="text-xl font-semibold mb-md">Validation Summary</h2>
        
        {summary ? (
          <div className="space-y-md">
            <div className="grid grid-cols-1 gap-md sm:grid-cols-2 lg:grid-cols-3">
              <div className="bg-danger-soft rounded-lg p-md border border-danger">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-danger font-medium">Errors</p>
                    <p className="text-2xl font-bold text-danger">{summary.errors}</p>
                  </div>
                  <XCircle className="h-8 w-8 text-danger" />
                </div>
              </div>
              
              <div className="bg-warning-soft rounded-lg p-md border border-warning">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-warning font-medium">Warnings</p>
                    <p className="text-2xl font-bold text-warning">{summary.warnings}</p>
                  </div>
                  <AlertTriangle className="h-8 w-8 text-warning" />
                </div>
              </div>
              
              <div className="bg-primary-soft rounded-lg p-md border border-primary">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-primary font-medium">Info</p>
                    <p className="text-2xl font-bold text-primary">{summary.info}</p>
                  </div>
                  <Info className="h-8 w-8 text-primary" />
                </div>
              </div>
            </div>

            <div>
              <h3 className="text-sm font-medium text-text-muted mb-xs">Recent Issues</h3>
              <div className="space-y-xs max-h-64 overflow-y-auto">
                {issues.slice(0, 5).map((issue) => (
                  <div
                    key={issue.id}
                    className="flex items-start space-x-sm p-sm bg-surface-subtle rounded-lg"
                  >
                    {getIssueIcon(issue.type)}
                    <div className="flex-1">
                      <p className="text-sm font-medium text-text">{issue.message}</p>
                      {issue.tab && (
                        <p className="text-xs text-text-muted mt-xs">Tab: {issue.tab}</p>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        ) : (
          <div className="text-center py-xl text-text-muted">
            <CheckCircle className="h-12 w-12 mx-auto mb-sm text-success" />
            <p>No validation issues found</p>
          </div>
        )}
      </div>

      <div className="card">
        <h2 className="text-xl font-semibold mb-md">Tab Validation Status</h2>
        
        <div className="grid grid-cols-1 gap-md sm:grid-cols-2">
          {tabData.slice(0, 10).map((tab) => (
            <div
              key={tab.name}
              className={`p-sm rounded-lg border ${
                tab.hasDiscrepancies
                  ? 'bg-danger-soft border-danger'
                  : 'bg-success-soft border-success'
              }`}
            >
              <div className="flex items-center justify-between">
                <span className="font-medium text-sm">{tab.name}</span>
                {tab.hasDiscrepancies ? (
                  <XCircle className="h-4 w-4 text-danger" />
                ) : (
                  <CheckCircle className="h-4 w-4 text-success" />
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
