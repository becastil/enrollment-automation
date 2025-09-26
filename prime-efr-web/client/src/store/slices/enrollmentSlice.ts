import { createSlice } from '@reduxjs/toolkit';
import type { PayloadAction } from '@reduxjs/toolkit';

export interface EnrollmentRecord {
  CLIENT_ID: string;
  PLAN: string;
  BEN_CODE: string;
  plan_type?: string;
  tier?: string;
  count: number;
}

export interface TabData {
  name: string;
  client_ids: string[];
  blocks: BlockData[];
  totals: TierTotals;
  hasDiscrepancies: boolean;
}

export interface BlockData {
  label: string;
  plan_type: string;
  tiers: TierTotals;
  cells: CellMapping[];
}

export interface TierTotals {
  'EE': number;
  'EE & Spouse': number;
  'EE & Children': number;
  'EE & Family': number;
  'EE & Child'?: number; // For 5-tier tabs
}

export interface CellMapping {
  tier: string;
  cell: string;
  expected: number;
  actual: number;
  match: boolean;
}

interface EnrollmentState {
  sourceData: EnrollmentRecord[];
  tabData: TabData[];
  controlTotals: TierTotals;
  uploadedFile: File | null;
  loading: boolean;
  error: string | null;
}

const initialState: EnrollmentState = {
  sourceData: [],
  tabData: [],
  controlTotals: {
    'EE': 0,
    'EE & Spouse': 0,
    'EE & Children': 0,
    'EE & Family': 0,
  },
  uploadedFile: null,
  loading: false,
  error: null,
};

const enrollmentSlice = createSlice({
  name: 'enrollment',
  initialState,
  reducers: {
    setSourceData: (state, action: PayloadAction<EnrollmentRecord[]>) => {
      state.sourceData = action.payload;
      // Calculate control totals
      const totals: TierTotals = {
        'EE': 0,
        'EE & Spouse': 0,
        'EE & Children': 0,
        'EE & Family': 0,
      };
      action.payload.forEach(record => {
        if (record.tier && record.tier in totals) {
          totals[record.tier as keyof TierTotals] += record.count;
        }
      });
      state.controlTotals = totals;
    },
    setTabData: (state, action: PayloadAction<TabData[]>) => {
      state.tabData = action.payload;
    },
    uploadFile: (state, action: PayloadAction<File>) => {
      state.uploadedFile = action.payload;
      state.loading = true;
      state.error = null;
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload;
    },
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
      state.loading = false;
    },
    clearData: (state) => {
      state.sourceData = [];
      state.tabData = [];
      state.uploadedFile = null;
      state.error = null;
    },
  },
});

export const {
  setSourceData,
  setTabData,
  uploadFile,
  setLoading,
  setError,
  clearData,
} = enrollmentSlice.actions;

export default enrollmentSlice.reducer;
