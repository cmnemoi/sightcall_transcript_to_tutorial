export interface User {
  id: string;
  name: string;
}

export interface AuthResponse {
  jwt: string;
  user: User;
}

export interface Tutorial {
  id: string;
  title: string;
  content: string;
  user_id: string;
  created_at: string;
  updated_at: string;
}

export interface TutorialListResponse {
  total: number;
  page: number;
  page_size: number;
  items: Tutorial[];
}

export interface TutorialUpdateRequest {
  title?: string;
  content?: string;
}

export interface GenerateTutorialRequest {
  transcript_id: string;
}

export interface TutorialResponse {
  title: string;
  content: string;
}

export interface TranscriptUploadResponse {
  id: string;
}

export interface ApiError {
  error: string;
}