"""
Module de monitoring et logging pour l'API Real Estate Scraper.
"""

import logging
import json
from datetime import datetime
from typing import Dict, Any
import os

# Configuration du logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# Créer un logger
logger = logging.getLogger("real_estate_api")
logger.setLevel(getattr(logging, LOG_LEVEL))

# Handler pour console
console_handler = logging.StreamHandler()
console_handler.setLevel(getattr(logging, LOG_LEVEL))

# Format du log
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)


class APIMonitor:
    """Classe pour monitorer les métriques de l'API."""
    
    def __init__(self):
        self.start_time = datetime.utcnow()
        self.request_count = 0
        self.error_count = 0
        self.total_response_time = 0
        
    def log_request(self, method: str, endpoint: str, status_code: int, response_time: float):
        """Enregistrer une requête."""
        self.request_count += 1
        self.total_response_time += response_time
        
        if status_code >= 400:
            self.error_count += 1
        
        logger.info(
            f"Request: {method} {endpoint} | Status: {status_code} | Time: {response_time:.3f}s"
        )
    
    def get_metrics(self) -> Dict[str, Any]:
        """Récupérer les métriques."""
        uptime = (datetime.utcnow() - self.start_time).total_seconds()
        avg_response_time = (
            self.total_response_time / self.request_count 
            if self.request_count > 0 
            else 0
        )
        
        return {
            "environment": ENVIRONMENT,
            "uptime_seconds": uptime,
            "request_count": self.request_count,
            "error_count": self.error_count,
            "error_rate": (
                self.error_count / self.request_count 
                if self.request_count > 0 
                else 0
            ),
            "avg_response_time_ms": avg_response_time * 1000,
            "timestamp": datetime.utcnow().isoformat(),
        }


# Instance globale du monitor
monitor = APIMonitor()


def log_startup():
    """Enregistrer le démarrage de l'API."""
    logger.info(f"Starting Real Estate Scraper API in {ENVIRONMENT} mode")
    logger.info(f"Log level: {LOG_LEVEL}")


def log_error(error: Exception, context: str = ""):
    """Enregistrer une erreur."""
    logger.error(f"Error in {context}: {str(error)}", exc_info=True)


def log_warning(message: str):
    """Enregistrer un avertissement."""
    logger.warning(message)


def log_info(message: str):
    """Enregistrer une information."""
    logger.info(message)
