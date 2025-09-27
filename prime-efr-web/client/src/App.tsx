import { useState } from 'react';
import { Provider } from 'react-redux';
import { Layout, Menu } from 'antd';
import { UploadOutlined, BarChartOutlined, SettingOutlined, FileExcelOutlined } from '@ant-design/icons';
import { store } from './store';
import Header from './components/Header';
import FileUpload from './components/FileUpload';
import ValidationDashboard from './components/ValidationDashboard';
import TabGrid from './components/TabGrid';
import DiscrepancyPanel from './components/DiscrepancyPanel';
import ConfigManager from './components/ConfigManager';

const { Sider, Content } = Layout;

type ViewId = 'upload' | 'validation' | 'config';

const menuItems = [
  {
    key: 'upload',
    icon: <UploadOutlined />,
    label: 'Upload Data',
  },
  {
    key: 'validation',
    icon: <BarChartOutlined />,
    label: 'Validation Dashboard',
  },
  {
    key: 'config',
    icon: <SettingOutlined />,
    label: 'Configuration',
  },
];

function App() {
  const [activeView, setActiveView] = useState<ViewId>('upload');
  const [collapsed, setCollapsed] = useState(false);

  const handleMenuClick = ({ key }: { key: string }) => {
    setActiveView(key as ViewId);
  };

  return (
    <Provider store={store}>
      <Layout style={{ minHeight: '100vh' }}>
        <Sider 
          collapsible 
          collapsed={collapsed} 
          onCollapse={setCollapsed}
          theme="light"
          width={256}
          style={{
            position: 'fixed',
            height: '100vh',
            left: 0,
            top: 0,
            bottom: 0,
          }}
        >
          <div className="flex items-center justify-center h-16 border-b border-gray-200">
            <FileExcelOutlined className="text-2xl text-blue-500" />
            {!collapsed && (
              <span className="ml-3 text-lg font-semibold text-gray-900">Prime EFR</span>
            )}
          </div>
          <Menu
            mode="inline"
            selectedKeys={[activeView]}
            onClick={handleMenuClick}
            items={menuItems}
            style={{ borderRight: 0, marginTop: 16 }}
          />
        </Sider>
        
        <Layout style={{ marginLeft: collapsed ? 80 : 256, transition: 'margin-left 0.2s' }}>
          <Header />
          
          <Content style={{ margin: '24px', overflow: 'initial' }}>
            {activeView === 'upload' && (
              <div className="space-y-6">
                <FileUpload />
                <TabGrid />
              </div>
            )}

            {activeView === 'validation' && (
              <div className="grid grid-cols-1 gap-6 lg:grid-cols-[2fr_1fr]">
                <ValidationDashboard />
                <div>
                  <DiscrepancyPanel />
                </div>
              </div>
            )}

            {activeView === 'config' && <ConfigManager />}
          </Content>
        </Layout>
      </Layout>
    </Provider>
  );
}

export default App;
