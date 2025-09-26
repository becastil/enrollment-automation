import { createSlice } from '@reduxjs/toolkit';
import type { PayloadAction } from '@reduxjs/toolkit';

export interface EnrollmentRecord {
  CLIENT_ID: string;
  PLAN: string;
  BEN_CODE: string;
  plan_type?: string;
  tier?: keyof TierTotals;
  count: number;
  [key: string]: any;
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

const BEN_CODE_TO_TIER: Record<string, keyof TierTotals> = {
  EMP: 'EE',
  ESP: 'EE & Spouse',
  ECH: 'EE & Children',
  FAM: 'EE & Family',
  E1D: 'EE & Children',
};

const TIER_LABEL_NORMALIZERS: Record<string, keyof TierTotals> = {
  'EE': 'EE',
  'EE ONLY': 'EE',
  'EE ONLY ': 'EE',
  'EE & SPOUSE': 'EE & Spouse',
  'EE+SPOUSE': 'EE & Spouse',
  'EE SPOUSE': 'EE & Spouse',
  'EE & CHILDREN': 'EE & Children',
  'EE+CHILD(REN)': 'EE & Children',
  'EE CHILDREN': 'EE & Children',
  'EE & FAMILY': 'EE & Family',
  'EE+FAMILY': 'EE & Family',
};

const NUMERIC_FIELD_FALLBACKS = ['count', 'COUNT', 'Count', 'Value', 'VALUE', 'value', 'TOTAL', 'Total', 'total'];

const VALID_TIER_KEYS = new Set<keyof TierTotals>(['EE', 'EE & Spouse', 'EE & Children', 'EE & Family']);

function normalizeTierLabel(rawTier: string | undefined, benCode: string | undefined): keyof TierTotals | undefined {
  if (rawTier) {
    const normalized = rawTier.trim().toUpperCase();
    if (normalized in TIER_LABEL_NORMALIZERS) {
      return TIER_LABEL_NORMALIZERS[normalized];
    }
    if (VALID_TIER_KEYS.has(rawTier as keyof TierTotals)) {
      return rawTier as keyof TierTotals;
    }
  }

  if (benCode) {
    const mapped = BEN_CODE_TO_TIER[benCode.trim().toUpperCase()];
    if (mapped) {
      return mapped;
    }
  }

  return undefined;
}

function parseNumeric(value: unknown): number | null {
  if (value === undefined || value === null || value === '') {
    return null;
  }

  if (typeof value === 'number') {
    return Number.isFinite(value) ? value : null;
  }

  if (typeof value === 'string') {
    const normalized = value.replace(/,/g, '').trim();
    if (normalized === '') {
      return null;
    }

    const parsed = Number(normalized);
    return Number.isFinite(parsed) ? parsed : null;
  }

  return null;
}

function normalizeCount(record: EnrollmentRecord): number {
  const direct = parseNumeric(record.count);
  if (direct !== null) {
    return direct;
  }

  for (const field of NUMERIC_FIELD_FALLBACKS) {
    if (field in record) {
      const parsed = parseNumeric((record as Record<string, unknown>)[field]);
      if (parsed !== null) {
        return parsed;
      }
    }
  }

  return 0;
}

const enrollmentSlice = createSlice({
  name: 'enrollment',
  initialState,
  reducers: {
    setSourceData: (state, action: PayloadAction<EnrollmentRecord[]>) => {
      const normalized = action.payload.map((record) => {
        const tier = normalizeTierLabel(record.tier, record.BEN_CODE);
        const count = normalizeCount(record);

        return {
          ...record,
          tier,
          count: Number.isFinite(count) ? count : 0,
        };
      });

      state.sourceData = normalized;
      // Calculate control totals
      const totals: TierTotals = {
        'EE': 0,
        'EE & Spouse': 0,
        'EE & Children': 0,
        'EE & Family': 0,
      };
      normalized.forEach(record => {
        if (record.tier && Object.prototype.hasOwnProperty.call(totals, record.tier)) {
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
