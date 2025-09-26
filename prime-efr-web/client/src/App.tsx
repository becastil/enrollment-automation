import { useState } from 'react';
import { Provider } from 'react-redux';
import type { LucideIcon } from 'lucide-react';
import { Upload, BarChart3, Settings2, FileSpreadsheet } from 'lucide-react';
import { store } from './store';
import Header from './components/Header';
import FileUpload from './components/FileUpload';
import ValidationDashboard from './components/ValidationDashboard';
import TabGrid from './components/TabGrid';
import DiscrepancyPanel from './components/DiscrepancyPanel';
import ConfigManager from './components/ConfigManager';

type ViewId = 'upload' | 'validation' | 'config';

type NavItem = {
  id: ViewId;
  label: string;
  longLabel: string;
  icon: LucideIcon;
};

const NAV_ITEMS: NavItem[] = [
  { id: 'upload', label: 'Upload', longLabel: 'Upload Data', icon: Upload },
  { id: 'validation', label: 'Validation', longLabel: 'Validation Dashboard', icon: BarChart3 },
  { id: 'config', label: 'Config', longLabel: 'Configuration', icon: Settings2 },
];

function App() {
  const [activeView, setActiveView] = useState<ViewId>('upload');

  return (
    <Provider store={store}>
      <div className="app-shell">
        <aside className="app-shell__sidebar">
          <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-primary-soft text-primary lg:w-full lg:justify-start lg:px-sm">
            <FileSpreadsheet className="h-6 w-6" aria-hidden="true" />
            <span className="sr-only lg:hidden">Prime EFR</span>
            <span className="hidden lg:ml-sm lg:inline-block lg:text-sm lg:font-semibold">Prime EFR</span>
          </div>
          <nav className="flex w-full flex-col gap-xs" aria-label="Primary views">
            {NAV_ITEMS.map(({ id, label, longLabel, icon: Icon }) => {
              const isActive = activeView === id;
              return (
                <button
                  key={id}
                  type="button"
                  aria-label={longLabel}
                  aria-current={isActive ? 'page' : undefined}
                  onClick={() => setActiveView(id)}
                  className={`flex h-12 w-12 items-center justify-center rounded-md transition-colors lg:w-full lg:justify-start lg:px-sm lg:py-2 ${
                    isActive
                      ? 'bg-primary-soft text-primary'
                      : 'text-text-muted hover:bg-surface-subtle hover:text-text'
                  }`}
                >
                  <Icon className="h-5 w-5" />
                  <span className="hidden lg:ml-sm lg:inline">{label}</span>
                </button>
              );
            })}
          </nav>
        </aside>

        <div className="app-shell__header">
          <Header />
        </div>

        <section className="app-shell__filters" aria-label="View switcher">
          <div className="app-shell__container py-sm">
            <div className="flex flex-wrap items-center gap-xs">
              {NAV_ITEMS.map(({ id, longLabel }) => {
                const isActive = activeView === id;
                return (
                  <button
                    key={`filter-${id}`}
                    type="button"
                    aria-current={isActive ? 'page' : undefined}
                    onClick={() => setActiveView(id)}
                    className={`rounded-full border px-sm py-2xs text-sm font-medium transition-colors ${
                      isActive
                        ? 'border-primary bg-primary text-text-inverse'
                        : 'border-border text-text-muted hover:bg-surface-subtle hover:text-text'
                    }`}
                  >
                    {longLabel}
                  </button>
                );
              })}
            </div>
          </div>
        </section>

        <main className="app-shell__content">
          <div className="app-shell__container space-y-xl">
            {activeView === 'upload' && (
              <div className="space-y-xl">
                <FileUpload />
                <TabGrid />
              </div>
            )}

            {activeView === 'validation' && (
              <div className="grid grid-cols-1 gap-xl lg:grid-cols-[minmax(0,2fr)_minmax(0,1fr)]">
                <ValidationDashboard />
                <div>
                  <DiscrepancyPanel />
                </div>
              </div>
            )}

            {activeView === 'config' && <ConfigManager />}
          </div>
        </main>
      </div>
    </Provider>
  );
}

export default App;
