import { AlertCircle, ArrowLeft, Eye, Loader2, Save } from 'lucide-react';
import React, { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { apiService } from '../services/api';
import { Tutorial } from '../types';

const TutorialEdit: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [tutorial, setTutorial] = useState<Tutorial | null>(null);
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [hasChanges, setHasChanges] = useState(false);

  useEffect(() => {
    const loadTutorial = async () => {
      if (!id) return;
      
      try {
        setLoading(true);
        const tutorialData = await apiService.getTutorial(id);
        setTutorial(tutorialData);
        setTitle(tutorialData.title);
        setContent(tutorialData.content);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load tutorial');
      } finally {
        setLoading(false);
      }
    };

    loadTutorial();
  }, [id]);

  useEffect(() => {
    if (tutorial) {
      const titleChanged = title !== tutorial.title;
      const contentChanged = content !== tutorial.content;
      setHasChanges(titleChanged || contentChanged);
    }
  }, [title, content, tutorial]);

  const handleSave = async () => {
    if (!id || !hasChanges) return;

    try {
      setSaving(true);
      setError(null);
      
      const updatedTutorial = await apiService.updateTutorial(id, {
        ...(title !== tutorial?.title && { title }),
        ...(content !== tutorial?.content && { content })
      });
      
      setTutorial(updatedTutorial);
      setHasChanges(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to save tutorial');
    } finally {
      setSaving(false);
    }
  };

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

  if (error && !tutorial) {
    return (
      <div className="bg-white/80 backdrop-blur-md rounded-xl border border-white/20 p-8 shadow-lg text-center">
        <AlertCircle className="h-12 w-12 text-red-500 mx-auto mb-4" />
        <h2 className="text-xl font-semibold text-slate-900 mb-2">Error Loading Tutorial</h2>
        <p className="text-slate-600 mb-6">{error}</p>
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

  if (!tutorial) return null;

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Header */}
      <div className="bg-white/80 backdrop-blur-md rounded-xl border border-white/20 p-6 shadow-lg">
        <div className="flex items-center justify-between mb-4">
          <Link
            to={`/tutorial/${id}`}
            className="inline-flex items-center text-slate-600 hover:text-slate-900 transition-colors"
          >
            <ArrowLeft className="h-5 w-5 mr-2" />
            Back to Tutorial
          </Link>
          
          <div className="flex items-center space-x-3">
            <Link
              to={`/tutorial/${id}`}
              className="inline-flex items-center px-4 py-2 text-slate-600 hover:text-slate-900 hover:bg-slate-100 font-semibold rounded-lg transition-all duration-200"
            >
              <Eye className="h-4 w-4 mr-2" />
              Preview
            </Link>
            
            <button
              onClick={handleSave}
              disabled={!hasChanges || saving}
              className="inline-flex items-center px-6 py-2 bg-indigo-600 hover:bg-indigo-700 disabled:bg-slate-400 text-white font-semibold rounded-lg transition-all duration-200 shadow-lg hover:shadow-xl"
            >
              {saving ? (
                <Loader2 className="h-4 w-4 mr-2 animate-spin" />
              ) : (
                <Save className="h-4 w-4 mr-2" />
              )}
              {saving ? 'Saving...' : 'Save Changes'}
            </button>
          </div>
        </div>
        
        <h1 className="text-2xl font-bold text-slate-900 mb-2">Edit Tutorial</h1>
        <p className="text-sm text-slate-600">
          Last updated {formatDate(tutorial.updated_at)}
        </p>
        
        {hasChanges && (
          <div className="mt-4 p-3 bg-amber-50 border border-amber-200 rounded-lg">
            <p className="text-sm text-amber-800">
              You have unsaved changes. Don't forget to save your work!
            </p>
          </div>
        )}
        
        {error && (
          <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-sm text-red-800">{error}</p>
          </div>
        )}
      </div>

      {/* Edit Form */}
      <div className="bg-white/80 backdrop-blur-md rounded-xl border border-white/20 p-8 shadow-lg space-y-6">
        <div>
          <label htmlFor="title" className="block text-sm font-semibold text-slate-900 mb-2">
            Title
          </label>
          <input
            id="title"
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all duration-200 text-lg font-semibold"
            placeholder="Enter tutorial title..."
          />
        </div>
        
        <div>
          <label htmlFor="content" className="block text-sm font-semibold text-slate-900 mb-2">
            Content
          </label>
          <textarea
            id="content"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            rows={20}
            className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all duration-200 font-mono text-sm leading-relaxed resize-none"
            placeholder="Enter tutorial content..."
          />
        </div>
      </div>
    </div>
  );
};

export default TutorialEdit;