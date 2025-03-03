import { useState, useEffect } from 'react';
import { Row, Col, Card, Statistic, List, Tag, Progress, Alert, Typography, Space } from 'antd';
import { 
  ClockCircleOutlined, 
  CheckCircleOutlined, 
  WarningOutlined, 
  DollarOutlined,
  UserOutlined,
  ArrowUpOutlined
} from '@ant-design/icons';

const { Title, Text } = Typography;

// Sample JSON data that would come from backend
const sampleData = {
  user: {
    name: "Dr. Smith",
    role: "Medical Coder & Biller",
    avatar: null
  },
  stats: {
    pendingTasks: 12,
    approvedClaims: 45,
    rejectedClaims: 8,
    totalRevenue: 42650
  },
  pendingTasks: [
    { id: 1, title: 'Review patient encounter #12345', priority: 'high', due: '2 hours' },
    { id: 2, title: 'Verify ICD-10 codes for claim #67890', priority: 'medium', due: '4 hours' },
    { id: 3, title: 'Update patient information for John Doe', priority: 'low', due: '1 day' },
    { id: 4, title: 'Submit claim for patient #54321', priority: 'medium', due: '1 day' },
  ],
  claimStatuses: [
    { id: 1, patient: 'Sarah Johnson', claimId: 'CLM-2023-001', status: 'approved', amount: 1250.00 },
    { id: 2, patient: 'Michael Smith', claimId: 'CLM-2023-002', status: 'pending', amount: 780.50 },
    { id: 3, patient: 'Emily Davis', claimId: 'CLM-2023-003', status: 'rejected', amount: 450.75 },
    { id: 4, patient: 'Robert Wilson', claimId: 'CLM-2023-004', status: 'pending', amount: 920.25 },
  ],
  errorAlerts: [
    { id: 1, message: 'Missing diagnosis code for claim #67890', level: 'error' },
    { id: 2, message: 'Potential code mismatch in patient encounter #12345', level: 'warning' },
    { id: 3, message: 'Duplicate claim submission detected for patient #54321', level: 'error' },
  ],
  codingAccuracy: {
    icd10: 92,
    cpt: 88,
    hcpcs: 85
  },
  revenueData: {
    current: 42650,
    previous: 38500,
    percentChange: 10.8
  }
};

