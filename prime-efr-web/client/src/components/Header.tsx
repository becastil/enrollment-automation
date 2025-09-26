import { FileSpreadsheet, AlertCircle, CheckCircle, Moon, Sun } from 'lucide-react';
import { useSelector } from 'react-redux';
import type { RootState } from '../store';
import { useTheme } from '../theme/ThemeProvider';

export default function Header() {
  const { theme, toggleTheme } = useTheme();
  const { controlTotals } = useSelector((state: RootState) => state.enrollment);
  const { summary } = useSelector((state: RootState) => state.validation);
  
  const totalEnrollment = Object.values(controlTotals).reduce((sum, val) => sum + val, 0);

  return (
    <header className="bg-surface-raised shadow">
      <div className="max-w-7xl mx-auto px-md sm:px-lg lg:px-xl py-md">
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <FileSpreadsheet className="h-8 w-8 text-primary mr-sm" />
            <div>
              <h1 className="text-2xl font-bold text-text">
                Prime Enrollment Validation System
              </h1>
              <p className="text-sm text-text-muted">
                Validate and manage enrollment data across facilities
              </p>
            </div>
          </div>
          
          <div className="flex items-center space-x-lg">
            <div className="text-right">
              <p className="text-sm text-text-muted">Total Enrollment</p>
              <p className="text-xl font-semibold text-text">
                {totalEnrollment.toLocaleString()}
              </p>
            </div>
            
            {summary && (
              <div className="flex items-center space-x-xs">
                {summary.errors > 0 ? (
                  <div className="flex items-center text-danger">
                    <AlertCircle className="h-5 w-5 mr-2xs" />
                    <span className="font-medium">{summary.errors} Errors</span>
                  </div>
                ) : (
                  <div className="flex items-center text-success">
                    <CheckCircle className="h-5 w-5 mr-2xs" />
                    <span className="font-medium">No Errors</span>
                  </div>
                )}
                {summary.warnings > 0 && (
                  <div className="flex items-center text-warning">
                    <AlertCircle className="h-5 w-5 mr-2xs" />
                    <span className="font-medium">{summary.warnings} Warnings</span>
                  </div>
                )}
              </div>
            )}
            <button
              type="button"
              onClick={toggleTheme}
              className="p-2xs rounded-full border border-border hover:bg-surface-subtle transition-colors"
              aria-label={`Switch to ${theme === 'light' ? 'dark' : 'light'} theme`}
            >
              {theme === 'light' ? (
                <Moon className="h-5 w-5 text-text" />
              ) : (
                <Sun className="h-5 w-5 text-text" />
              )}
            </button>
          </div>
        </div>
      </div>
    </header>
  );
}
