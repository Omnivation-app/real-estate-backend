"""
Application FastAPI simplifiée pour tester le déploiement Heroku.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

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


@app.get("/", tags=["health"])
def root():
    """Endpoint racine."""
    return {
        "message": "Real Estate Scraper API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health", tags=["health"])
def health_check():
    """Vérifier la santé de l'API."""
    return {
        "status": "healthy",
        "database": "healthy",
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
        },
        "documentation": "/docs",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
