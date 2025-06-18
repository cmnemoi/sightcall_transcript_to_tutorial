Voici la spécification technique extraite et convertie en **Markdown** pour ton usage :

---

# Technical Test — VIE Fullstack Developer

## Goal

Build an AI-powered system that automatically generates step-by-step tutorials based on real-world customer support conversations. These tutorials should summarize the technical troubleshooting performed during the interaction, in a clear and actionable format.

---

## Functional Requirements

### 1. Authentication

* Implement OAuth 2.0 login via GitHub to access the portal.

### 2. Transcript Upload & Processing

* Provide a simple UI to:

  * Upload a conversation transcript file (in JSON format — sample files will be provided).
  * Provide the video recording URL (will be provided too).
  * Trigger processing of the transcript.
* Format of the JSON transcripts is fixed and known (3 sample transcripts will be available in a provided folder). An example is:
```json
{
  "timestamp": "2025-02-26T20:36:06Z",
  "duration_in_ticks": 4216800000,
  "phrases": [
    {
      "offset_milliseconds": 10920,
      "duration_in_ticks": 16800000.0,
      "display": "Hello, thanks for calling in today.",
      "speaker": 1,
      "locale": "en-US",
      "confidence": 0.95266676
    },
    {
      "offset_milliseconds": 12600,
      "duration_in_ticks": 8800000.0,
      "display": "How can I help you?",
      "speaker": 1,
      "locale": "en-US",
      "confidence": 0.9780294
    },
    ...
  ]
}
```

### 3. Tutorial Generation

* Use OpenAI SDK to:

  * Extract relevant steps from the transcript.
  * Generate a clear step-by-step tutorial summarizing how the issue was resolved or handled.
  * Include steps only when meaningful (avoid trivial dialogue).
  * Sub-video clip related to it.

### 4. Database Integration

* Store each tutorial in a database with:

  * Associated transcript
  * Creation date
  * GitHub user who uploaded it

### 5. Tutorial Editing

* Enable the logged-in user to:

  * View their previously generated tutorials
  * Edit the tutorial text
  * Save the updated version

---

## 🛠 Technical Requirements

### Backend

* Use FastAPI with a local DB.
* Expose a proper REST API for:

  * Uploading transcripts
  * Triggering processing
  * Fetching and editing tutorials

### Frontend

* Use **React** to:

  * Authenticate with GitHub
  * Upload files/provided URL recording
  * Display tutorial list and individual tutorials
  * Allow tutorial editing
