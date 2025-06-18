import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import Layout from './components/Layout';
import ProtectedRoute from './components/ProtectedRoute';
import { AuthProvider } from './context/AuthContext';
import AuthCallbackSuccess from './pages/AuthCallbackSuccess';
import Dashboard from './pages/Dashboard';
import Login from './pages/Login';
import TutorialEdit from './pages/TutorialEdit';
import TutorialView from './pages/TutorialView';
import Upload from './pages/Upload';

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/auth/callback/success" element={<AuthCallbackSuccess />} />
          <Route path="/" element={<Layout />}>
            <Route index element={<Navigate to="/dashboard" replace />} />
            <Route
              path="dashboard"
              element={
                <ProtectedRoute>
                  <Dashboard />
                </ProtectedRoute>
              }
            />
            <Route
              path="upload"
              element={
                <ProtectedRoute>
                  <Upload />
                </ProtectedRoute>
              }
            />
            <Route
              path="tutorial/:id"
              element={
                <ProtectedRoute>
                  <TutorialView />
                </ProtectedRoute>
              }
            />
            <Route
              path="tutorial/:id/edit"
              element={
                <ProtectedRoute>
                  <TutorialEdit />
                </ProtectedRoute>
              }
            />
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;