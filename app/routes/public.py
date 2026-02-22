"""
Routes publiques simplifiées pour le frontend
"""

from fastapi import APIRouter, Query
from datetime import datetime

router = APIRouter(prefix="/api", tags=["public"])


@router.get("/listings")
def get_all_listings(limit: int = Query(10, ge=1, le=100)):
    """
    Récupérer toutes les annonces (version simplifiée)
    """
    return [
        {
            "id": 1,
            "title": "Appartement 3 pièces à Paris 15e",
            "price": 450000,
            "location": "Paris 15e",
            "bedrooms": 3,
            "bathrooms": 1,
            "area": 65,
            "image": "https://via.placeholder.com/300x200?text=Apt+1",
            "agency": "Agence Immobilière Paris",
            "posted_date": "2026-02-20",
        },
        {
            "id": 2,
            "title": "Maison 4 pièces à Versailles",
            "price": 650000,
            "location": "Versailles",
            "bedrooms": 4,
            "bathrooms": 2,
            "area": 120,
            "image": "https://via.placeholder.com/300x200?text=Maison+1",
            "agency": "Agence Versailles",
            "posted_date": "2026-02-21",
        },
        {
            "id": 3,
            "title": "Studio à Lyon",
            "price": 200000,
            "location": "Lyon",
            "bedrooms": 1,
            "bathrooms": 1,
            "area": 35,
            "image": "https://via.placeholder.com/300x200?text=Studio+1",
            "agency": "Agence Lyon",
            "posted_date": "2026-02-22",
        },
    ][:limit]


@router.get("/agencies")
def get_all_agencies(limit: int = Query(10, ge=1, le=100)):
    """
    Récupérer toutes les agences (version simplifiée)
    """
    return [
        {
            "id": 1,
            "name": "Agence Immobilière Paris",
            "email": "contact@agence-paris.fr",
            "phone": "+33 1 23 45 67 89",
            "city": "Paris",
            "postal_code": "75015",
            "website": "https://agence-paris.fr",
        },
        {
            "id": 2,
            "name": "Agence Versailles",
            "email": "contact@agence-versailles.fr",
            "phone": "+33 1 98 76 54 32",
            "city": "Versailles",
            "postal_code": "78000",
            "website": "https://agence-versailles.fr",
        },
        {
            "id": 3,
            "name": "Agence Lyon",
            "email": "contact@agence-lyon.fr",
            "phone": "+33 4 12 34 56 78",
            "city": "Lyon",
            "postal_code": "69000",
            "website": "https://agence-lyon.fr",
        },
    ][:limit]


@router.get("/search")
def search_listings(
    city: str = Query(None),
    min_price: int = Query(None),
    max_price: int = Query(None),
    bedrooms: int = Query(None),
):
    """
    Rechercher des annonces avec filtres simples
    """
    all_listings = [
        {
            "id": 1,
            "title": "Appartement 3 pièces à Paris 15e",
            "price": 450000,
            "location": "Paris 15e",
            "bedrooms": 3,
            "bathrooms": 1,
            "area": 65,
            "city": "Paris",
        },
        {
            "id": 2,
            "title": "Maison 4 pièces à Versailles",
            "price": 650000,
            "location": "Versailles",
            "bedrooms": 4,
            "bathrooms": 2,
            "area": 120,
            "city": "Versailles",
        },
        {
            "id": 3,
            "title": "Studio à Lyon",
            "price": 200000,
            "location": "Lyon",
            "bedrooms": 1,
            "bathrooms": 1,
            "area": 35,
            "city": "Lyon",
        },
    ]
    
    # Filtrer
    results = all_listings
    
    if city:
        results = [l for l in results if city.lower() in l["city"].lower()]
    
    if min_price:
        results = [l for l in results if l["price"] >= min_price]
    
    if max_price:
        results = [l for l in results if l["price"] <= max_price]
    
    if bedrooms:
        results = [l for l in results if l["bedrooms"] >= bedrooms]
    
    return {
        "count": len(results),
        "listings": results,
        "filters": {
            "city": city,
            "min_price": min_price,
            "max_price": max_price,
            "bedrooms": bedrooms,
        }
    }


@router.get("/favorites")
def get_favorites():
    """
    Récupérer les favoris de l'utilisateur
    """
    return {
        "count": 1,
        "favorites": [
            {
                "id": 1,
                "title": "Appartement 3 pièces à Paris 15e",
                "price": 450000,
                "location": "Paris 15e",
                "added_date": "2026-02-20",
            }
        ]
    }


@router.post("/favorites/{listing_id}")
def add_favorite(listing_id: int):
    """
    Ajouter une annonce aux favoris
    """
    return {
        "status": "success",
        "message": f"Annonce {listing_id} ajoutée aux favoris",
        "timestamp": datetime.utcnow().isoformat(),
    }


@router.delete("/favorites/{listing_id}")
def remove_favorite(listing_id: int):
    """
    Retirer une annonce des favoris
    """
    return {
        "status": "success",
        "message": f"Annonce {listing_id} retirée des favoris",
        "timestamp": datetime.utcnow().isoformat(),
    }
