from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router
from app.core.config import settings

from app.core.env_validator import validate_environment
import logging

# Configure basic logging for startup
logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Backend API for Local LLM Instrumentation, Tracing and Replay Platform",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    validate_environment()

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins in development
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(api_router)
