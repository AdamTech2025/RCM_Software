import { useState, useEffect } from 'react';
import { Input, Select, Button, Table, Card, Typography, Space, Tag, Tabs, Tooltip, Row, Col, List, Divider } from 'antd';
import { SearchOutlined, BulbOutlined, HistoryOutlined, StarOutlined, StarFilled } from '@ant-design/icons';

const { Title, Text, Paragraph } = Typography;
const { Option } = Select;
const { TabPane } = Tabs;

// Sample JSON data that would come from backend
const sampleData = {
  searchResults: {
    'ICD-10': [
      { code: 'I10', description: 'Essential (primary) hypertension', category: 'Diseases of the circulatory system' },
      { code: 'E11.9', description: 'Type 2 diabetes mellitus without complications', category: 'Endocrine, nutritional and metabolic diseases' },
      { code: 'J45.909', description: 'Unspecified asthma, uncomplicated', category: 'Diseases of the respiratory system' },
      { code: 'M54.5', description: 'Low back pain', category: 'Diseases of the musculoskeletal system and connective tissue' },
    ],
    'CPT': [
      { code: '99213', description: 'Office or other outpatient visit for the evaluation and management of an established patient', category: 'Evaluation and Management' },
      { code: '99214', description: 'Office or other outpatient visit for the evaluation and management of an established patient (moderate complexity)', category: 'Evaluation and Management' },
      { code: '36415', description: 'Collection of venous blood by venipuncture', category: 'Laboratory' },
      { code: '71045', description: 'Radiologic examination, chest; single view', category: 'Radiology' },
    ],
    'HCPCS': [
      { code: 'G0008', description: 'Administration of influenza virus vaccine', category: 'Procedures/Professional Services' },
      { code: 'J0131', description: 'Injection, acetaminophen, 10 mg', category: 'Drugs' },
      { code: 'A4253', description: 'Blood glucose test or reagent strips for home blood glucose monitor, per 50 strips', category: 'Medical Equipment' },
      { code: 'E0601', description: 'Continuous positive airway pressure (CPAP) device', category: 'Durable Medical Equipment' },
    ]
  },
  aiSuggestions: [
    { id: 1, code: 'I10', description: 'Essential (primary) hypertension', confidence: 95, notes: 'Based on documented elevated blood pressure readings and current medications.' },
    { id: 2, code: 'E78.5', description: 'Hyperlipidemia, unspecified', confidence: 88, notes: 'Patient has documented high cholesterol levels in lab results.' },
    { id: 3, code: '99214', description: 'Office visit, established patient (moderate complexity)', confidence: 92, notes: 'Visit included detailed history, examination and moderate complexity decision making.' },
  ],
  recentSearches: [
    { code: 'J44.9', description: 'Chronic obstructive pulmonary disease, unspecified', type: 'ICD-10', timestamp: '10 minutes ago' },
    { code: '99213', description: 'Office visit, established patient (low complexity)', type: 'CPT', timestamp: '1 hour ago' },
    { code: 'E11.9', description: 'Type 2 diabetes mellitus without complications', type: 'ICD-10', timestamp: '3 hours ago' },
  ],
  favoriteItems: [
    { code: 'I10', description: 'Essential (primary) hypertension', type: 'ICD-10' },
    { code: '99214', description: 'Office visit, established patient (moderate complexity)', type: 'CPT' },
    { code: 'J0131', description: 'Injection, acetaminophen, 10 mg', type: 'HCPCS' },
  ],
  patientContext: {
    name: "John Doe",
    age: 58,
    gender: "male",
    complaint: "Patient presents with chest pain, shortness of breath, and fatigue for the past 3 days.",
    vitals: "BP 150/90, HR 88, RR 18, Temp 98.6°F",
    history: "Hypertension, Hyperlipidemia, Type 2 Diabetes",
    medications: "Lisinopril 10mg daily, Atorvastatin 20mg daily, Metformin 500mg twice daily",
    assessment: "Patient with uncontrolled hypertension and hyperlipidemia. EKG shows normal sinus rhythm. Lab results show elevated cholesterol levels."
  }
};

