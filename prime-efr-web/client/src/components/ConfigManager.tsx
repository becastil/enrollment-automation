import { useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import type { RootState, AppDispatch } from '../store';
import { addPlanMapping, removePlanMapping } from '../store/slices/configSlice';
import { Plus, Trash2, Download, Upload } from 'lucide-react';

export default function ConfigManager() {
  const dispatch = useDispatch<AppDispatch>();
  const { planMappings, allowedTabs, excludedClientIds } = useSelector(
    (state: RootState) => state.config
  );
  
  const [newPlanCode, setNewPlanCode] = useState('');
  const [newPlanType, setNewPlanType] = useState('EPO');
  const [activeTab, setActiveTab] = useState<'mappings' | 'tabs' | 'exclusions'>('mappings');

  const handleAddMapping = () => {
    if (newPlanCode && newPlanType) {
      dispatch(addPlanMapping({ code: newPlanCode, type: newPlanType }));
      setNewPlanCode('');
    }
  };

  const handleExportConfig = () => {
    const config = {
      planMappings,
      allowedTabs,
      excludedClientIds,
    };
    const blob = new Blob([JSON.stringify(config, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'enrollment-config.json';
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleImportConfig = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;
    
    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const config = JSON.parse(e.target?.result as string);
        // Dispatch actions to update config
        console.log('Imported config:', config);
      } catch (error) {
        console.error('Failed to parse config file:', error);
      }
    };
    reader.readAsText(file);
  };

  return (
    <div className="space-y-lg">
      <div className="card">
        <div className="flex items-center justify-between mb-lg">
          <h2 className="text-xl font-semibold">Configuration Management</h2>
          <div className="flex space-x-xs">
            <label className="btn-secondary flex items-center cursor-pointer">
              <Upload className="h-4 w-4 mr-xs" />
              Import
              <input
                type="file"
                accept=".json"
                onChange={handleImportConfig}
                className="hidden"
              />
            </label>
            <button onClick={handleExportConfig} className="btn-secondary flex items-center">
              <Download className="h-4 w-4 mr-xs" />
              Export
            </button>
          </div>
        </div>

        <div className="border-b border-border mb-lg">
          <nav className="-mb-px flex space-x-xl">
            <button
              onClick={() => setActiveTab('mappings')}
              className={`py-sm px-2xs border-b-2 font-medium text-sm ${
                activeTab === 'mappings'
                  ? 'border-primary text-primary'
                  : 'border-transparent text-text-muted hover:text-text hover:border-border'
              }`}
            >
              Plan Mappings
            </button>
            <button
              onClick={() => setActiveTab('tabs')}
              className={`py-sm px-2xs border-b-2 font-medium text-sm ${
                activeTab === 'tabs'
                  ? 'border-primary text-primary'
                  : 'border-transparent text-text-muted hover:text-text hover:border-border'
              }`}
            >
              Allowed Tabs
            </button>
            <button
              onClick={() => setActiveTab('exclusions')}
              className={`py-sm px-2xs border-b-2 font-medium text-sm ${
                activeTab === 'exclusions'
                  ? 'border-primary text-primary'
                  : 'border-transparent text-text-muted hover:text-text hover:border-border'
              }`}
            >
              Exclusions
            </button>
          </nav>
        </div>

        {activeTab === 'mappings' && (
          <div>
            <div className="mb-md">
              <h3 className="text-lg font-medium mb-sm">Plan Code to Type Mappings</h3>
              <p className="text-sm text-text-muted">
                Map plan codes to their corresponding plan types (EPO, VALUE, PPO)
              </p>
            </div>

            <div className="flex space-x-xs mb-md">
              <input
                type="text"
                value={newPlanCode}
                onChange={(e) => setNewPlanCode(e.target.value.toUpperCase())}
                placeholder="Plan Code (e.g., PRIMEMMEPO)"
                className="input-field flex-1"
              />
              <select
                value={newPlanType}
                onChange={(e) => setNewPlanType(e.target.value)}
                className="input-field"
              >
                <option value="EPO">EPO</option>
                <option value="VALUE">VALUE</option>
                <option value="PPO">PPO</option>
              </select>
              <button
                onClick={handleAddMapping}
                className="btn-primary flex items-center"
              >
                <Plus className="h-4 w-4 mr-2xs" />
                Add
              </button>
            </div>

            <div className="space-y-xs max-h-96 overflow-y-auto">
              {Object.entries(planMappings).map(([code, type]) => (
                <div
                  key={code}
                  className="flex items-center justify-between p-sm bg-surface-subtle rounded-lg"
                >
                  <div className="flex items-center space-x-md">
                    <span className="font-mono text-sm font-medium">{code}</span>
                    <span className="text-text-muted">→</span>
                    <span className={`px-xs py-2xs rounded text-xs font-medium ${
                      type === 'EPO'
                        ? 'bg-primary-soft text-primary'
                        : type === 'VALUE'
                          ? 'bg-success-soft text-success'
                          : 'bg-warning-soft text-warning'
                    }`}>
                      {type}
                    </span>
                  </div>
                  <button
                    onClick={() => dispatch(removePlanMapping(code))}
                    className="p-2xs hover:bg-surface-subtle rounded transition-colors"
                  >
                    <Trash2 className="h-4 w-4 text-text-muted" />
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'tabs' && (
          <div>
            <div className="mb-md">
              <h3 className="text-lg font-medium mb-sm">Allowed Tabs</h3>
              <p className="text-sm text-text-muted">
                Only these tabs will be processed during validation
              </p>
            </div>

            <div className="grid grid-cols-2 gap-xs">
              {allowedTabs.map((tab) => (
                <div
                  key={tab}
                  className="p-xs bg-success-soft border border-success rounded text-sm"
                >
                  {tab}
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'exclusions' && (
          <div>
            <div className="mb-md">
              <h3 className="text-lg font-medium mb-sm">Excluded Client IDs</h3>
              <p className="text-sm text-text-muted">
                These client IDs will be excluded from processing
              </p>
            </div>

            <div className="space-y-xs">
              {excludedClientIds.map((clientId) => (
                <div
                  key={clientId}
                  className="p-xs bg-danger-soft border border-danger rounded text-sm font-mono"
                >
                  {clientId}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
