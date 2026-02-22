"""
Routes FastAPI pour le monitoring et les métriques.
"""

from fastapi import APIRouter
from datetime import datetime
from monitoring import monitor, logger

router = APIRouter(prefix="/api/monitoring", tags=["monitoring"])


@router.get("/metrics")
def get_metrics():
    """
    Récupérer les métriques de l'API.
    
    Returns:
        Dict avec les métriques de performance et d'utilisation
    """
    return monitor.get_metrics()


@router.get("/status")
def get_status():
    """
    Récupérer le statut de l'API.
    
    Returns:
        Dict avec le statut actuel de l'API
    """
    return {
        "status": "running",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
    }


@router.get("/health/detailed")
def get_detailed_health():
    """
    Récupérer le statut de santé détaillé de l'API.
    
    Returns:
        Dict avec les détails de santé de l'API
    """
    metrics = monitor.get_metrics()
    
    return {
        "status": "healthy",
        "metrics": metrics,
        "components": {
            "api": "operational",
            "database": "checking",
            "cache": "operational",
        },
        "timestamp": datetime.utcnow().isoformat(),
    }
