import { useMemo } from 'react';
import { useSelector } from 'react-redux';
import { Card, Statistic, Row, Col, Alert, List } from 'antd';
import { CheckCircleOutlined, CloseCircleOutlined, WarningOutlined, InfoCircleOutlined } from '@ant-design/icons';
import type { RootState } from '../store';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';
import { useTheme } from '../theme/ThemeProvider';
import { getChartPalette } from '../utils/theme';

export default function ValidationDashboard() {
  const { theme } = useTheme();
  const { controlTotals, tabData } = useSelector((state: RootState) => state.enrollment);
  const { summary, issues } = useSelector((state: RootState) => state.validation);

  const tierData = Object.entries(controlTotals).map(([tier, count]) => ({
    name: tier,
    value: count,
  }));

  const COLORS = useMemo(() => getChartPalette(), [theme]);
        return <InfoCircleOutlined />;
    }
  };

  const getIssueAlertType = (type: string): 'error' | 'warning' | 'info' => {
    switch (type) {
      case 'error':
        return 'error';
      case 'warning':
        return 'warning';
      case 'info':
      default:
        return 'info';
    }
  };

  const totalEnrollment = Object.values(controlTotals).reduce((a, b) => a + b, 0);

  return (
    <div className="space-y-6">
      <Card title="Control Totals">
        <Row gutter={[24, 24]}>
          <Col xs={24} lg={12}>
            <div className="space-y-4">
              <h4 className="text-base font-medium text-gray-600 mb-3">Tier Distribution</h4>
              <Row gutter={[16, 16]}>
                {Object.entries(controlTotals).map(([tier, count]) => (
                  <Col xs={12} sm={8} key={tier}>
                    <Statistic 
                      title={tier}
                      value={count}
                      formatter={(value) => value?.toLocaleString()}
                      valueStyle={{ fontSize: '18px' }}
                    />
                  </Col>
                ))}
              </Row>
              <div className="pt-4 border-t border-gray-200">
                <Statistic 
                  title="Total Enrollment"
                  value={totalEnrollment}
                  formatter={(value) => value?.toLocaleString()}
                  valueStyle={{ fontSize: '24px', fontWeight: 'bold', color: '#1890ff' }}
                />
              </div>
            </div>
          </Col>
          
          <Col xs={24} lg={12}>
            <div style={{ height: 300 }}>
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={tierData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    outerRadius={80}
                    fill="var(--color-primary)"
                    dataKey="value"
                  >
                    {tierData.map((_, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </Col>
        </Row>
      </Card>

      <Card title="Validation Summary">
        {summary ? (
          <div className="space-y-6">
            <Row gutter={[16, 16]}>
              <Col xs={24} sm={8}>
                <Card>
                  <Statistic
                    title="Errors"
                    value={summary.errors}
                    prefix={<CloseCircleOutlined />}
                    valueStyle={{ color: '#ff4d4f' }}
                  />
                </Card>
              </Col>
              <Col xs={24} sm={8}>
                <Card>
                  <Statistic
                    title="Warnings"
                    value={summary.warnings}
                    prefix={<WarningOutlined />}
                    valueStyle={{ color: '#faad14' }}
                  />
                </Card>
              </Col>
              <Col xs={24} sm={8}>
                <Card>
                  <Statistic
                    title="Info"
                    value={summary.info}
                    prefix={<InfoCircleOutlined />}
                    valueStyle={{ color: '#1890ff' }}
                  />
                </Card>
              </Col>
            </Row>

            <div>
              <h4 className="text-base font-medium mb-3">Recent Issues</h4>
              <List
                size="small"
                dataSource={issues.slice(0, 5)}
                renderItem={(issue) => (
                  <List.Item>
                    <Alert
                      message={issue.message}
                      description={issue.tab ? `Tab: ${issue.tab}` : undefined}
                      type={getIssueAlertType(issue.type)}
                      showIcon
                      style={{ width: '100%' }}
                    />
                  </List.Item>
                )}
                style={{ maxHeight: 300, overflow: 'auto' }}
              />
            </div>
          </div>
        ) : (
          <div className="text-center py-12">
            <CheckCircleOutlined style={{ fontSize: 48, color: '#52c41a', marginBottom: 16 }} />
            <p className="text-gray-500">No validation issues found</p>
          </div>
        )}
      </Card>

      <Card title="Tab Validation Status">
        <Row gutter={[16, 16]}>
          {tabData.slice(0, 10).map((tab) => (
            <Col xs={12} sm={8} md={6} key={tab.name}>
              <Card 
                size="small"
                style={{
                  borderColor: tab.hasDiscrepancies ? '#ff4d4f' : '#52c41a',
                  backgroundColor: tab.hasDiscrepancies ? '#fff2f0' : '#f6ffed'
                }}
              >
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium truncate">{tab.name}</span>
                  {tab.hasDiscrepancies ? (
                    <CloseCircleOutlined style={{ color: '#ff4d4f' }} />
                  ) : (
                    <CheckCircleOutlined style={{ color: '#52c41a' }} />
                  )}
                </div>
              </Card>
            </Col>
          ))}
        </Row>
      </Card>
    </div>
  );
}
