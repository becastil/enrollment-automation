import { Router, Request, Response } from 'express';
import { processEnrollmentData } from '../services/enrollmentProcessor';
import { validateEnrollmentData } from '../validators/enrollmentValidator';

const router = Router();

// Process enrollment data
router.post('/process', async (req: Request, res: Response) => {
  try {
    const { data, config } = req.body;
    
    // Validate input data
    const validation = validateEnrollmentData(data);
    if (!validation.isValid) {
      return res.status(400).json({ 
        error: 'Invalid enrollment data',
        issues: validation.issues 
      });
    }
    
    // Process the enrollment data
    const result = await processEnrollmentData(data, config);
    
    res.json({
      success: true,
      summary: result.summary,
      tabData: result.tabData,
      controlTotals: result.controlTotals
    });
  } catch (error: any) {
    console.error('Enrollment processing error:', error);
    res.status(500).json({ error: error.message || 'Failed to process enrollment data' });
  }
});

// Get enrollment summary
router.get('/summary', async (req: Request, res: Response) => {
  try {
    // This would fetch from database in production
    const summary = {
      totalEnrollment: 24708,
      byTier: {
        'EE': 14533,
        'EE & Spouse': 2639,
        'EE & Children': 4413,
        'EE & Family': 3123
      },
      byPlanType: {
        'EPO': 20000,
        'VALUE': 4000,
        'PPO': 708
      }
    };
    
    res.json(summary);
  } catch (error: any) {
    console.error('Summary fetch error:', error);
    res.status(500).json({ error: error.message || 'Failed to fetch summary' });
  }
});

// Export enrollment data
router.post('/export', async (req: Request, res: Response) => {
  try {
    const { format, tabData } = req.body;
    
    // Generate export based on format
    let exportData;
    if (format === 'csv') {
      // Generate CSV
      exportData = 'CSV data here';
    } else if (format === 'excel') {
      // Generate Excel
      exportData = 'Excel data here';
    } else {
      return res.status(400).json({ error: 'Invalid export format' });
    }
    
    res.json({
      success: true,
      data: exportData,
      format
    });
  } catch (error: any) {
    console.error('Export error:', error);
    res.status(500).json({ error: error.message || 'Failed to export data' });
  }
});

export default router;