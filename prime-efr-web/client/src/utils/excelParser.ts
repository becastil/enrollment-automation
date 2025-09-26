import * as XLSX from 'xlsx';

export async function parseExcelFile(file: File): Promise<any[]> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    
    reader.onload = (e) => {
      try {
        const data = e.target?.result;
        const workbook = XLSX.read(data, { type: 'binary' });
        
        // Get the first sheet (Sheet1)
        const sheetName = workbook.SheetNames[0];
        const worksheet = workbook.Sheets[sheetName];
        
        // Convert to JSON
        const jsonData = XLSX.utils.sheet_to_json(worksheet, {
          header: 1,
          defval: '',
        });
        
        if (jsonData.length === 0) {
          throw new Error('No data found in the Excel file');
        }
        
        // Convert array of arrays to array of objects
        const headers = jsonData[0] as string[];
        const rows = jsonData.slice(1) as any[][];
        
        const parsedData = rows.map(row => {
          const obj: any = {};
          headers.forEach((header, index) => {
            obj[header] = row[index];
          });
          return obj;
        });
        
        resolve(parsedData);
      } catch (error) {
        reject(error);
      }
    };
    
    reader.onerror = () => {
      reject(new Error('Failed to read file'));
    };
    
    reader.readAsBinaryString(file);
  });
}

export function normalizeClientId(clientId: string): string {
  // Normalize client ID format (e.g., H3170 -> H3170)
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