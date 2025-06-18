import { BookOpen, Github, Sparkles } from 'lucide-react';
import React, { useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { apiService } from '../services/api';

const Login: React.FC = () => {
  const { login, user } = useAuth();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  useEffect(() => {
    const handleCallback = async () => {
      const code = searchParams.get('code');
      if (code) {
        try {
          await apiService.handleGitHubCallback(code);
          // The AuthContext will handle setting the user state via getCurrentUser
          navigate('/dashboard');
        } catch (error) {
          console.error('Auth callback error:', error);
        }
      }
    };

    handleCallback();
  }, [searchParams, navigate]);

  useEffect(() => {
    if (user) {
      navigate('/dashboard');
    }
  }, [user, navigate]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 flex items-center justify-center px-4">
      <div className="max-w-md w-full">
        <div className="bg-white/80 backdrop-blur-md rounded-2xl shadow-xl border border-white/20 p-8">
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-indigo-100 rounded-2xl mb-4">
              <BookOpen className="h-8 w-8 text-indigo-600" />
            </div>
            <h1 className="text-3xl font-bold text-slate-900 mb-2">SightCall</h1>
            <p className="text-slate-600 leading-relaxed">
              Transform SightCall video support sessions into step-by-step tutorials with AI
            </p>
          </div>

          <div className="space-y-6">
            <div className="bg-gradient-to-r from-indigo-50 to-blue-50 rounded-xl p-4 border border-indigo-100">
              <div className="flex items-center space-x-3 mb-3">
                <Sparkles className="h-5 w-5 text-indigo-600" />
                <span className="font-semibold text-slate-900">AI-Powered</span>
              </div>
              <ul className="text-sm text-slate-600 space-y-1">
                <li>• Upload SightCall session transcripts</li>
                <li>• Generate step-by-step tutorials</li>
                <li>• Edit and manage your tutorials</li>
              </ul>
            </div>

            <button
              onClick={login}
              className="w-full bg-slate-900 hover:bg-slate-800 text-white font-semibold py-3 px-6 rounded-xl transition-all duration-200 flex items-center justify-center space-x-3 group shadow-lg hover:shadow-xl cursor-pointer"
            >
              <Github className="h-5 w-5 group-hover:scale-110 transition-transform" />
              <span>Continue with GitHub</span>
            </button>

            <p className="text-xs text-slate-500 text-center leading-relaxed">
              By continuing, you agree to our Terms of Service and Privacy Policy
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;