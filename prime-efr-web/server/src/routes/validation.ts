import { Router, Request, Response } from 'express';
import { runValidation } from '../services/validationService';

const router = Router();

// Run validation on enrollment data
router.post('/validate', async (req: Request, res: Response) => {
  try {
    const { sourceData, tabData, config } = req.body;
    
    const validationResult = await runValidation(sourceData, tabData, config);
    
    res.json({
      success: true,
      issues: validationResult.issues,
      summary: validationResult.summary
    });
  } catch (error: any) {
    console.error('Validation error:', error);
    res.status(500).json({ error: error.message || 'Validation failed' });
  }
});

// Get validation rules
router.get('/rules', async (req: Request, res: Response) => {
  try {
    const rules = {
      tierMappings: {
        'EMP': 'EE',
        'ESP': 'EE & Spouse',
        'ECH': 'EE & Children',
        'FAM': 'EE & Family'
      },
      controlTotals: {
        'EE': 14533,
        'EE & Spouse': 2639,
        'EE & Children': 4413,
        'EE & Family': 3123
      },
      allowedTabs: [
        'Centinela', 'Coshocton', 'Dallas Medical Center', 'Dallas Regional',
        'East Liverpool', 'Encino-Garden Grove', 'Garden City', 'Harlingen',
        'Illinois', 'Knapp', 'Lake Huron', 'Landmark', 'Legacy', 'Lower Bucks',
        'Mission', 'Monroe', 'North Vista', 'Pampa', 'Providence & St John',
        'Riverview & Gadsden', 'Roxborough', "Saint Clare's", "Saint Mary's Passaic",
        "Saint Mary's Reno", 'Southern Regional', "St Joe & St Mary's",
        "St Michael's", 'St. Francis', 'Suburban'
      ]
    };
    
    res.json(rules);
  } catch (error: any) {
    console.error('Rules fetch error:', error);
    res.status(500).json({ error: error.message || 'Failed to fetch validation rules' });
  }
});

// Apply suggested fix
router.post('/apply-fix', async (req: Request, res: Response) => {
  try {
    const { issueId, fix } = req.body;
    
    // Apply the fix (this would update the data in production)
    const result = {
      success: true,
      issueId,
      fixApplied: fix,
      timestamp: new Date().toISOString()
    };
    
    res.json(result);
  } catch (error: any) {
    console.error('Fix application error:', error);
    res.status(500).json({ error: error.message || 'Failed to apply fix' });
  }
});

export default router;