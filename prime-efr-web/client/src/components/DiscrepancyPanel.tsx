import { useSelector, useDispatch } from 'react-redux';
import type { RootState, AppDispatch } from '../store';
import { selectIssue, removeIssue } from '../store/slices/validationSlice';
import { AlertTriangle, XCircle, Info, X, CheckCircle } from 'lucide-react';

export default function DiscrepancyPanel() {
  const dispatch = useDispatch<AppDispatch>();
  const { issues, selectedIssue, filters } = useSelector(
    (state: RootState) => state.validation
  );

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

  const getCategoryLabel = (category: string) => {
    const labels: Record<string, string> = {
      missing_mapping: 'Missing Mapping',
      tier_mismatch: 'Tier Mismatch',
      unassigned_plan: 'Unassigned Plan',
      total_mismatch: 'Total Mismatch',
      multi_block: 'Multi-Block Issue',
    };
    return labels[category] || category;
  };

  const filteredIssues = issues.filter(issue => {
    if (filters.type.length > 0 && !filters.type.includes(issue.type)) return false;
    if (filters.category.length > 0 && !filters.category.includes(issue.category)) return false;
    if (filters.tab.length > 0 && issue.tab && !filters.tab.includes(issue.tab)) return false;
    return true;
  });

  const handleApplyFix = (issue: typeof selectedIssue) => {
    if (!issue || !issue.suggestedFix) return;
    
    // This would trigger the fix application logic
    console.log('Applying fix:', issue.suggestedFix);
    dispatch(removeIssue(issue.id));
    dispatch(selectIssue(null));
  };

  return (
    <div className="card">
      <h2 className="text-xl font-semibold mb-md">Discrepancies</h2>
      
      {selectedIssue && (
        <div className="mb-md p-md bg-surface-subtle rounded-lg border border-border">
          <div className="flex items-start justify-between mb-xs">
            <div className="flex items-start space-x-xs">
              {getIssueIcon(selectedIssue.type)}
              <div>
                <p className="font-medium text-text">{selectedIssue.message}</p>
                <p className="text-sm text-text-muted mt-xs">
                  {getCategoryLabel(selectedIssue.category)}
                  {selectedIssue.tab && ` • ${selectedIssue.tab}`}
                </p>
              </div>
            </div>
            <button
              onClick={() => dispatch(selectIssue(null))}
              className="p-2xs hover:bg-surface-subtle rounded"
            >
              <X className="h-4 w-4 text-text-muted" />
            </button>
          </div>
          
          {selectedIssue.details && (
            <div className="mt-sm p-sm bg-surface rounded border border-border">
              <p className="text-xs font-medium text-text-muted mb-2xs">Details</p>
              <pre className="text-xs text-text overflow-x-auto">
                {JSON.stringify(selectedIssue.details, null, 2)}
              </pre>
            </div>
          )}
          
          {selectedIssue.suggestedFix && (
            <div className="mt-sm">
              <p className="text-sm font-medium text-text mb-xs">Suggested Fix:</p>
              <p className="text-sm text-text-muted">{selectedIssue.suggestedFix}</p>
              <button
                onClick={() => handleApplyFix(selectedIssue)}
                className="mt-2 btn-primary text-sm"
              >
                Apply Fix
              </button>
            </div>
          )}
        </div>
      )}
      
      <div className="space-y-xs max-h-96 overflow-y-auto">
        {filteredIssues.length === 0 ? (
          <div className="text-center py-xl">
            <CheckCircle className="h-12 w-12 mx-auto mb-sm text-success" />
            <p className="text-text-muted">No discrepancies found</p>
          </div>
        ) : (
          filteredIssues.map((issue) => (
            <button
              key={issue.id}
              onClick={() => dispatch(selectIssue(issue))}
              className={`w-full text-left p-sm rounded-lg transition-colors ${
                selectedIssue?.id === issue.id
                  ? 'border border-primary bg-primary-soft text-primary'
                  : 'border border-border bg-surface hover:bg-surface-subtle'
              }`}
            >
              <div className="flex items-start space-x-xs">
                {getIssueIcon(issue.type)}
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-text truncate">
                    {issue.message}
                  </p>
                  <p className="text-xs text-text-muted mt-xs">
                    {getCategoryLabel(issue.category)}
                    {issue.tab && ` • ${issue.tab}`}
                  </p>
                </div>
              </div>
            </button>
          ))
        )}
      </div>
      
      {filteredIssues.length > 0 && (
        <div className="mt-md pt-md border-t border-border">
          <p className="text-sm text-text-muted">
            Showing {filteredIssues.length} of {issues.length} issues
          </p>
        </div>
      )}
    </div>
  );
}
