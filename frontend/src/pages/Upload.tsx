import { AlertCircle, CheckCircle, FileText, Loader2, Sparkles, Upload as UploadIcon } from 'lucide-react';
import React, { useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiService } from '../services/api';

const Upload: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [uploadStatus, setUploadStatus] = useState<'idle' | 'uploading' | 'generating' | 'success' | 'error'>('idle');
  const [error, setError] = useState<string | null>(null);
  const [dragActive, setDragActive] = useState(false);
  const [generatedTutorial, setGeneratedTutorial] = useState<{ title: string; content: string } | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const navigate = useNavigate();

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setDragActive(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setDragActive(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragActive(false);
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile) {
      handleFileSelect(droppedFile);
    }
  };

  const handleFileSelect = (selectedFile: File) => {
    if (selectedFile.type !== 'application/json') {
      setError('Please select a JSON file');
      return;
    }
    setFile(selectedFile);
    setError(null);
    setGeneratedTutorial(null);
  };

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      handleFileSelect(selectedFile);
    }
  };

  const handleUploadAndGenerate = async () => {
    if (!file) return;

    try {
      setUploadStatus('uploading');
      setError(null);

      // Upload transcript
      const uploadResponse = await apiService.uploadTranscript(file);
      
      setUploadStatus('generating');
      
      // Generate tutorial
      const tutorialResponse = await apiService.generateTutorial({
        transcript_id: uploadResponse.id
      });

      setGeneratedTutorial(tutorialResponse);
      setUploadStatus('success');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
      setUploadStatus('error');
    }
  };

  const getStatusIcon = () => {
    switch (uploadStatus) {
      case 'uploading':
      case 'generating':
        return <Loader2 className="h-6 w-6 animate-spin text-indigo-600" />;
      case 'success':
        return <CheckCircle className="h-6 w-6 text-emerald-600" />;
      case 'error':
        return <AlertCircle className="h-6 w-6 text-red-600" />;
      default:
        return <UploadIcon className="h-6 w-6 text-slate-400" />;
    }
  };

  const getStatusMessage = () => {
    switch (uploadStatus) {
      case 'uploading':
        return 'Uploading transcript...';
      case 'generating':
        return 'Generating tutorial with AI...';
      case 'success':
        return 'Tutorial generated successfully!';
      case 'error':
        return error || 'An error occurred';
      default:
        return 'Ready to upload';
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-3xl font-bold text-slate-900 mb-4">Upload SightCall Transcript</h1>
        <p className="text-slate-600 leading-relaxed">
          Upload a SightCall session transcript and let AI generate a step-by-step tutorial
        </p>
      </div>

      {/* Upload Section */}
      <div className="bg-white/80 backdrop-blur-md rounded-2xl border border-white/20 p-8 shadow-lg">
        <div
          className={`border-2 border-dashed rounded-xl p-12 text-center transition-all duration-200 ${
            dragActive
              ? 'border-indigo-400 bg-indigo-50'
              : file
              ? 'border-emerald-400 bg-emerald-50'
              : 'border-slate-300 hover:border-slate-400 hover:bg-slate-50'
          }`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
        >
          <input
            ref={fileInputRef}
            type="file"
            accept=".json"
            onChange={handleFileInput}
            className="hidden"
          />
          
          <div className="space-y-4">
            {file ? (
              <div className="flex items-center justify-center space-x-3">
                <FileText className="h-8 w-8 text-emerald-600" />
                <div className="text-left">
                  <p className="font-semibold text-slate-900">{file.name}</p>
                  <p className="text-sm text-slate-500">
                    {(file.size / 1024).toFixed(1)} KB
                  </p>
                </div>
              </div>
            ) : (
              <>
                <UploadIcon className="h-12 w-12 text-slate-400 mx-auto" />
                <div>
                  <p className="text-lg font-semibold text-slate-900 mb-2">
                    Drop your SightCall transcript here
                  </p>
                  <p className="text-slate-600">
                    or{' '}
                    <button
                      onClick={() => fileInputRef.current?.click()}
                      className="text-indigo-600 hover:text-indigo-700 font-semibold underline"
                    >
                      browse files
                    </button>
                  </p>
                </div>
                <p className="text-sm text-slate-500">
                  Supports SightCall JSON transcript files up to 10MB
                </p>
              </>
            )}
          </div>
        </div>

        {file && (
          <div className="mt-6 flex items-center justify-between">
            <button
              onClick={() => {
                setFile(null);
                setError(null);
                setGeneratedTutorial(null);
                setUploadStatus('idle');
                if (fileInputRef.current) {
                  fileInputRef.current.value = '';
                }
              }}
              className="text-slate-600 hover:text-slate-700 font-medium"
            >
              Choose different file
            </button>
            
            <button
              onClick={handleUploadAndGenerate}
              disabled={uploadStatus === 'uploading' || uploadStatus === 'generating'}
              className="inline-flex items-center px-8 py-3 bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-400 text-white font-semibold rounded-xl transition-all duration-200 shadow-lg hover:shadow-xl group"
            >
              <Sparkles className="h-5 w-5 mr-2 group-hover:scale-110 transition-transform" />
              Generate Tutorial
            </button>
          </div>
        )}
      </div>

      {/* Status Section */}
      {uploadStatus !== 'idle' && (
        <div className="bg-white/80 backdrop-blur-md rounded-xl border border-white/20 p-6 shadow-lg">
          <div className="flex items-center space-x-3">
            {getStatusIcon()}
            <div>
              <p className="font-semibold text-slate-900">{getStatusMessage()}</p>
              {uploadStatus === 'generating' && (
                <p className="text-sm text-slate-600 mt-1">
                  This may take a few moments while AI processes your SightCall transcript
                </p>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Generated Tutorial Preview */}
      {generatedTutorial && (
        <div className="bg-white/80 backdrop-blur-md rounded-xl border border-white/20 p-8 shadow-lg">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-slate-900">Generated Tutorial</h2>
            <button
              onClick={() => navigate('/dashboard')}
              className="px-6 py-2 bg-emerald-600 hover:bg-emerald-700 text-white font-semibold rounded-lg transition-all duration-200 shadow-lg hover:shadow-xl"
            >
              View in Dashboard
            </button>
          </div>
          
          <div className="space-y-4">
            <div>
              <h3 className="text-xl font-semibold text-slate-900 mb-2">
                {generatedTutorial.title}
              </h3>
            </div>
            
            <div className="prose prose-slate max-w-none">
              <div className="bg-slate-50 rounded-lg p-6 border border-slate-200">
                <pre className="whitespace-pre-wrap text-sm text-slate-700 font-sans">
                  {generatedTutorial.content}
                </pre>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Upload;