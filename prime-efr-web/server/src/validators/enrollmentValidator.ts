interface ValidationResult {
  isValid: boolean;
  issues: string[];
}

export function validateEnrollmentData(data: any[]): ValidationResult {
  const issues: string[] = [];
  
  if (!Array.isArray(data)) {
    issues.push('Data must be an array');
    return { isValid: false, issues };
  }
  
  if (data.length === 0) {
    issues.push('Data array is empty');
    return { isValid: false, issues };
  }
  
  // Check required fields
  const requiredFields = ['CLIENT_ID', 'PLAN', 'BEN_CODE'];
  const missingFields = new Set<string>();
  
  data.forEach((record, index) => {
    requiredFields.forEach(field => {
      if (!record[field]) {
        missingFields.add(field);
      }
    });
  });
  
  if (missingFields.size > 0) {
    issues.push(`Missing required fields: ${Array.from(missingFields).join(', ')}`);
  }
  
  // Validate BEN_CODE values
  const validBenCodes = ['EMP', 'ESP', 'ECH', 'FAM'];
  const invalidBenCodes = new Set<string>();
  
  data.forEach(record => {
    if (record.BEN_CODE && !validBenCodes.includes(record.BEN_CODE)) {
      invalidBenCodes.add(record.BEN_CODE);
    }
  });
  
  if (invalidBenCodes.size > 0) {
    issues.push(`Invalid BEN_CODE values: ${Array.from(invalidBenCodes).join(', ')}`);
  }
  
  // Validate CLIENT_ID format (should start with H and be followed by numbers)
  const invalidClientIds = new Set<string>();
  
  data.forEach(record => {
    if (record.CLIENT_ID && !/^H\d+$/.test(record.CLIENT_ID)) {
      invalidClientIds.add(record.CLIENT_ID);
    }
  });
  
  if (invalidClientIds.size > 0 && invalidClientIds.size <= 5) {
    issues.push(`Invalid CLIENT_ID format: ${Array.from(invalidClientIds).join(', ')}`);
  } else if (invalidClientIds.size > 5) {
    issues.push(`${invalidClientIds.size} CLIENT_IDs have invalid format`);
  }
  
  return {
    isValid: issues.length === 0,
    issues
  };
}

export function validatePlanMapping(planCode: string, planType: string): boolean {
  const validPlanTypes = ['EPO', 'VALUE', 'PPO'];
  return validPlanTypes.includes(planType);
}

export function validateTabName(tabName: string, allowedTabs: string[]): boolean {
  return allowedTabs.includes(tabName);
}