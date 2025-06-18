import React, { createContext, ReactNode, useContext, useEffect, useState } from 'react';
import { apiService } from '../services/api';
import { User } from '../types';

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  login: () => void;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const initAuth = async () => {
      try {
        const currentUser = await apiService.getCurrentUser();
        setUser(currentUser);
      } catch {
        setUser(null);
      }
      setIsLoading(false);
    };

    initAuth();
  }, []);

  const login = async () => {
    try {
      const response = await fetch('http://localhost:8000/auth/github/login');
      const data = await response.json();
      if (data.login_url) {
        window.location.href = data.login_url;
      } else {
        throw new Error('No login_url returned from backend');
      }
    } catch (error) {
      console.error('Failed to initiate GitHub login:', error);
    }
  };

  const logout = async () => {
    try {
      await apiService.logout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      setUser(null);
    }
  };

  return (
    <AuthContext.Provider value={{ user, isLoading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};