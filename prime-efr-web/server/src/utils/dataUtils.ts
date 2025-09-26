export function normalizeClientId(clientId: string): string {
  return clientId.trim().toUpperCase();
}

export function normalizeTier(benCode: string): string {
  const tierMap: Record<string, string> = {
    'EMP': 'EE',
    'ESP': 'EE & Spouse',
    'ECH': 'EE & Children',
    'FAM': 'EE & Family',
  };
  
  return tierMap[benCode] || benCode;
}

export function getPlanType(planCode: string, planMappings: Record<string, string>): string {
  // First check direct mapping
  if (planMappings[planCode]) {
    return planMappings[planCode];
  }
  
  // Apply default rules
  if (planCode.includes('VAL') || planCode.includes('VALUE')) {
    return 'VALUE';
  }
  if (planCode.includes('EPO')) {
    return 'EPO';
  }
  if (planCode.includes('PPO')) {
    return 'PPO';
  }
  
  return 'UNKNOWN';
}

export function calculateTierTotals(data: any[]): Record<string, number> {
  const totals: Record<string, number> = {
    'EE': 0,
    'EE & Spouse': 0,
    'EE & Children': 0,
    'EE & Family': 0
  };
  
  data.forEach(record => {
    const tier = normalizeTier(record.BEN_CODE);
    if (tier in totals) {
      totals[tier]++;
    }
  });
  
  return totals;
}

export function splitChildTier(data: any[], is5Tier: boolean): any[] {
  if (!is5Tier) return data;
  
  return data.map(record => {
    if (record.tier === 'EE & Children') {
      // In a real implementation, check dependent count
      // For now, default to 'EE & Children'
      const childCount = record.dependentCount || 2;
      return {
        ...record,
        tier: childCount === 1 ? 'EE & Child' : 'EE & Children'
      };
    }
    return record;
  });
}