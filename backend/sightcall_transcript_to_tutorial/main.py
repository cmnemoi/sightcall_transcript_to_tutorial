from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sightcall_transcript_to_tutorial import __version__
from sightcall_transcript_to_tutorial.presentation.api.middlewares.jwt_middleware import JWTMiddleware
from sightcall_transcript_to_tutorial.presentation.api.routers import auth, tutorial
from sightcall_transcript_to_tutorial.presentation.api.routers.transcripts import router as transcripts_router

app = FastAPI(
    title="Sightcall Transcript to Tutorial API",
    description="An API that converts a Sightcall transcripts to tutorials",
    version=__version__,
    license_info={
        "name": "AGPL-3.0-or-later",
        "url": "https://www.gnu.org/licenses/agpl-3.0.en.html",
    },
)

# Add CORS middleware to allow requests from localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add JWT middleware (protects protected routes)
app.add_middleware(JWTMiddleware)

app.include_router(auth.router)
app.include_router(tutorial.router)
app.include_router(transcripts_router)


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
