"""
Application FastAPI principale pour le scraping immobilier.
Version robuste pour Heroku avec gestion des erreurs de DB.
"""

import logging
from datetime import datetime
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Créer l'application FastAPI
app = FastAPI(
    title="Real Estate Scraper API",
    description="API pour scraper les annonces immobilières françaises",
    version="1.0.0",
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Importer la DB avec gestion d'erreurs
try:
    from app.database import get_db, init_db
    DB_AVAILABLE = True
except Exception as e:
    logger.warning(f"Database import failed: {e}")
    DB_AVAILABLE = False


# Initialiser la base de données au démarrage
@app.on_event("startup")
async def startup_event():
    """Initialiser la base de données au démarrage."""
    if DB_AVAILABLE:
        try:
            init_db()
            logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
    else:
        logger.warning("Database not available, running in read-only mode")


# Charger les routes avec gestion d'erreurs
try:
    from app.routes import agencies, listings, scraper, auth, user_features, maps
    from app.routes.discovery_scraping import router as discovery_router
    
    app.include_router(agencies.router)
    app.include_router(listings.router)
    app.include_router(scraper.router)
    app.include_router(auth.router)
    app.include_router(user_features.router)
    app.include_router(maps.router)
    app.include_router(discovery_router)
    logger.info("All routes loaded successfully")
except Exception as e:
    logger.warning(f"Some routes failed to load: {e}")


# Endpoints de base
@app.get("/", tags=["health"])
def root():
    """Endpoint racine."""
    return {
        "message": "Real Estate Scraper API",
        "version": "1.0.0",
        "docs": "/docs",
        "database": "available" if DB_AVAILABLE else "unavailable",
    }


@app.get("/health", tags=["health"])
def health_check():
    """Vérifier la santé de l'API."""
    return {
        "status": "healthy",
        "database": "healthy" if DB_AVAILABLE else "unavailable",
        "timestamp": datetime.utcnow().isoformat(),
    }


@app.get("/api/info", tags=["info"])
def get_api_info():
    """Récupérer les informations sur l'API."""
    return {
        "name": "Real Estate Scraper API",
        "version": "1.0.0",
        "description": "API pour scraper les annonces immobilières françaises",
        "endpoints": {
            "agencies": "/api/agencies",
            "listings": "/api/listings",
            "scraper": "/api/scraper",
            "auth": "/api/auth",
            "maps": "/api/maps",
        },
        "documentation": "/docs",
        "database_status": "available" if DB_AVAILABLE else "unavailable",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


# Endpoint de monitoring
@app.get("/api/monitoring/metrics", tags=["monitoring"])
def get_metrics():
    """Récupérer les métriques de l'API."""
    try:
        from monitoring import monitor
        return monitor.get_metrics()
    except Exception as e:
        logger.error(f"Error getting metrics: {e}")
        return {"error": "Unable to get metrics"}


@app.get("/api/monitoring/status", tags=["monitoring"])
def get_monitoring_status():
    """Récupérer le statut du monitoring."""
    return {
        "status": "operational",
        "timestamp": datetime.utcnow().isoformat(),
    }
