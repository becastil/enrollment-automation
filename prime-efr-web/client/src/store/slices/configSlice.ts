import { createSlice } from '@reduxjs/toolkit';
import type { PayloadAction } from '@reduxjs/toolkit';

export interface PlanMapping {
  [planCode: string]: string; // plan code -> plan type (EPO, VALUE, PPO)
}

export interface BlockAggregation {
  client_id: string;
  blocks: {
    [blockLabel: string]: {
      plan_type: string;
      sum_of: string[];
    };
  };
}

export interface TabConfig {
  name: string;
  client_ids: string[];
  is_5tier?: boolean;
  blocks: BlockAggregation[];
}

interface ConfigState {
  planMappings: PlanMapping;
  tabConfigs: TabConfig[];
  allowedTabs: string[];
  excludedClientIds: string[];
  loading: boolean;
  error: string | null;
}

const initialState: ConfigState = {
  planMappings: {},
  tabConfigs: [],
  allowedTabs: [
    "Centinela", "Coshocton", "Dallas Medical Center", "Dallas Regional",
    "East Liverpool", "Encino-Garden Grove", "Garden City", "Harlingen",
    "Illinois", "Knapp", "Lake Huron", "Landmark", "Legacy", "Lower Bucks",
    "Mission", "Monroe", "North Vista", "Pampa", "Providence & St John",
    "Riverview & Gadsden", "Roxborough", "Saint Clare's", "Saint Mary's Passaic",
    "Saint Mary's Reno", "Southern Regional", "St Joe & St Mary's",
    "St Michael's", "St. Francis", "Suburban"
  ],
  excludedClientIds: ["H3310"], // Alvarado
  loading: false,
  error: null,
};

const configSlice = createSlice({
  name: 'config',
  initialState,
  reducers: {
    setPlanMappings: (state, action: PayloadAction<PlanMapping>) => {
      state.planMappings = action.payload;
    },
    addPlanMapping: (state, action: PayloadAction<{ code: string; type: string }>) => {
      state.planMappings[action.payload.code] = action.payload.type;
    },
    removePlanMapping: (state, action: PayloadAction<string>) => {
      delete state.planMappings[action.payload];
    },
    setTabConfigs: (state, action: PayloadAction<TabConfig[]>) => {
      state.tabConfigs = action.payload;
    },
    updateTabConfig: (state, action: PayloadAction<TabConfig>) => {
      const index = state.tabConfigs.findIndex(tab => tab.name === action.payload.name);
      if (index >= 0) {
        state.tabConfigs[index] = action.payload;
      } else {
        state.tabConfigs.push(action.payload);
      }
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload;
    },
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
    },
  },
});

export const {
  setPlanMappings,
  addPlanMapping,
  removePlanMapping,
  setTabConfigs,
  updateTabConfig,
  setLoading,
  setError,
} = configSlice.actions;

export default configSlice.reducer;
