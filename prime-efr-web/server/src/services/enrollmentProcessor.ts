import { normalizeClientId, normalizeTier, getPlanType } from '../utils/dataUtils';

interface EnrollmentData {
  CLIENT_ID: string;
  PLAN: string;
  BEN_CODE: string;
  count?: number;
  [key: string]: any;
}

interface ProcessConfig {
  planMappings: Record<string, string>;
  allowedTabs: string[];
  excludedClientIds: string[];
}

interface ProcessResult {
  summary: {
    totalRecords: number;
    processedRecords: number;
    skippedRecords: number;
  };
  tabData: any[];
  controlTotals: Record<string, number>;
}

const numericFieldCandidates = [
  'count',
  'COUNT',
  'Count',
  'VALUE',
  'Value',
  'value',
  'TOTAL',
  'Total',
  'total'
];

function createEmptyTotals(): Record<string, number> {
  return {
    'EE': 0,
    'EE & Spouse': 0,
    'EE & Children': 0,
    'EE & Family': 0
  };
}

function parseCountValue(value: unknown): number | null {
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

function getRecordCount(record: EnrollmentData): number | null {
  if ('count' in record) {
    const parsed = parseCountValue(record.count);
    if (parsed !== null) {
      return parsed;
    }
  }

  for (const field of numericFieldCandidates) {
    if (field in record) {
      const parsed = parseCountValue(record[field]);
      if (parsed !== null) {
        return parsed;
      }
    }
  }

  return null;
}

export async function processEnrollmentData(
  data: EnrollmentData[],
  config: ProcessConfig
): Promise<ProcessResult> {
  const controlTotals = createEmptyTotals();
  
  const tabDataMap = new Map<string, any>();
  let processedCount = 0;
  let skippedCount = 0;
  
  // Process each enrollment record
  for (const record of data) {
    // Skip excluded client IDs
    if (config.excludedClientIds.includes(record.CLIENT_ID)) {
      skippedCount++;
      continue;
    }
    
    // Normalize data
    const clientId = normalizeClientId(record.CLIENT_ID);
    const tier = normalizeTier(record.BEN_CODE);
    const planType = getPlanType(record.PLAN, config.planMappings);
    const count = getRecordCount(record);
    const units = count !== null ? count : 1;

    // Skip unknown plan types
    if (planType === 'UNKNOWN') {
      skippedCount++;
      continue;
    }

    // Update control totals
    if (tier in controlTotals) {
      controlTotals[tier] += units;
    }

    // Map to tab (this would use CID_TO_TAB mapping in production)
    const tab = getTabForClientId(clientId);
    if (!tab || !config.allowedTabs.includes(tab)) {
      skippedCount++;
      continue;
    }

    // Update tab data
    if (!tabDataMap.has(tab)) {
      tabDataMap.set(tab, {
        name: tab,
        client_ids: [],
        blocks: [],
        totals: createEmptyTotals(),
        hasDiscrepancies: false
      });
    }

    const tabData = tabDataMap.get(tab);
    if (!tabData.client_ids.includes(clientId)) {
      tabData.client_ids.push(clientId);
    }

    if (tier in tabData.totals) {
      tabData.totals[tier] += units;
    }

    processedCount += units;
  }
  
  return {
    summary: {
      totalRecords: data.length,
      processedRecords: processedCount,
      skippedRecords: skippedCount
    },
    tabData: Array.from(tabDataMap.values()),
    controlTotals
  };
}

function getTabForClientId(clientId: string): string | null {
  // This is a simplified mapping - in production, use the full CID_TO_TAB mapping
  const cidToTabMap: Record<string, string> = {
    'H3170': 'Legacy',
    'H3130': 'Legacy',
    'H3100': 'Legacy',
    'H3270': 'Centinela',
    'H3250': 'Encino-Garden Grove',
    'H3260': 'Encino-Garden Grove',
    // Add more mappings...
  };
  
  return cidToTabMap[clientId] || null;
}
