import { createSlice } from '@reduxjs/toolkit';
import type { PayloadAction } from '@reduxjs/toolkit';

export interface ValidationIssue {
  id: string;
  type: 'error' | 'warning' | 'info';
  category: 'missing_mapping' | 'tier_mismatch' | 'unassigned_plan' | 'total_mismatch' | 'multi_block';
  tab?: string;
  client_id?: string;
  plan?: string;
  message: string;
  details?: any;
  suggestedFix?: string;
}

export interface ValidationSummary {
  totalIssues: number;
  errors: number;
  warnings: number;
  info: number;
  byCategory: Record<string, number>;
  byTab: Record<string, number>;
}

interface ValidationState {
  issues: ValidationIssue[];
  summary: ValidationSummary | null;
  selectedIssue: ValidationIssue | null;
  filters: {
    type: string[];
    category: string[];
    tab: string[];
  };
}

const initialState: ValidationState = {
  issues: [],
  summary: null,
  selectedIssue: null,
  filters: {
    type: [],
    category: [],
    tab: [],
  },
};

const validationSlice = createSlice({
  name: 'validation',
  initialState,
  reducers: {
    setIssues: (state, action: PayloadAction<ValidationIssue[]>) => {
      state.issues = action.payload;
      // Calculate summary
      const summary: ValidationSummary = {
        totalIssues: action.payload.length,
        errors: 0,
        warnings: 0,
        info: 0,
        byCategory: {},
        byTab: {},
      };
      
      action.payload.forEach(issue => {
        // Count by type
        if (issue.type === 'error') summary.errors++;
        else if (issue.type === 'warning') summary.warnings++;
        else summary.info++;
        
        // Count by category
        summary.byCategory[issue.category] = (summary.byCategory[issue.category] || 0) + 1;
        
        // Count by tab
        if (issue.tab) {
          summary.byTab[issue.tab] = (summary.byTab[issue.tab] || 0) + 1;
        }
      });
      
      state.summary = summary;
    },
    addIssue: (state, action: PayloadAction<ValidationIssue>) => {
      state.issues.push(action.payload);
    },
    removeIssue: (state, action: PayloadAction<string>) => {
      state.issues = state.issues.filter(issue => issue.id !== action.payload);
    },
    selectIssue: (state, action: PayloadAction<ValidationIssue | null>) => {
      state.selectedIssue = action.payload;
    },
    setFilters: (state, action: PayloadAction<Partial<ValidationState['filters']>>) => {
      state.filters = { ...state.filters, ...action.payload };
    },
    clearValidation: (state) => {
      state.issues = [];
      state.summary = null;
      state.selectedIssue = null;
    },
  },
});

export const {
  setIssues,
  addIssue,
  removeIssue,
  selectIssue,
  setFilters,
  clearValidation,
} = validationSlice.actions;

export default validationSlice.reducer;
