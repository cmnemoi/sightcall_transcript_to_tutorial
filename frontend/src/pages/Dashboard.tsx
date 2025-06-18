import { BookOpen, Calendar, Edit, Eye, Loader2, Plus, Search, Upload } from 'lucide-react';
import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { apiService } from '../services/api';
import { Tutorial } from '../types';

const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const [tutorials, setTutorials] = useState<Tutorial[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalTutorials, setTotalTutorials] = useState(0);

  const loadTutorials = async (page = 1, search = '') => {
    try {
      setLoading(true);
      const response = await apiService.getTutorials({
        page,
        page_size: 6,
        search: search || undefined
      });
      setTutorials(response.items);
      setTotalPages(Math.ceil(response.total / response.page_size));
      setTotalTutorials(response.total);
      setCurrentPage(page);
    } catch (error) {
      console.error('Failed to load tutorials:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadTutorials();
  }, []);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    loadTutorials(1, searchTerm);
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const truncateContent = (content: string, maxLength = 120) => {
    return content.length > maxLength ? content.substring(0, maxLength) + '...' : content;
  };

  const getLatestTutorialDate = (): string => {
    if (tutorials.length === 0) {
      return 'N/A';
    }
    
    const latestTimestamp = Math.max(...tutorials.map(t => new Date(t.created_at).getTime()));
    return formatDate(new Date(latestTimestamp).toISOString());
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="bg-white/80 backdrop-blur-md rounded-2xl border border-white/20 p-8 shadow-lg">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-4 sm:space-y-0">
          <div>
            <h1 className="text-3xl font-bold text-slate-900 mb-2">
              Welcome back, {user?.name}!
            </h1>
            <p className="text-slate-600">
              Manage your AI-generated tutorials and create new ones from SightCall session transcripts
            </p>
          </div>
          <Link
            to="/upload"
            className="inline-flex items-center px-6 py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded-xl transition-all duration-200 shadow-lg hover:shadow-xl group"
          >
            <Plus className="h-5 w-5 mr-2 group-hover:scale-110 transition-transform" />
            New Tutorial
          </Link>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
        <div className="bg-white/80 backdrop-blur-md rounded-xl border border-white/20 p-6 shadow-lg">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-indigo-100 rounded-lg">
              <BookOpen className="h-6 w-6 text-indigo-600" />
            </div>
            <div>
              <p className="text-2xl font-bold text-slate-900">{totalTutorials}</p>
              <p className="text-sm text-slate-600">Total Tutorials</p>
            </div>
          </div>
        </div>
        <div className="bg-white/80 backdrop-blur-md rounded-xl border border-white/20 p-6 shadow-lg">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-emerald-100 rounded-lg">
              <Upload className="h-6 w-6 text-emerald-600" />
            </div>
            <div>
              <p className="text-2xl font-bold text-slate-900">{tutorials.length}</p>
              <p className="text-sm text-slate-600">This Page</p>
            </div>
          </div>
        </div>
        <div className="bg-white/80 backdrop-blur-md rounded-xl border border-white/20 p-6 shadow-lg">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-amber-100 rounded-lg">
              <Calendar className="h-6 w-6 text-amber-600" />
            </div>
            <div>
              <p className="text-2xl font-bold text-slate-900">
                {getLatestTutorialDate()}
              </p>
              <p className="text-sm text-slate-600">Latest</p>
            </div>
          </div>
        </div>
      </div>

      {/* Search */}
      <div className="bg-white/80 backdrop-blur-md rounded-xl border border-white/20 p-6 shadow-lg">
        <form onSubmit={handleSearch} className="flex space-x-4">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-slate-400" />
            <input
              type="text"
              placeholder="Search tutorials..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-3 bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all duration-200"
            />
          </div>
          <button
            type="submit"
            className="px-6 py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded-lg transition-all duration-200 shadow-lg hover:shadow-xl"
          >
            Search
          </button>
        </form>
      </div>

      {/* Tutorials Grid */}
      {loading ? (
        <div className="flex items-center justify-center py-12">
          <div className="text-center">
            <Loader2 className="h-8 w-8 animate-spin text-indigo-600 mx-auto mb-4" />
            <p className="text-slate-600">Loading tutorials...</p>
          </div>
        </div>
      ) : tutorials.length === 0 ? (
        <div className="bg-white/80 backdrop-blur-md rounded-xl border border-white/20 p-12 shadow-lg text-center">
          <BookOpen className="h-12 w-12 text-slate-300 mx-auto mb-4" />
          <h3 className="text-xl font-semibold text-slate-900 mb-2">No tutorials yet</h3>
          <p className="text-slate-600 mb-6">
            {searchTerm ? 'No tutorials found matching your search.' : 'Upload your first SightCall session transcript to generate a tutorial.'}
          </p>
          {!searchTerm && (
            <Link
              to="/upload"
              className="inline-flex items-center px-6 py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded-xl transition-all duration-200 shadow-lg hover:shadow-xl"
            >
              <Upload className="h-5 w-5 mr-2" />
              Upload SightCall Transcript
            </Link>
          )}
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {tutorials.map((tutorial) => (
              <div
                key={tutorial.id}
                className="bg-white/80 backdrop-blur-md rounded-xl border border-white/20 p-6 shadow-lg hover:shadow-xl transition-all duration-200 group"
              >
                <div className="space-y-4">
                  <div>
                    <h3 className="text-lg font-semibold text-slate-900 group-hover:text-indigo-600 transition-colors line-clamp-2">
                      {tutorial.title}
                    </h3>
                    <p className="text-sm text-slate-500 mt-1">
                      {formatDate(tutorial.created_at)}
                    </p>
                  </div>
                  
                  <p className="text-slate-600 text-sm leading-relaxed">
                    {truncateContent(tutorial.content)}
                  </p>
                  
                  <div className="flex items-center justify-between pt-2 border-t border-slate-100">
                    <div className="flex items-center space-x-2">
                      <Link
                        to={`/tutorial/${tutorial.id}`}
                        className="inline-flex items-center px-3 py-1.5 text-sm text-indigo-600 hover:text-indigo-700 hover:bg-indigo-50 rounded-lg transition-all duration-200"
                      >
                        <Eye className="h-4 w-4 mr-1" />
                        View
                      </Link>
                      <Link
                        to={`/tutorial/${tutorial.id}/edit`}
                        className="inline-flex items-center px-3 py-1.5 text-sm text-slate-600 hover:text-slate-700 hover:bg-slate-100 rounded-lg transition-all duration-200"
                      >
                        <Edit className="h-4 w-4 mr-1" />
                        Edit
                      </Link>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Pagination */}
          {totalPages > 1 && (
            <div className="flex items-center justify-center space-x-2">
              <button
                onClick={() => currentPage > 1 && loadTutorials(currentPage - 1, searchTerm)}
                disabled={currentPage === 1}
                className="px-4 py-2 text-sm font-medium text-slate-500 bg-white border border-slate-300 rounded-lg hover:bg-slate-50 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
              >
                Previous
              </button>
              
              <div className="flex items-center space-x-1">
                {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
                  <button
                    key={page}
                    onClick={() => loadTutorials(page, searchTerm)}
                    className={`px-3 py-2 text-sm font-medium rounded-lg transition-all duration-200 ${
                      currentPage === page
                        ? 'bg-indigo-600 text-white'
                        : 'text-slate-500 bg-white border border-slate-300 hover:bg-slate-50'
                    }`}
                  >
                    {page}
                  </button>
                ))}
              </div>
              
              <button
                onClick={() => currentPage < totalPages && loadTutorials(currentPage + 1, searchTerm)}
                disabled={currentPage === totalPages}
                className="px-4 py-2 text-sm font-medium text-slate-500 bg-white border border-slate-300 rounded-lg hover:bg-slate-50 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
              >
                Next
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default Dashboard;