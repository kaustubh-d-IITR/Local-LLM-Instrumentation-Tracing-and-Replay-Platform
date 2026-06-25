import os
import logging

logger = logging.getLogger(__name__)

from app.core.config import settings
from app.telemetry.config import telemetry_config

def validate_environment() -> None:
    """
    Validates that required environment variables are present.
    Logs warnings instead of crashing to allow safe fallbacks.
    """
    
    # Either DATABASE_URL (Railway/Render) or constructed URI must be present
    if not settings.DATABASE_URL and settings.POSTGRES_SERVER == "localhost":
        logger.warning("No remote DATABASE_URL provided, falling back to local postgres configuration.")
        
    logger.info("Environment validation complete. Running with current settings.")
