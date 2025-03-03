import {
  BrowserRouter as Router,
  Route,
  Routes,
  Outlet,
  Navigate,
} from "react-router-dom";
// import Projects from './page/Projects.jsx';
import Login from "./components/auth/Login";
import Register from "./components/auth/Register";
import ForgotPassword from "./components/auth/ForgotPassword";
import Dashboard from "./pages/Dashboard";
import DashboardHome from "./pages/DashboardHome";
import CodeLookup from "./pages/CodeLookup";
import PropTypes from 'prop-types';

// Protected Route wrapper component
const ProtectedRoute = ({ children }) => {
  // Add your authentication logic here
  const isAuthenticated = localStorage.getItem("isAuthenticated") === "true";
  return isAuthenticated ? children : <Navigate to="/login" />;
};

ProtectedRoute.propTypes = {
  children: PropTypes.node.isRequired,
};

const AuthLayout = () => (
  <Outlet />
);

const App = () => {
  return (
    <Router>
      <Routes>
        {/* Auth routes */}
        <Route path="/" element={<AuthLayout />}>
          <Route index element={<Navigate to="/login" />} />
          <Route path="login" element={<Login />} />
          <Route path="register" element={<Register />} />
          <Route path="forgot-password" element={<ForgotPassword />} />
        </Route>

        {/* Protected routes */}
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        >
          <Route path="dashboard" element={<DashboardHome />} />
          <Route path="code-lookup" element={<CodeLookup />} />
          <Route path="patient-encounters" element={<div style={{ color: 'white' }}>Patient Encounters Page (Coming Soon)</div>} />
          <Route path="claims" element={<div style={{ color: 'white' }}>Claims & Billing Page (Coming Soon)</div>} />
          <Route path="audit" element={<div style={{ color: 'white' }}>Audit & Compliance Page (Coming Soon)</div>} />
          <Route path="analytics" element={<div style={{ color: 'white' }}>Analytics & Reports Page (Coming Soon)</div>} />
          <Route path="settings" element={<div style={{ color: 'white' }}>Settings Page (Coming Soon)</div>} />
          <Route index element={<Navigate to="/dashboard" />} />
        </Route>
      </Routes>
    </Router>
  );
};

export default App;
