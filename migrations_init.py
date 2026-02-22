"""
Script d'initialisation des migrations de la base de données.
Crée les tables principales pour l'application immobilière.
"""

import os
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
import enum

# Configuration de la base de données
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./real_estate_scraper.db"
)

engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)


# ==================== MODELS ====================

class User(Base):
    """Modèle utilisateur"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    phone = Column(String(20))
    avatar_url = Column(String(500))
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    favorites = relationship("Favorite", back_populates="user", cascade="all, delete-orphan")
    searches = relationship("SavedSearch", back_populates="user", cascade="all, delete-orphan")


class Agency(Base):
    """Modèle agence immobilière"""
    __tablename__ = "agencies"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, index=True)
    email = Column(String(255))
    phone = Column(String(20))
    website = Column(String(500))
    address = Column(String(500))
    postal_code = Column(String(10), index=True)
    city = Column(String(100), index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    logo_url = Column(String(500))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    listings = relationship("Listing", back_populates="agency", cascade="all, delete-orphan")


class Listing(Base):
    """Modèle annonce immobilière"""
    __tablename__ = "listings"
    
    id = Column(Integer, primary_key=True)
    agency_id = Column(Integer, ForeignKey("agencies.id"), nullable=False, index=True)
    title = Column(String(500), nullable=False, index=True)
    description = Column(Text)
    price = Column(Float, nullable=False, index=True)
    property_type = Column(String(50))  # apartment, house, studio, etc.
    bedrooms = Column(Integer)
    bathrooms = Column(Integer)
    area = Column(Float)  # m²
    address = Column(String(500), nullable=False)
    postal_code = Column(String(10), index=True)
    city = Column(String(100), index=True)
    latitude = Column(Float, index=True)
    longitude = Column(Float, index=True)
    image_urls = Column(Text)  # JSON array as string
    source_url = Column(String(500), unique=True)
    source_site = Column(String(100))  # seloger, leboncoin, etc.
    is_available = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    scraped_at = Column(DateTime)
    
    # Relations
    agency = relationship("Agency", back_populates="listings")
    favorites = relationship("Favorite", back_populates="listing", cascade="all, delete-orphan")


class Favorite(Base):
    """Modèle favori utilisateur"""
    __tablename__ = "favorites"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    listing_id = Column(Integer, ForeignKey("listings.id"), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relations
    user = relationship("User", back_populates="favorites")
    listing = relationship("Listing", back_populates="favorites")


class SavedSearch(Base):
    """Modèle recherche sauvegardée"""
    __tablename__ = "saved_searches"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    city = Column(String(100))
    postal_code = Column(String(10))
    min_price = Column(Float)
    max_price = Column(Float)
    min_area = Column(Float)
    max_area = Column(Float)
    property_type = Column(String(50))
    bedrooms = Column(Integer)
    bathrooms = Column(Integer)
    radius_km = Column(Float)  # Rayon de recherche en km
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    user = relationship("User", back_populates="searches")


class ScrapingLog(Base):
    """Modèle log de scraping"""
    __tablename__ = "scraping_logs"
    
    id = Column(Integer, primary_key=True)
    source_site = Column(String(100), nullable=False, index=True)
    status = Column(String(50))  # success, failed, partial
    listings_count = Column(Integer, default=0)
    error_message = Column(Text)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    duration_seconds = Column(Float)


# ==================== INIT ====================

def init_db():
    """Initialiser la base de données"""
    print("🗄️ Création des tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables créées avec succès !")


def seed_sample_data():
    """Ajouter des données d'exemple"""
    session = Session()
    
    # Créer une agence d'exemple
    agency = Agency(
        name="Agence Immobilière Paris",
        email="contact@agence-paris.fr",
        phone="+33 1 23 45 67 89",
        website="https://agence-paris.fr",
        address="123 Rue de la Paix",
        postal_code="75001",
        city="Paris",
        latitude=48.8566,
        longitude=2.3522,
        is_active=True
    )
    session.add(agency)
    session.commit()
    
    # Créer des annonces d'exemple
    listings = [
        Listing(
            agency_id=agency.id,
            title="Appartement 3 pièces à Paris 15e",
            description="Bel appartement spacieux avec vue sur la Seine",
            price=450000,
            property_type="apartment",
            bedrooms=3,
            bathrooms=1,
            area=65,
            address="456 Avenue de la République",
            postal_code="75015",
            city="Paris",
            latitude=48.8450,
            longitude=2.2950,
            source_site="seloger",
            is_available=True
        ),
        Listing(
            agency_id=agency.id,
            title="Maison 4 pièces à Versailles",
            description="Maison moderne avec jardin et garage",
            price=650000,
            property_type="house",
            bedrooms=4,
            bathrooms=2,
            area=120,
            address="789 Rue du Château",
            postal_code="78000",
            city="Versailles",
            latitude=48.8048,
            longitude=2.1301,
            source_site="leboncoin",
            is_available=True
        ),
    ]
    
    for listing in listings:
        session.add(listing)
    
    session.commit()
    print("✅ Données d'exemple ajoutées !")
    session.close()


if __name__ == "__main__":
    init_db()
    seed_sample_data()
    print("\n✅ Base de données initialisée avec succès !")
