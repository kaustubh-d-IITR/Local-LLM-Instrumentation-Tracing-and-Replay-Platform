import os
import logging

logger = logging.getLogger(__name__)

def validate_environment() -> None:
    """
    Validates that required environment variables are present.
    Logs warnings instead of crashing to allow safe fallbacks.
    """
    required_vars = [
        "SQLALCHEMY_DATABASE_URI"
    ]
    
    optional_vars = {
        "ENABLE_LATENCY": "True",
        "ENABLE_ACTIVATIONS": "True",
        "ENABLE_ANOMALIES": "True",
        "MAX_ACTIVATION_THRESHOLD": "50.0",
        "MAX_LATENCY_THRESHOLD_MS": "100.0",
        "MEMORY_WARNING_THRESHOLD_PERCENT": "90.0",
        "TELEMETRY_SAMPLE_RATE": "1.0",
        "HF_HOME": "/root/.cache/huggingface"
    }

    missing_required = []
    for var in required_vars:
        if not os.getenv(var):
            missing_required.append(var)
            
    if missing_required:
        logger.error(f"CRITICAL: Missing required environment variables: {', '.join(missing_required)}")
        logger.error("The application may fail to start or connect to the database.")

    missing_optional = []
    for var, default in optional_vars.items():
        if not os.getenv(var):
            missing_optional.append((var, default))
            
    if missing_optional:
        logger.warning("Missing optional environment variables. Using safe defaults:")
        for var, default in missing_optional:
            logger.warning(f"  {var} = {default}")

    logger.info("Environment validation complete.")
