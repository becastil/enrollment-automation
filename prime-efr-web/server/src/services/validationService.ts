interface ValidationIssue {
  id: string;
  type: 'error' | 'warning' | 'info';
  category: string;
  tab?: string;
  client_id?: string;
  plan?: string;
  message: string;
  details?: any;
  suggestedFix?: string;
}

interface ValidationResult {
  issues: ValidationIssue[];
  summary: {
    totalIssues: number;
    errors: number;
    warnings: number;
    info: number;
    byCategory: Record<string, number>;
    byTab: Record<string, number>;
  };
}

export async function runValidation(
  sourceData: any[],
  tabData: any[],
  config: any
): Promise<ValidationResult> {
  const issues: ValidationIssue[] = [];
  let issueIdCounter = 1;
  
  // Check for missing plan mappings
  const unmappedPlans = new Set<string>();
  sourceData.forEach(record => {
    if (!config.planMappings[record.PLAN]) {
      unmappedPlans.add(record.PLAN);
    }
  });
  
  unmappedPlans.forEach(plan => {
    issues.push({
      id: `issue-${issueIdCounter++}`,
      type: 'error',
      category: 'missing_mapping',
      plan,
      message: `Plan code "${plan}" has no mapping`,
      suggestedFix: `Add mapping for plan code "${plan}" to EPO, VALUE, or PPO`
    });
  });
  
  // Check control totals
  const expectedTotals = {
    'EE': 14533,
    'EE & Spouse': 2639,
    'EE & Children': 4413,
    'EE & Family': 3123
  };
  
  const actualTotals: Record<string, number> = {
    'EE': 0,
    'EE & Spouse': 0,
    'EE & Children': 0,
    'EE & Family': 0
  };
  
  tabData.forEach(tab => {
    Object.entries(tab.totals || {}).forEach(([tier, count]) => {
      actualTotals[tier] = (actualTotals[tier] || 0) + (count as number);
    });
  });
  
  Object.entries(expectedTotals).forEach(([tier, expected]) => {
    const actual = actualTotals[tier] || 0;
    if (actual !== expected) {
      issues.push({
        id: `issue-${issueIdCounter++}`,
        type: 'error',
        category: 'total_mismatch',
        message: `${tier} total mismatch: expected ${expected}, got ${actual}`,
        details: { tier, expected, actual, difference: actual - expected }
      });
    }
  });
  
  // Check for unassigned facilities
  const unassignedClients = new Set<string>();
  sourceData.forEach(record => {
    const hasTab = tabData.some(tab => 
      tab.client_ids && tab.client_ids.includes(record.CLIENT_ID)
    );
    if (!hasTab && !config.excludedClientIds.includes(record.CLIENT_ID)) {
      unassignedClients.add(record.CLIENT_ID);
    }
  });
  
  unassignedClients.forEach(clientId => {
    issues.push({
      id: `issue-${issueIdCounter++}`,
      type: 'warning',
      category: 'unassigned_plan',
      client_id: clientId,
      message: `Client ID "${clientId}" is not assigned to any tab`,
      suggestedFix: `Map client ID "${clientId}" to an appropriate tab`
    });
  });
  
  // Check for multi-block aggregation issues
  tabData.forEach(tab => {
    if (tab.blocks && tab.blocks.length > 1) {
      const planTypes = new Set(tab.blocks.map((b: any) => b.plan_type));
      if (planTypes.size > 1) {
        issues.push({
          id: `issue-${issueIdCounter++}`,
          type: 'info',
          category: 'multi_block',
          tab: tab.name,
          message: `Tab "${tab.name}" has multiple block types`,
          details: { blockCount: tab.blocks.length, planTypes: Array.from(planTypes) }
        });
      }
    }
  });
  
  // Calculate summary
  const summary = {
    totalIssues: issues.length,
    errors: issues.filter(i => i.type === 'error').length,
    warnings: issues.filter(i => i.type === 'warning').length,
    info: issues.filter(i => i.type === 'info').length,
    byCategory: {} as Record<string, number>,
    byTab: {} as Record<string, number>
  };
  
  issues.forEach(issue => {
    summary.byCategory[issue.category] = (summary.byCategory[issue.category] || 0) + 1;
    if (issue.tab) {
      summary.byTab[issue.tab] = (summary.byTab[issue.tab] || 0) + 1;
    }
  });
  
  return { issues, summary };
}