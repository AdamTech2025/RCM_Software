import { useState } from 'react';
import { Outlet, Link, useLocation, useNavigate } from 'react-router-dom';
import { 
  HomeOutlined, 
  SearchOutlined, 
  FileTextOutlined, 
  DollarOutlined, 
  AuditOutlined, 
  BarChartOutlined, 
  SettingOutlined,
  MenuFoldOutlined,
  MenuUnfoldOutlined,
  LogoutOutlined
} from '@ant-design/icons';
import { Layout, Menu, Button, Tooltip, Modal, message } from 'antd';

const { Header, Sider, Content } = Layout;

const Dashboard = () => {
  const [collapsed, setCollapsed] = useState(false);
  const location = useLocation();
  const navigate = useNavigate();

  const handleLogout = () => {
    Modal.confirm({
      title: 'Confirm Logout',
      content: 'Are you sure you want to logout?',
      okText: 'Logout',
      cancelText: 'Cancel',
      onOk: () => {
        localStorage.removeItem('isAuthenticated');
        message.success({
          content: 'Logged out successfully',
          className: 'custom-message',
          style: {
            marginTop: '20vh',
          },
          duration: 3,
        });
        navigate('/login');
      },
      className: 'custom-modal',
    });
  };

  const menuItems = [
    {
      key: 'dashboard',
      icon: <HomeOutlined />,
      label: 'Dashboard',
      path: '/dashboard'
    },
    {
      key: 'code-lookup',
      icon: <SearchOutlined />,
      label: 'Code Lookup & AI',
      path: '/code-lookup'
    },
    {
      key: 'patient-encounters',
      icon: <FileTextOutlined />,
      label: 'Patient Encounters',
      path: '/patient-encounters'
    },
    {
      key: 'claims',
      icon: <DollarOutlined />,
      label: 'Claims & Billing',
      path: '/claims'
    },
    {
      key: 'audit',
      icon: <AuditOutlined />,
      label: 'Audit & Compliance',
      path: '/audit'
    },
    {
      key: 'analytics',
      icon: <BarChartOutlined />,
      label: 'Analytics & Reports',
      path: '/analytics'
    },
    {
      key: 'settings',
      icon: <SettingOutlined />,
      label: 'Settings',
      path: '/settings'
    },
  ];

  const getSelectedKey = () => {
    const path = location.pathname;
    const item = menuItems.find(item => path.startsWith(item.path));
    return item ? item.key : 'dashboard';
  };

  return (
    <Layout style={{ minHeight: '100vh', margin: 0, padding: 0 }}>
      <Sider 
        trigger={null} 
        collapsible 
        collapsed={collapsed}
        className="sidebar-dark"
        width={250}
        style={{
          overflow: 'auto',
          height: '100vh',
          position: 'fixed',
          left: 0,
          top: 0,
          bottom: 0,
          background: '#000000',
          borderRight: 'none',
          zIndex: 1000
        }}
      >
        <div className="logo-container" style={{ 
          height: '64px', 
          display: 'flex', 
          alignItems: 'center', 
          justifyContent: collapsed ? 'center' : 'flex-start',
          padding: collapsed ? '0' : '0 16px',
          borderBottom: '1px solid #333333',
          marginBottom: '16px',
          background: 'linear-gradient(to right, #121212, #000000)'
        }}>
          {collapsed ? (
            <div className="logo-small" style={{ fontSize: '24px', color: '#fff' }}>RCM</div>
          ) : (
            <div className="logo-full" style={{ fontSize: '20px', color: '#fff', fontWeight: 'bold' }}>
              RCM Dashboard
            </div>
          )}
        </div>
        
        <Menu
          theme="dark"
          mode="inline"
          selectedKeys={[getSelectedKey()]}
          style={{ 
            background: 'transparent',
            borderRight: 'none'
          }}
          items={menuItems.map(item => ({
            key: item.key,
            icon: item.icon,
            label: <Link to={item.path}>{item.label}</Link>,
          }))}
        />
        
        <div style={{ 
          position: 'absolute', 
          bottom: '16px', 
          width: '100%',
          display: 'flex',
          justifyContent: 'center'
        }}>
          <Tooltip title="Logout">
            <Button 
              type="text" 
              icon={<LogoutOutlined />} 
              onClick={handleLogout}
              style={{ 
                color: 'rgba(255, 255, 255, 0.65)',
                fontSize: '16px',
                width: collapsed ? '100%' : 'auto',
                marginLeft: collapsed ? '0' : '16px'
              }}
            >
              {!collapsed && 'Logout'}
            </Button>
          </Tooltip>
        </div>
      </Sider>
      
      <Layout style={{ marginLeft: collapsed ? 80 : 250, transition: 'all 0.2s', padding: 0 }}>
        <Header style={{ 
          padding: 0, 
          background: '#000000',
          borderBottom: '1px solid #333333',
          position: 'sticky',
          top: 0,
          zIndex: 999,
          width: '100%',
          display: 'flex',
          alignItems: 'center',
          boxShadow: '0 4px 12px rgba(0, 0, 0, 0.5)'
        }}>
          <Button
            type="text"
            icon={collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
            onClick={() => setCollapsed(!collapsed)}
            style={{
              fontSize: '16px',
              width: 64,
              height: 64,
              color: 'white'
            }}
          />
          <div style={{ color: 'white', fontSize: '18px', marginLeft: '16px', fontWeight: '500' }}>
            Medical Coding & Billing System
          </div>
        </Header>
        
        <Content style={{
          padding: 0,
          margin: 0,
          background: '#000000',
          borderRadius: 0,
          border: 'none',
          minHeight: 280,
          overflow: 'initial',
          position: 'relative',
          zIndex: 1
        }}>
          <Outlet />
        </Content>
      </Layout>
    </Layout>
  );
};

export default Dashboard; 