const DashboardHome = () => {
  // State to store data that would come from API
  const [data, setData] = useState(sampleData);
  
  // Simulate API call
  useEffect(() => {
    // In a real app, this would be an API call
    setData(sampleData);
  }, []);

  const getPriorityColor = (priority) => {
    switch(priority) {
      case 'high': return '#ff5e57';
      case 'medium': return '#ffdd59';
      case 'low': return '#0be881';
      default: return '#8c7ae6';
    }
  };

  const getStatusColor = (status) => {
    switch(status) {
      case 'approved': return 'success';
      case 'pending': return 'processing';
      case 'rejected': return 'error';
      default: return 'default';
    }
  };

  const getAlertType = (level) => {
    switch(level) {
      case 'error': return 'error';
      case 'warning': return 'warning';
      default: return 'info';
    }
  };

  return (
    <div className="dashboard-home" style={{ padding: '16px', background: '#000000', width: '100%' }}>
      <Space direction="vertical" size="middle" style={{ width: '100%', display: 'flex' }}>
        <div className="welcome-section" style={{ 
          padding: '16px', 
          background: 'linear-gradient(135deg, #121212, #1a1a1a)', 
          borderRadius: '12px', 
          border: '1px solid #333333',
          width: '100%'
        }}>
          <Row gutter={[16, 16]} align="middle" style={{ width: '100%' }}>
            <Col>
              <div className="avatar-container" style={{ 
                width: 64, 
                height: 64, 
                borderRadius: '50%', 
                background: 'linear-gradient(135deg, #8c7ae6, #7158e2)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: 32,
                color: 'white',
                boxShadow: '0 4px 12px rgba(113, 88, 226, 0.4)'
              }}>
                <UserOutlined />
              </div>
            </Col>
            <Col flex="1">
              <Title level={2} style={{ margin: 0, color: 'white' }}>Welcome, {data.user.name}</Title>
              <Text style={{ color: 'rgba(255, 255, 255, 0.85)' }}>{data.user.role}</Text>
            </Col>
          </Row>
        </div>

        <Row gutter={[16, 16]} style={{ width: '100%', margin: 0 }}>
          <Col xs={24} sm={12} md={6} style={{ padding: '0 8px' }}>
            <Card 
              className="stat-card"
              style={{ 
                background: 'linear-gradient(135deg, #121212, #1a1a1a)',
                borderRadius: '12px',
                border: '1px solid #333333',
                boxShadow: '0 8px 24px rgba(0, 0, 0, 0.4)',
                margin: 0,
                width: '100%'
              }}
              bodyStyle={{ padding: '20px', width: '100%' }}
            >
              <Statistic 
                title={<span style={{ color: 'rgba(255, 255, 255, 0.85)' }}>Pending Tasks</span>}
                value={data.stats.pendingTasks}
                valueStyle={{ color: '#8c7ae6', fontWeight: 'bold' }}
                prefix={<ClockCircleOutlined style={{ marginRight: '8px' }} />}
                suffix={<small style={{ fontSize: '14px', color: 'rgba(255, 255, 255, 0.65)' }}> tasks</small>}
              />
            </Card>
          </Col>
          <Col xs={24} sm={12} md={6} style={{ padding: '0 8px' }}>
            <Card 
              className="stat-card"
              style={{ 
                background: 'linear-gradient(135deg, #121212, #1a1a1a)',
                borderRadius: '12px',
                border: '1px solid #333333',
                boxShadow: '0 8px 24px rgba(0, 0, 0, 0.4)',
                margin: 0,
                width: '100%'
              }}
              bodyStyle={{ padding: '20px', width: '100%' }}
            >
              <Statistic 
                title={<span style={{ color: 'rgba(255, 255, 255, 0.85)' }}>Approved Claims</span>}
                value={data.stats.approvedClaims}
                valueStyle={{ color: '#0be881', fontWeight: 'bold' }}
                prefix={<CheckCircleOutlined style={{ marginRight: '8px' }} />}
                suffix={<small style={{ fontSize: '14px', color: 'rgba(255, 255, 255, 0.65)' }}> claims</small>}
              />
            </Card>
          </Col>
          <Col xs={24} sm={12} md={6} style={{ padding: '0 8px' }}>
            <Card 
              className="stat-card"
              style={{ 
                background: 'linear-gradient(135deg, #121212, #1a1a1a)',
                borderRadius: '12px',
                border: '1px solid #333333',
                boxShadow: '0 8px 24px rgba(0, 0, 0, 0.4)',
                margin: 0,
                width: '100%'
              }}
              bodyStyle={{ padding: '20px', width: '100%' }}
            >
              <Statistic 
                title={<span style={{ color: 'rgba(255, 255, 255, 0.85)' }}>Rejected Claims</span>}
                value={data.stats.rejectedClaims}
                valueStyle={{ color: '#ff5e57', fontWeight: 'bold' }}
                prefix={<WarningOutlined style={{ marginRight: '8px' }} />}
                suffix={<small style={{ fontSize: '14px', color: 'rgba(255, 255, 255, 0.65)' }}> claims</small>}
              />
            </Card>
          </Col>
          <Col xs={24} sm={12} md={6} style={{ padding: '0 8px' }}>
            <Card 
              className="stat-card"
              style={{ 
                background: 'linear-gradient(135deg, #121212, #1a1a1a)',
                borderRadius: '12px',
                border: '1px solid #333333',
                boxShadow: '0 8px 24px rgba(0, 0, 0, 0.4)',
                margin: 0,
                width: '100%'
              }}
              bodyStyle={{ padding: '20px', width: '100%' }}
            >
              <Statistic 
                title={<span style={{ color: 'rgba(255, 255, 255, 0.85)' }}>Total Revenue</span>}
                value={data.stats.totalRevenue}
                precision={2}
                valueStyle={{ color: '#ffdd59', fontWeight: 'bold' }}
                prefix={<DollarOutlined style={{ marginRight: '8px' }} />}
                suffix={
                  <div style={{ display: 'inline-flex', alignItems: 'center', marginLeft: '8px' }}>
                    <ArrowUpOutlined style={{ color: '#0be881', fontSize: '12px' }} />
                    <span style={{ color: '#0be881', fontSize: '12px' }}>{data.revenueData.percentChange}%</span>
                  </div>
                }
              />
            </Card>
          </Col>
        </Row>

        <Row gutter={[16, 16]} style={{ width: '100%', margin: 0 }}>
          <Col xs={24} lg={12} style={{ padding: '0 8px' }}>
            <Card 
              title={<span style={{ color: 'white' }}>Pending Tasks</span>}
              style={{ 
                background: 'linear-gradient(135deg, #121212, #1a1a1a)',
                borderRadius: '12px',
                border: '1px solid #333333',
                boxShadow: '0 8px 24px rgba(0, 0, 0, 0.4)',
                margin: 0,
                width: '100%'
              }}
              headStyle={{ borderBottom: '1px solid #333333' }}
              bodyStyle={{ width: '100%', padding: '0' }}
            >
              <List
                dataSource={data.pendingTasks}
                style={{ width: '100%' }}
                renderItem={item => (
                  <List.Item
                    style={{ borderBottom: '1px solid #333333', width: '100%', padding: '12px 16px' }}
                  >
                    <div style={{ width: '100%' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px', width: '100%' }}>
                        <Text style={{ color: 'white' }}>{item.title}</Text>
                        <Tag color={getPriorityColor(item.priority)} style={{ borderRadius: '4px', boxShadow: '0 2px 4px rgba(0, 0, 0, 0.2)' }}>
                          {item.priority.toUpperCase()}
                        </Tag>
                      </div>
                      <div style={{ display: 'flex', alignItems: 'center' }}>
                        <ClockCircleOutlined style={{ color: 'rgba(255, 255, 255, 0.65)', marginRight: '5px' }} />
                        <Text style={{ color: 'rgba(255, 255, 255, 0.65)' }}>Due in {item.due}</Text>
                      </div>
                    </div>
                  </List.Item>
                )}
              />
            </Card>
          </Col>
          <Col xs={24} lg={12} style={{ padding: '0 8px' }}>
            <Card 
              title={<span style={{ color: 'white' }}>Recent Claims</span>}
              style={{ 
                background: 'linear-gradient(135deg, #121212, #1a1a1a)',
                borderRadius: '12px',
                border: '1px solid #333333',
                boxShadow: '0 8px 24px rgba(0, 0, 0, 0.4)',
                margin: 0,
                width: '100%'
              }}
              headStyle={{ borderBottom: '1px solid #333333' }}
              bodyStyle={{ width: '100%', padding: '0' }}
            >
              <List
                dataSource={data.claimStatuses}
                style={{ width: '100%' }}
                renderItem={item => (
                  <List.Item
                    style={{ borderBottom: '1px solid #333333', width: '100%', padding: '12px 16px' }}
                  >
                    <div style={{ width: '100%' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px', width: '100%' }}>
                        <Text style={{ color: 'white' }}>{item.patient}</Text>
                        <Tag color={getStatusColor(item.status)} style={{ borderRadius: '4px', boxShadow: '0 2px 4px rgba(0, 0, 0, 0.2)' }}>
                          {item.status.toUpperCase()}
                        </Tag>
                      </div>
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', width: '100%' }}>
                        <Text style={{ color: 'rgba(255, 255, 255, 0.65)' }}>{item.claimId}</Text>
                        <Text style={{ color: 'rgba(255, 255, 255, 0.85)' }}>${item.amount.toFixed(2)}</Text>
                      </div>
                    </div>
                  </List.Item>
                )}
              />
            </Card>
          </Col>
        </Row>

        <Card 
          title={<span style={{ color: 'white' }}>Error Alerts</span>}
          style={{ 
            background: 'linear-gradient(135deg, #121212, #1a1a1a)',
            borderRadius: '12px',
            border: '1px solid #333333',
            boxShadow: '0 8px 24px rgba(0, 0, 0, 0.4)',
            margin: 0,
            width: '100%'
          }}
          headStyle={{ borderBottom: '1px solid #333333' }}
          bodyStyle={{ width: '100%', padding: '16px' }}
        >
          <Space direction="vertical" style={{ width: '100%' }}>
            {data.errorAlerts.map(alert => (
              <Alert
                key={alert.id}
                message={alert.message}
                type={getAlertType(alert.level)}
                showIcon
                style={{ 
                  background: 'rgba(18, 18, 18, 0.6)',
                  border: '1px solid #333333',
                  borderRadius: '8px',
                  marginBottom: '8px',
                  width: '100%'
                }}
              />
            ))}
          </Space>
        </Card>

        <Card 
          title={<span style={{ color: 'white' }}>Coding Accuracy</span>}
          style={{ 
            background: 'linear-gradient(135deg, #121212, #1a1a1a)',
            borderRadius: '12px',
            border: '1px solid #333333',
            boxShadow: '0 8px 24px rgba(0, 0, 0, 0.4)',
            margin: 0,
            width: '100%'
          }}
          headStyle={{ borderBottom: '1px solid #333333' }}
          bodyStyle={{ width: '100%', padding: '16px' }}
        >
          <Row gutter={[16, 16]} style={{ width: '100%', margin: 0 }}>
            <Col xs={24} md={8} style={{ padding: '0 8px', display: 'flex', justifyContent: 'center' }}>
              <div style={{ textAlign: 'center' }}>
                <Text style={{ color: 'rgba(255, 255, 255, 0.85)', display: 'block', marginBottom: '8px' }}>ICD-10 Coding</Text>
                <Progress 
                  type="dashboard" 
                  percent={data.codingAccuracy.icd10} 
                  strokeColor={{
                    '0%': '#8c7ae6',
                    '100%': '#7158e2',
                  }}
                  trailColor="rgba(18, 18, 18, 0.6)"
                  gapDegree={30}
                  strokeWidth={12}
                  width={180}
                />
              </div>
            </Col>
            <Col xs={24} md={8} style={{ padding: '0 8px', display: 'flex', justifyContent: 'center' }}>
              <div style={{ textAlign: 'center' }}>
                <Text style={{ color: 'rgba(255, 255, 255, 0.85)', display: 'block', marginBottom: '8px' }}>CPT Coding</Text>
                <Progress 
                  type="dashboard" 
                  percent={data.codingAccuracy.cpt} 
                  strokeColor={{
                    '0%': '#0be881',
                    '100%': '#05c46b',
                  }}
                  trailColor="rgba(18, 18, 18, 0.6)"
                  gapDegree={30}
                  strokeWidth={12}
                  width={180}
                />
              </div>
            </Col>
            <Col xs={24} md={8} style={{ padding: '0 8px', display: 'flex', justifyContent: 'center' }}>
              <div style={{ textAlign: 'center' }}>
                <Text style={{ color: 'rgba(255, 255, 255, 0.85)', display: 'block', marginBottom: '8px' }}>HCPCS Coding</Text>
                <Progress 
                  type="dashboard" 
                  percent={data.codingAccuracy.hcpcs} 
                  strokeColor={{
                    '0%': '#ffdd59',
                    '100%': '#ffd32a',
                  }}
                  trailColor="rgba(18, 18, 18, 0.6)"
                  gapDegree={30}
                  strokeWidth={12}
                  width={180}
                />
              </div>
            </Col>
          </Row>
        </Card>
      </Space>
    </div>
  );
};

export default DashboardHome; 