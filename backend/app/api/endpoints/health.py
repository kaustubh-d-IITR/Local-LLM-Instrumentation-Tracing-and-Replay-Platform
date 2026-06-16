from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import get_db

router = APIRouter()

@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint for Docker and external monitors.
    Returns the status of the API and Database connection.
    """
    db_status = "disconnected"
    try:
        # Simple query to verify DB is reachable
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
        
    return {
        "status": "ok" if db_status == "connected" else "degraded",
        "database": db_status,
        "websocket_manager": "active",  # Assuming it boots automatically via main.py
        "models_loaded": 0 # Tracked by SessionManager, static here for MVP health
    }
