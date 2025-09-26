import { Router, Request, Response } from 'express';
import multer from 'multer';
import * as XLSX from 'xlsx';
import path from 'path';
import fs from 'fs';

const router = Router();

// Configure multer for file uploads
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    const uploadDir = path.join(__dirname, '../../uploads');
    if (!fs.existsSync(uploadDir)) {
      fs.mkdirSync(uploadDir, { recursive: true });
    }
    cb(null, uploadDir);
  },
  filename: (req, file, cb) => {
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
    cb(null, file.fieldname + '-' + uniqueSuffix + path.extname(file.originalname));
  }
});

const upload = multer({
  storage,
  fileFilter: (req, file, cb) => {
    const allowedTypes = ['.xlsx', '.xls', '.csv'];
    const ext = path.extname(file.originalname).toLowerCase();
    if (allowedTypes.includes(ext)) {
      cb(null, true);
    } else {
      cb(new Error('Invalid file type. Only Excel and CSV files are allowed.'));
    }
  },
  limits: {
    fileSize: 10 * 1024 * 1024 // 10MB limit
  }
});

const numberFieldCandidates = [
  'COUNT',
  'Count',
  'count',
  'VALUE',
  'Value',
  'value',
  'TOTAL',
  'Total',
  'total'
];

function parseNumeric(value: any): number | null {
  if (value === undefined || value === null || value === '') {
    return null;
  }

  if (typeof value === 'number') {
    return Number.isFinite(value) ? value : null;
  }

  const normalized = String(value).replace(/,/g, '').trim();
  if (normalized === '') {
    return null;
  }

  const parsed = Number(normalized);
  return Number.isFinite(parsed) ? parsed : null;
}

function extractCount(row: Record<string, unknown>): number | null {
  for (const field of numberFieldCandidates) {
    if (field in row) {
      const parsed = parseNumeric(row[field]);
      if (parsed !== null) {
        return parsed;
      }
    }
  }

  return null;
}

// Parse Excel file endpoint
router.post('/parse', upload.single('file'), async (req: Request, res: Response) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'No file uploaded' });
    }

    const filePath = req.file.path;
    const workbook = XLSX.readFile(filePath);
    const sheetName = workbook.SheetNames[0];
    const worksheet = workbook.Sheets[sheetName];
    
    // Convert to JSON
    const data = XLSX.utils.sheet_to_json(worksheet);
    
    // Clean up uploaded file
    fs.unlinkSync(filePath);
    
    // Process data
    const processedData = data.map((row: any) => {
      const clientId = row['CLIENT_ID'] || row['Client ID'] || row['client_id'];
      const plan = row['PLAN'] || row['Plan'] || row['plan'];
      const benCode = row['BEN CODE'] || row['Ben Code'] || row['BEN_CODE'] || row['ben_code'];
      const count = extractCount(row);

      return {
        CLIENT_ID: clientId,
        PLAN: plan,
        BEN_CODE: benCode,
        count,
      };
    });
    
    res.json({
      success: true,
      rowCount: processedData.length,
      data: processedData,
      preview: processedData.slice(0, 10) // Send first 10 rows as preview
    });
  } catch (error: any) {
    console.error('File parsing error:', error);
    res.status(500).json({ error: error.message || 'Failed to parse file' });
  }
});

// Validate Excel structure
router.post('/validate-structure', upload.single('file'), async (req: Request, res: Response) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'No file uploaded' });
    }

    const filePath = req.file.path;
    const workbook = XLSX.readFile(filePath);
    
    const structure = {
      sheets: workbook.SheetNames,
      sheetDetails: {} as any
    };
    
    workbook.SheetNames.forEach(sheetName => {
      const worksheet = workbook.Sheets[sheetName];
      const range = XLSX.utils.decode_range(worksheet['!ref'] || 'A1');
      const headers: string[] = [];
      
      // Get headers from first row
      for (let col = range.s.c; col <= range.e.c; col++) {
        const cellAddress = XLSX.utils.encode_cell({ r: 0, c: col });
        const cell = worksheet[cellAddress];
        if (cell && cell.v) {
          headers.push(cell.v.toString());
        }
      }
      
      structure.sheetDetails[sheetName] = {
        rowCount: range.e.r + 1,
        columnCount: range.e.c + 1,
        headers
      };
    });
    
    // Clean up uploaded file
    fs.unlinkSync(filePath);
    
    res.json({
      success: true,
      structure
    });
  } catch (error: any) {
    console.error('Structure validation error:', error);
    res.status(500).json({ error: error.message || 'Failed to validate file structure' });
  }
});

export default router;
