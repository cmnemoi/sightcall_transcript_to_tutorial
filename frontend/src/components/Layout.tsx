import { BookOpen, LogOut, Upload, User } from 'lucide-react';
import React from 'react';
import { Link, Outlet, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Layout: React.FC = () => {
  const { user, logout } = useAuth();
  const location = useLocation();

  const isActive = (path: string) => location.pathname === path;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      <nav className="bg-white/80 backdrop-blur-md border-b border-slate-200/50 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <Link to="/" className="flex items-center space-x-2 group">
              <BookOpen className="h-8 w-8 text-indigo-600 group-hover:text-indigo-700 transition-colors" />
              <span className="text-xl font-bold text-slate-900">SightCall Tutorials</span>
            </Link>
            
            {user && (
              <div className="flex items-center space-x-6">
                <Link
                  to="/dashboard"
                  className={`px-4 py-2 rounded-lg transition-all duration-200 ${
                    isActive('/dashboard')
                      ? 'bg-indigo-100 text-indigo-700'
                      : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
                  }`}
                >
                  Dashboard
                </Link>
                <Link
                  to="/upload"
                  className={`px-4 py-2 rounded-lg transition-all duration-200 flex items-center space-x-2 ${
                    isActive('/upload')
                      ? 'bg-indigo-100 text-indigo-700'
                      : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
                  }`}
                >
                  <Upload className="h-4 w-4" />
                  <span>Upload</span>
                </Link>
                
                <div className="flex items-center space-x-3 border-l border-slate-200 pl-6">
                  <div className="flex items-center space-x-2">
                    <User className="h-5 w-5 text-slate-500" />
                    <span className="text-sm font-medium text-slate-700">{user.name}</span>
                  </div>
                  <button
                    onClick={logout}
                    className="p-2 text-slate-500 hover:text-slate-700 hover:bg-slate-100 rounded-lg transition-all duration-200"
                    title="Logout"
                  >
                    <LogOut className="h-4 w-4" />
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </nav>
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Outlet />
      </main>
    </div>
  );
};

export default Layout;