const CodeLookup = () => {
  // State to store data that would come from API
  const [data, setData] = useState(sampleData);
  const [searchTerm, setSearchTerm] = useState('');
  const [codeType, setCodeType] = useState('ICD-10');
  const [searchResults, setSearchResults] = useState([]);
  const [favorites, setFavorites] = useState(data.favoriteItems);
  const [activeTab, setActiveTab] = useState('search');

  // Simulate API call
  useEffect(() => {
    // In a real app, this would be an API call
    setData(sampleData);
    setFavorites(sampleData.favoriteItems);
  }, []);

  const handleSearch = () => {
    // In a real application, this would be an API call
    setSearchResults(data.searchResults[codeType]);
  };

  const handleFavoriteToggle = (code) => {
    const isFavorite = favorites.some(item => item.code === code.code);
    if (isFavorite) {
      setFavorites(favorites.filter(item => item.code !== code.code));
    } else {
      setFavorites([...favorites, { ...code, type: codeType }]);
    }
  };

  const isFavorite = (code) => {
    return favorites.some(item => item.code === code);
  };

  const columns = [
    {
      title: <span style={{ color: 'white' }}>Code</span>,
      dataIndex: 'code',
      key: 'code',
      width: '15%',
      render: (text) => <Text strong style={{ color: 'white' }}>{text}</Text>,
    },
    {
      title: <span style={{ color: 'white' }}>Description</span>,
      dataIndex: 'description',
      key: 'description',
      width: '45%',
      render: (text) => <Text style={{ color: 'rgba(255, 255, 255, 0.85)' }}>{text}</Text>,
    },
    {
      title: <span style={{ color: 'white' }}>Category</span>,
      dataIndex: 'category',
      key: 'category',
      width: '20%',
      render: (text) => <Tag color="#8c7ae6" style={{ borderRadius: '4px', boxShadow: '0 2px 4px rgba(0, 0, 0, 0.2)' }}>{text}</Tag>,
    },
    {
      title: <span style={{ color: 'white' }}>Actions</span>,
      key: 'actions',
      width: '20%',
      render: (_, record) => (
        <Space>
          <Tooltip title={isFavorite(record.code) ? "Remove from favorites" : "Add to favorites"}>
            <Button 
              type="text" 
              icon={isFavorite(record.code) ? <StarFilled style={{ color: '#ffdd59' }} /> : <StarOutlined style={{ color: 'white' }} />} 
              onClick={() => handleFavoriteToggle(record)}
            />
          </Tooltip>
          <Button type="primary" size="small" style={{ borderRadius: '8px' }}>
            Use Code
          </Button>
        </Space>
      ),
    },
  ];

  const aiSuggestionColumns = [
    {
      title: <span style={{ color: 'white' }}>Code</span>,
      dataIndex: 'code',
      key: 'code',
      width: '15%',
      render: (text) => <Text strong style={{ color: 'white' }}>{text}</Text>,
    },
    {
      title: <span style={{ color: 'white' }}>Description</span>,
      dataIndex: 'description',
      key: 'description',
      width: '30%',
      render: (text) => <Text style={{ color: 'rgba(255, 255, 255, 0.85)' }}>{text}</Text>,
    },
    {
      title: <span style={{ color: 'white' }}>Confidence</span>,
      dataIndex: 'confidence',
      key: 'confidence',
      width: '15%',
      render: (value) => {
        let color = '#0be881';
        if (value < 80) color = '#ffdd59';
        if (value < 70) color = '#ff5e57';
        
        return (
          <Tag color={color} style={{ borderRadius: '4px', boxShadow: '0 2px 4px rgba(0, 0, 0, 0.2)' }}>
            {value}%
          </Tag>
        );
      },
    },
    {
      title: <span style={{ color: 'white' }}>Notes</span>,
      dataIndex: 'notes',
      key: 'notes',
      width: '25%',
      render: (text) => <Text style={{ color: 'rgba(255, 255, 255, 0.65)' }}>{text}</Text>,
    },
    {
      title: <span style={{ color: 'white' }}>Actions</span>,
      key: 'actions',
      width: '15%',
      render: () => (
        <Button type="primary" size="small" style={{ borderRadius: '8px' }}>
          Use Code
        </Button>
      ),
    },
  ];

  return (
    <div className="code-lookup" style={{ padding: '16px', background: '#000000', width: '100%' }}>
      <Title level={2} style={{ color: 'white', marginBottom: '16px' }}>Code Lookup & AI Suggestions</Title>
      
      <Tabs 
        activeKey={activeTab} 
        onChange={setActiveTab}
        type="card"
        className="custom-tabs"
        style={{ marginBottom: '16px', width: '100%' }}
      >
        <TabPane 
          tab={
            <span style={{ color: 'white' }}>
              <SearchOutlined /> Search Codes
            </span>
          } 
          key="search"
          style={{ width: '100%' }}
        >
          <Card 
            style={{ 
              background: 'linear-gradient(135deg, #121212, #1a1a1a)',
              borderRadius: '12px',
              border: '1px solid #333333',
              boxShadow: '0 8px 24px rgba(0, 0, 0, 0.4)',
              marginBottom: '16px',
              margin: 0,
              width: '100%'
            }}
          >
            <Space direction="vertical" size="middle" style={{ width: '100%' }}>
              <Row gutter={[16, 16]} align="middle" style={{ width: '100%' }}>
                <Col xs={24} md={6}>
                  <Select
                    value={codeType}
                    onChange={setCodeType}
                    style={{ width: '100%' }}
                  >
                    <Option value="ICD-10">ICD-10</Option>
                    <Option value="CPT">CPT</Option>
                    <Option value="HCPCS">HCPCS</Option>
                  </Select>
                </Col>
                <Col xs={24} md={14}>
                  <Input
                    placeholder="Search by code or description..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    prefix={<SearchOutlined style={{ color: 'rgba(255, 255, 255, 0.65)' }} />}
                    style={{ width: '100%' }}
                  />
                </Col>
                <Col xs={24} md={4}>
                  <Button 
                    type="primary" 
                    onClick={handleSearch}
                    style={{ width: '100%' }}
                  >
                    Search
                  </Button>
                </Col>
              </Row>

              {searchResults.length > 0 && (
                <>
                  <Divider style={{ borderColor: '#333333', margin: '12px 0' }} />
                  <div style={{ width: '100%', overflowX: 'auto' }}>
                    <Table 
                      columns={columns} 
                      dataSource={searchResults} 
                      rowKey="code"
                      pagination={false}
                      style={{ width: '100%' }}
                    />
                  </div>
                </>
              )}
            </Space>
          </Card>

          <Row gutter={[16, 16]} style={{ width: '100%' }}>
            <Col xs={24} md={12}>
              <Card 
                title={<span style={{ color: 'white' }}><HistoryOutlined /> Recent Searches</span>}
                style={{ 
                  background: 'linear-gradient(135deg, #121212, #1a1a1a)',
                  borderRadius: '12px',
                  border: '1px solid #333333',
                  boxShadow: '0 8px 24px rgba(0, 0, 0, 0.4)',
                  margin: 0,
                  width: '100%'
                }}
                headStyle={{ borderBottom: '1px solid #333333' }}
              >
                <List
                  dataSource={data.recentSearches}
                  style={{ width: '100%' }}
                  renderItem={item => (
                    <List.Item
                      style={{ borderBottom: '1px solid #333333', width: '100%' }}
                    >
                      <div style={{ width: '100%' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px', width: '100%' }}>
                          <Space>
                            <Text strong style={{ color: 'white' }}>{item.code}</Text>
                            <Tag color="#8c7ae6" style={{ borderRadius: '4px', boxShadow: '0 2px 4px rgba(0, 0, 0, 0.2)' }}>{item.type}</Tag>
                          </Space>
                          <Text style={{ color: 'rgba(255, 255, 255, 0.65)', fontSize: '12px' }}>{item.timestamp}</Text>
                        </div>
                        <Text style={{ color: 'rgba(255, 255, 255, 0.85)' }}>{item.description}</Text>
                      </div>
                    </List.Item>
                  )}
                />
              </Card>
            </Col>
            <Col xs={24} md={12}>
              <Card 
                title={<span style={{ color: 'white' }}><StarFilled style={{ color: '#ffdd59' }} /> Favorites</span>}
                style={{ 
                  background: 'linear-gradient(135deg, #121212, #1a1a1a)',
                  borderRadius: '12px',
                  border: '1px solid #333333',
                  boxShadow: '0 8px 24px rgba(0, 0, 0, 0.4)',
                  margin: 0,
                  width: '100%'
                }}
                headStyle={{ borderBottom: '1px solid #333333' }}
              >
                <List
                  dataSource={favorites}
                  style={{ width: '100%' }}
                  renderItem={item => (
                    <List.Item
                      style={{ borderBottom: '1px solid #333333', width: '100%' }}
                      actions={[
                        <Button 
                          key="favorite-action"
                          type="text" 
                          icon={<StarFilled style={{ color: '#ffdd59' }} />} 
                          onClick={() => handleFavoriteToggle(item)}
                        />
                      ]}
                    >
                      <div style={{ width: '100%' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
                          <Text strong style={{ color: 'white' }}>{item.code}</Text>
                          <Tag color="#8c7ae6" style={{ borderRadius: '4px', boxShadow: '0 2px 4px rgba(0, 0, 0, 0.2)' }}>{item.type}</Tag>
                        </div>
                        <Text style={{ color: 'rgba(255, 255, 255, 0.85)' }}>{item.description}</Text>
                      </div>
                    </List.Item>
                  )}
                />
              </Card>
            </Col>
          </Row>
        </TabPane>
        
        <TabPane 
          tab={
            <span style={{ color: 'white' }}>
              <BulbOutlined /> AI Suggestions
            </span>
          } 
          key="ai"
          style={{ width: '100%' }}
        >
          <Card 
            style={{ 
              background: 'linear-gradient(135deg, #121212, #1a1a1a)',
              borderRadius: '12px',
              border: '1px solid #333333',
              boxShadow: '0 8px 24px rgba(0, 0, 0, 0.4)',
              marginBottom: '16px',
              margin: 0,
              width: '100%'
            }}
          >
            <Space direction="vertical" size="middle" style={{ width: '100%' }}>
              <div>
                <Title level={4} style={{ color: 'white', margin: 0 }}>AI-Suggested Codes</Title>
                <Paragraph style={{ color: 'rgba(255, 255, 255, 0.85)', marginTop: '8px' }}>
                  Based on the patient&apos;s medical records, symptoms, and history, our AI suggests the following codes:
                </Paragraph>
              </div>
              
              <div style={{ width: '100%', overflowX: 'auto' }}>
                <Table 
                  columns={aiSuggestionColumns} 
                  dataSource={data.aiSuggestions} 
                  rowKey="id"
                  pagination={false}
                  style={{ width: '100%' }}
                />
              </div>
              
              <div style={{ marginTop: '16px' }}>
                <Button type="primary">
                  Generate More Suggestions
                </Button>
              </div>
            </Space>
          </Card>
          
          <Card 
            title={<span style={{ color: 'white' }}>Patient Context</span>}
            style={{ 
              background: 'linear-gradient(135deg, #121212, #1a1a1a)',
              borderRadius: '12px',
              border: '1px solid #333333',
              boxShadow: '0 8px 24px rgba(0, 0, 0, 0.4)',
              margin: 0,
              width: '100%'
            }}
            headStyle={{ borderBottom: '1px solid #333333' }}
          >
            <Paragraph style={{ color: 'rgba(255, 255, 255, 0.85)' }}>
              <Text strong style={{ color: 'white' }}>Patient:</Text> {data.patientContext.name}, {data.patientContext.age}-year-old {data.patientContext.gender}
            </Paragraph>
            <Paragraph style={{ color: 'rgba(255, 255, 255, 0.85)' }}>
              <Text strong style={{ color: 'white' }}>Chief Complaint:</Text> {data.patientContext.complaint}
            </Paragraph>
            <Paragraph style={{ color: 'rgba(255, 255, 255, 0.85)' }}>
              <Text strong style={{ color: 'white' }}>Vitals:</Text> {data.patientContext.vitals}
            </Paragraph>
            <Paragraph style={{ color: 'rgba(255, 255, 255, 0.85)' }}>
              <Text strong style={{ color: 'white' }}>Medical History:</Text> {data.patientContext.history}
            </Paragraph>
            <Paragraph style={{ color: 'rgba(255, 255, 255, 0.85)' }}>
              <Text strong style={{ color: 'white' }}>Medications:</Text> {data.patientContext.medications}
            </Paragraph>
            <Paragraph style={{ color: 'rgba(255, 255, 255, 0.85)' }}>
              <Text strong style={{ color: 'white' }}>Assessment:</Text> {data.patientContext.assessment}
            </Paragraph>
          </Card>
        </TabPane>
      </Tabs>
    </div>
  );
};

export default CodeLookup; 