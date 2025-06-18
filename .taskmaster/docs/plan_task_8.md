# Plan for Task 8: Create Transcript Upload UI with Feature-Based Architecture

## 1. Feature Folder Structure
- Create a new feature folder: `src/features/transcripts/`
  - `components/`
    - `smart/` (container components)
      - `UploadPage.tsx`
      - `UploadForm.tsx`
    - `dumb/` (presentational components)
      - `FileDropzone.tsx`
      - `UploadProgress.tsx`
      - `VideoUrlInput.tsx`
  - `hooks/`
    - `useTranscriptUpload.ts`
    - `useUploadProgress.ts`
  - `api/`
    - `transcripts.ts`
  - `types/`
    - `index.ts`
  - `utils/`
    - `validation.ts`

## 2. Component Breakdown
### Smart Components
- **UploadPage**: Page-level container, handles authentication, layout, and navigation.
- **UploadForm**: Manages form state, validation, and calls upload logic.

### Dumb Components
- **FileDropzone**: Drag-and-drop area for transcript file (uses `react-dropzone`).
- **UploadProgress**: Shows upload/progress bar and status.
- **VideoUrlInput**: Input for video URL, with validation feedback.

## 3. Hooks & Services
- **useTranscriptUpload**: Handles upload logic, API calls, and state (file, video URL, progress, errors, success).
- **useUploadProgress**: (Optional) Manages progress state for uploads.

## 4. API Integration
- **Endpoint**: `POST /transcripts` (multipart/form-data, requires auth)
  - Request: `{ file: <transcript.json>, video_url: <string> }` (if video_url is required, else just file)
  - Response: `201 Created` `{ id: <transcript_id> }` on success
  - Error: `400/401/422` with `{ error: <string> }`
- **API Service**: `src/features/transcripts/api/transcripts.ts`
  - `uploadTranscript(file: File, videoUrl: string): Promise<{ id: string }>`
  - Handle auth (send JWT if required, or rely on cookie)

## 5. Validation
- **File**: Must be valid JSON transcript (check extension, parse JSON, show error if invalid)
- **Video URL**: Must be a valid URL (basic regex or URL constructor)
- **Form**: Prevent submit if invalid, show inline errors
- **Utils**: `src/features/transcripts/utils/validation.ts`

## 6. State Management
- Use React local state/hooks in smart components
- State to manage: file, video URL, validation errors, upload progress, API error/success, redirect
- Reset state on success or navigation

## 7. Styling
- Use Tailwind CSS utility classes for all components
- Follow Tailwind UI file upload patterns for dropzone and progress
- Ensure accessibility (labels, aria attributes)

## 8. Test Strategy (TDD)
- **Unit Tests**
  - Validate file and video URL logic (utils)
  - Test hooks (upload logic, error handling)
  - Test dumb components (render, props, events)
- **Integration Tests**
  - Test UploadForm with mocked API (success, error, progress)
  - Test UploadPage with authentication context
- **Test Doubles**
  - Use handwritten fakes for API and context
- **Coverage**
  - Focus on business logic, validation, and smart components

## 9. Error & Success Handling
- Show clear error messages for validation and API errors
- Show upload progress and disable form during upload
- On success, show confirmation and redirect to tutorial view (e.g., `/tutorials/{id}`)
- Handle auth errors by redirecting to login

---

## Implementation Checklist
- [ ] Create feature folder structure
- [ ] Implement types and API service
- [ ] Write validation utils and tests (TDD)
- [ ] Implement dumb components and tests (TDD)
- [ ] Implement smart components and tests (TDD)
- [ ] Implement hooks and tests (TDD)
- [ ] Integrate API and handle all states
- [ ] Add Tailwind styling and accessibility
- [ ] Test full upload flow (integration)
- [ ] Handle all error/success/redirect cases
- [ ] Update routing to include upload page
- [ ] Review and refactor for clean code and maintainability 