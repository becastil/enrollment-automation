import { Router, Request, Response } from 'express';
import fs from 'fs/promises';
import path from 'path';

const router = Router();

const CONFIG_DIR = path.join(__dirname, '../../config');

// Get all configuration
router.get('/', async (req: Request, res: Response) => {
  try {
    const planMappings = await loadJsonFile('plan_mappings.json');
    const blockAggregations = await loadJsonFile('block_aggregations.json');
    const tabConfigs = await loadJsonFile('tab_configs.json');
    
    res.json({
      planMappings: planMappings.mappings || {},
      blockAggregations: blockAggregations || {},
      tabConfigs: tabConfigs || []
    });
  } catch (error: any) {
    console.error('Config fetch error:', error);
    res.status(500).json({ error: error.message || 'Failed to fetch configuration' });
  }
});

// Update plan mappings
router.post('/plan-mappings', async (req: Request, res: Response) => {
  try {
    const { mappings } = req.body;
    
    await saveJsonFile('plan_mappings.json', { mappings });
    
    res.json({
      success: true,
      message: 'Plan mappings updated successfully'
    });
  } catch (error: any) {
    console.error('Plan mappings update error:', error);
    res.status(500).json({ error: error.message || 'Failed to update plan mappings' });
  }
});

// Add single plan mapping
router.post('/plan-mappings/add', async (req: Request, res: Response) => {
  try {
    const { code, type } = req.body;
    
    if (!code || !type) {
      return res.status(400).json({ error: 'Code and type are required' });
    }
    
    const current = await loadJsonFile('plan_mappings.json');
    current.mappings = current.mappings || {};
    current.mappings[code] = type;
    
    await saveJsonFile('plan_mappings.json', current);
    
    res.json({
      success: true,
      message: `Mapping added: ${code} -> ${type}`
    });
  } catch (error: any) {
    console.error('Add mapping error:', error);
    res.status(500).json({ error: error.message || 'Failed to add mapping' });
  }
});

// Remove plan mapping
router.delete('/plan-mappings/:code', async (req: Request, res: Response) => {
  try {
    const { code } = req.params;
    
    const current = await loadJsonFile('plan_mappings.json');
    if (current.mappings && current.mappings[code]) {
      delete current.mappings[code];
      await saveJsonFile('plan_mappings.json', current);
    }
    
    res.json({
      success: true,
      message: `Mapping removed: ${code}`
    });
  } catch (error: any) {
    console.error('Remove mapping error:', error);
    res.status(500).json({ error: error.message || 'Failed to remove mapping' });
  }
});

// Export configuration
router.get('/export', async (req: Request, res: Response) => {
  try {
    const config = {
      planMappings: await loadJsonFile('plan_mappings.json'),
      blockAggregations: await loadJsonFile('block_aggregations.json'),
      tabConfigs: await loadJsonFile('tab_configs.json')
    };
    
    res.setHeader('Content-Type', 'application/json');
    res.setHeader('Content-Disposition', 'attachment; filename="enrollment-config.json"');
    res.json(config);
  } catch (error: any) {
    console.error('Config export error:', error);
    res.status(500).json({ error: error.message || 'Failed to export configuration' });
  }
});

// Import configuration
router.post('/import', async (req: Request, res: Response) => {
  try {
    const { planMappings, blockAggregations, tabConfigs } = req.body;
    
    if (planMappings) {
      await saveJsonFile('plan_mappings.json', planMappings);
    }
    if (blockAggregations) {
      await saveJsonFile('block_aggregations.json', blockAggregations);
    }
    if (tabConfigs) {
      await saveJsonFile('tab_configs.json', tabConfigs);
    }
    
    res.json({
      success: true,
      message: 'Configuration imported successfully'
    });
  } catch (error: any) {
    console.error('Config import error:', error);
    res.status(500).json({ error: error.message || 'Failed to import configuration' });
  }
});

// Helper functions
async function loadJsonFile(filename: string): Promise<any> {
  try {
    const filePath = path.join(CONFIG_DIR, filename);
    const data = await fs.readFile(filePath, 'utf-8');
    return JSON.parse(data);
  } catch (error) {
    // Return empty object if file doesn't exist
    return {};
  }
}

async function saveJsonFile(filename: string, data: any): Promise<void> {
  try {
    // Ensure config directory exists
    await fs.mkdir(CONFIG_DIR, { recursive: true });
    
    const filePath = path.join(CONFIG_DIR, filename);
    await fs.writeFile(filePath, JSON.stringify(data, null, 2));
  } catch (error) {
    throw new Error(`Failed to save ${filename}: ${error}`);
  }
}

export default router;