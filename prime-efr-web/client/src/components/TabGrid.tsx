import { useState } from 'react';
import { useSelector } from 'react-redux';
import type { RootState } from '../store';
import { ChevronDown, ChevronRight, CheckCircle, XCircle } from 'lucide-react';

export default function TabGrid() {
  const { tabData } = useSelector((state: RootState) => state.enrollment);
  const [expandedTab, setExpandedTab] = useState<string | null>(null);

  const toggleTab = (tabName: string) => {
    setExpandedTab(expandedTab === tabName ? null : tabName);
  };

  const getCellColor = (match: boolean | undefined) => {
    if (match === undefined) return 'bg-surface-subtle text-text-muted';
    return match ? 'bg-success-soft text-success' : 'bg-danger-soft text-danger';
  };

  if (tabData.length === 0) {
    return (
      <div className="card">
        <div className="text-center py-2xl">
          <p className="text-text-muted">No tab data available. Please upload a source file.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="card">
      <h2 className="text-xl font-semibold mb-md">Tab Validation Grid</h2>
      
      <div className="space-y-md">
        {tabData.map((tab) => (
          <div key={tab.name} className="border border-border rounded-lg overflow-hidden">
            <button
              onClick={() => toggleTab(tab.name)}
              className="w-full px-md py-sm bg-surface-subtle hover:bg-surface transition-colors flex items-center justify-between"
            >
              <div className="flex items-center space-x-sm">
                {expandedTab === tab.name ? (
                  <ChevronDown className="h-5 w-5 text-text-muted" />
                ) : (
                  <ChevronRight className="h-5 w-5 text-text-muted" />
                )}
                <span className="font-medium">{tab.name}</span>
                <span className="text-sm text-text-muted">
                  ({tab.client_ids.join(', ')})
                </span>
              </div>
              
              <div className="flex items-center space-x-xs">
                {tab.hasDiscrepancies ? (
                  <span className="flex items-center text-danger">
                    <XCircle className="h-4 w-4 mr-2xs" />
                    Has Issues
                  </span>
                ) : (
                  <span className="flex items-center text-success">
                    <CheckCircle className="h-4 w-4 mr-2xs" />
                    Valid
                  </span>
                )}
              </div>
            </button>
            
            {expandedTab === tab.name && (
              <div className="p-md bg-surface">
                <div className="space-y-md">
                  {tab.blocks.map((block, blockIndex) => (
                    <div key={blockIndex} className="border border-border rounded-lg p-sm">
                      <div className="flex items-center justify-between mb-sm">
                        <h4 className="font-medium text-sm">
                          {block.label} ({block.plan_type})
                        </h4>
                      </div>
                      
                      <div className="overflow-x-auto">
                        <table className="min-w-full divide-y divide-border">
                          <thead className="bg-surface-subtle">
                            <tr>
                              <th className="px-sm py-xs text-left text-xs font-medium text-text-muted uppercase">
                                Tier
                              </th>
                              <th className="px-sm py-xs text-left text-xs font-medium text-text-muted uppercase">
                                Cell
                              </th>
                              <th className="px-sm py-xs text-right text-xs font-medium text-text-muted uppercase">
                                Expected
                              </th>
                              <th className="px-sm py-xs text-right text-xs font-medium text-text-muted uppercase">
                                Actual
                              </th>
                              <th className="px-sm py-xs text-center text-xs font-medium text-text-muted uppercase">
                                Status
                              </th>
                            </tr>
                          </thead>
                          <tbody className="bg-surface divide-y divide-border">
                            {block.cells.map((cell, cellIndex) => (
                              <tr key={cellIndex}>
                                <td className="px-sm py-xs text-sm text-text">
                                  {cell.tier}
                                </td>
                                <td className="px-sm py-xs text-sm font-mono text-text-muted">
                                  {cell.cell}
                                </td>
                                <td className="px-sm py-xs text-sm text-right">
                                  {cell.expected}
                                </td>
                                <td className={`px-sm py-xs text-sm text-right ${getCellColor(cell.match)}`}>
                                  {cell.actual}
                                </td>
                                <td className="px-sm py-xs text-center">
                                  {cell.match ? (
                                    <CheckCircle className="h-4 w-4 text-success inline" />
                                  ) : (
                                    <XCircle className="h-4 w-4 text-danger inline" />
                                  )}
                                </td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                      
                      <div className="mt-sm pt-sm border-t border-border">
                        <div className="grid grid-cols-4 gap-xs text-sm">
                          {Object.entries(block.tiers).map(([tier, count]) => (
                            <div key={tier} className="flex justify-between">
                              <span className="text-text-muted">{tier}:</span>
                              <span className="font-medium">{count}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
