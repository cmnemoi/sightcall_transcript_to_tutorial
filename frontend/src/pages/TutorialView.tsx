import { AlertCircle, ArrowLeft, Calendar, Edit, Loader2 } from 'lucide-react';
import React, { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { apiService } from '../services/api';
import { Tutorial } from '../types';

const TutorialView: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [tutorial, setTutorial] = useState<Tutorial | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadTutorial = async () => {
      if (!id) return;
      
      try {
        setLoading(true);
        const tutorialData = await apiService.getTutorial(id);
        setTutorial(tutorialData);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load tutorial');
      } finally {
        setLoading(false);
      }
    };

    loadTutorial();
  }, [id]);

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="text-center">
          <Loader2 className="h-8 w-8 animate-spin text-indigo-600 mx-auto mb-4" />
          <p className="text-slate-600">Loading tutorial...</p>
        </div>
      </div>
    );
  }

  if (error || !tutorial) {
    return (
      <div className="bg-white/80 backdrop-blur-md rounded-xl border border-white/20 p-8 shadow-lg text-center">
        <AlertCircle className="h-12 w-12 text-red-500 mx-auto mb-4" />
        <h2 className="text-xl font-semibold text-slate-900 mb-2">Error Loading Tutorial</h2>
        <p className="text-slate-600 mb-6">{error || 'Tutorial not found'}</p>
        <Link
          to="/dashboard"
          className="inline-flex items-center px-6 py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded-xl transition-all duration-200 shadow-lg hover:shadow-xl"
        >
          <ArrowLeft className="h-5 w-5 mr-2" />
          Back to Dashboard
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Header */}
      <div className="bg-white/80 backdrop-blur-md rounded-xl border border-white/20 p-6 shadow-lg">
        <div className="flex items-center justify-between mb-4">
          <Link
            to="/dashboard"
            className="inline-flex items-center text-slate-600 hover:text-slate-900 transition-colors"
          >
            <ArrowLeft className="h-5 w-5 mr-2" />
            Back to Dashboard
          </Link>
          
          <Link
            to={`/tutorial/${id}/edit`}
            className="inline-flex items-center px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded-lg transition-all duration-200 shadow-lg hover:shadow-xl"
          >
            <Edit className="h-4 w-4 mr-2" />
            Edit Tutorial
          </Link>
        </div>
        
        <h1 className="text-3xl font-bold text-slate-900 mb-4">{tutorial.title}</h1>
        
        <div className="flex items-center space-x-6 text-sm text-slate-600">
          <div className="flex items-center space-x-2">
            <Calendar className="h-4 w-4" />
            <span>Created {formatDate(tutorial.created_at)}</span>
          </div>
          {tutorial.updated_at !== tutorial.created_at && (
            <div className="flex items-center space-x-2">
              <Edit className="h-4 w-4" />
              <span>Updated {formatDate(tutorial.updated_at)}</span>
            </div>
          )}
        </div>
      </div>

      {/* Content */}
      <div className="bg-white/80 backdrop-blur-md rounded-xl border border-white/20 p-8 shadow-lg">
        <div className="prose prose-slate max-w-none">
          <div className="whitespace-pre-wrap text-slate-700 leading-relaxed">
            {tutorial.content}
          </div>
        </div>
      </div>
    </div>
  );
};

export default TutorialView;