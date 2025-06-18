import {
  AuthResponse,
  GenerateTutorialRequest,
  TranscriptUploadResponse,
  Tutorial,
  TutorialListResponse,
  TutorialResponse,
  TutorialUpdateRequest,
  User
} from '../types';

const API_BASE_URL = 'http://localhost:8000';

class ApiService {
  private async handleResponse<T>(response: Response): Promise<T> {
    if (!response.ok) {
      const error = await response.json().catch(() => ({ error: 'Network error' }));
      throw new Error(error.error || `HTTP ${response.status}`);
    }
    return response.json();
  }

  // Auth endpoints
  async initiateGitHubLogin(): Promise<void> {
    window.location.href = `${API_BASE_URL}/auth/github/login`;
  }

  async handleGitHubCallback(code: string): Promise<AuthResponse> {
    const response = await fetch(`${API_BASE_URL}/auth/github/callback?code=${code}`, {
      credentials: 'include',
    });
    return this.handleResponse<AuthResponse>(response);
  }

  async getCurrentUser(): Promise<User> {
    const response = await fetch(`${API_BASE_URL}/auth/github/me`, {
      credentials: 'include',
    });
    return this.handleResponse<User>(response);
  }

  async logout(): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/auth/github/logout`, {
      method: 'POST',
      credentials: 'include',
    });
    await this.handleResponse(response);
  }

  // Transcript endpoints
  async uploadTranscript(file: File): Promise<TranscriptUploadResponse> {
    const formData = new FormData();
    formData.append('file', file);
    const response = await fetch(`${API_BASE_URL}/transcripts`, {
      method: 'POST',
      credentials: 'include',
      body: formData
    });
    return this.handleResponse<TranscriptUploadResponse>(response);
  }

  // Tutorial endpoints
  async generateTutorial(request: GenerateTutorialRequest): Promise<TutorialResponse> {
    const response = await fetch(`${API_BASE_URL}/tutorials/generate`, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request)
    });
    return this.handleResponse<TutorialResponse>(response);
  }

  async getTutorials(params?: {
    page?: number;
    page_size?: number;
    search?: string;
    created_from?: string;
    created_to?: string;
  }): Promise<TutorialListResponse> {
    const queryParams = new URLSearchParams();
    if (params?.page) queryParams.append('page', params.page.toString());
    if (params?.page_size) queryParams.append('page_size', params.page_size.toString());
    if (params?.search) queryParams.append('search', params.search);
    if (params?.created_from) queryParams.append('created_from', params.created_from);
    if (params?.created_to) queryParams.append('created_to', params.created_to);

    const response = await fetch(`${API_BASE_URL}/tutorials?${queryParams}`, {
      credentials: 'include',
    });
    return this.handleResponse<TutorialListResponse>(response);
  }

  async getTutorial(id: string): Promise<Tutorial> {
    const response = await fetch(`${API_BASE_URL}/tutorials/${id}`, {
      credentials: 'include',
    });
    return this.handleResponse<Tutorial>(response);
  }

  async updateTutorial(id: string, update: TutorialUpdateRequest): Promise<Tutorial> {
    const response = await fetch(`${API_BASE_URL}/tutorials/${id}`, {
      method: 'PATCH',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(update)
    });
    return this.handleResponse<Tutorial>(response);
  }
}

export const apiService = new ApiService();