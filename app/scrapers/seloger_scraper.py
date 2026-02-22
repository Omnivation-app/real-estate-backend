"""
Scraper pour SeLoger.com
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class SeLogerScraper:
    """Scraper pour SeLoger"""
    
    BASE_URL = "https://www.seloger.com"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def search(self, city: str, min_price: int = None, max_price: int = None) -> List[Dict]:
        """
        Rechercher des annonces sur SeLoger
        
        Args:
            city: Ville à rechercher
            min_price: Prix minimum
            max_price: Prix maximum
            
        Returns:
            Liste des annonces trouvées
        """
        listings = []
        
        try:
            # Construire l'URL de recherche
            url = f"{self.BASE_URL}/recherche/result"
            params = {
                'ci': city,
                'tri': 'prix',
            }
            
            if min_price:
                params['pxmin'] = min_price
            if max_price:
                params['pxmax'] = max_price
            
            logger.info(f"Scraping SeLoger pour {city}...")
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Chercher les annonces (structure simplifiée pour la démo)
            # En production, adapter le sélecteur CSS selon la structure actuelle
            listings_elements = soup.find_all('div', class_='annonce')
            
            for element in listings_elements[:10]:  # Limiter à 10 résultats
                try:
                    listing = self._parse_listing(element)
                    if listing:
                        listings.append(listing)
                except Exception as e:
                    logger.warning(f"Erreur lors du parsing d'une annonce: {e}")
                    continue
            
            logger.info(f"✅ {len(listings)} annonces trouvées sur SeLoger")
            
        except Exception as e:
            logger.error(f"❌ Erreur lors du scraping SeLoger: {e}")
        
        return listings
    
    def _parse_listing(self, element) -> Dict:
        """Parser une annonce"""
        try:
            title = element.find('h2').text.strip()
            price_text = element.find('span', class_='prix').text.strip()
            price = int(''.join(filter(str.isdigit, price_text)))
            
            location = element.find('span', class_='localite').text.strip()
            
            # Extraire les caractéristiques
            features = element.find_all('span', class_='caracteristique')
            bedrooms = 0
            area = 0
            
            for feature in features:
                text = feature.text.lower()
                if 'chambre' in text:
                    bedrooms = int(''.join(filter(str.isdigit, text)))
                elif 'm²' in text:
                    area = int(''.join(filter(str.isdigit, text)))
            
            return {
                'title': title,
                'price': price,
                'location': location,
                'bedrooms': bedrooms,
                'area': area,
                'source_site': 'seloger',
                'scraped_at': datetime.utcnow(),
            }
        except Exception as e:
            logger.warning(f"Erreur parsing listing: {e}")
            return None


class LeBonCoinScraper:
    """Scraper pour LeBonCoin"""
    
    BASE_URL = "https://www.leboncoin.fr"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def search(self, city: str, min_price: int = None, max_price: int = None) -> List[Dict]:
        """
        Rechercher des annonces sur LeBonCoin
        """
        listings = []
        
        try:
            # Construire l'URL de recherche
            url = f"{self.BASE_URL}/recherche"
            params = {
                'category': '9',  # Immobilier
                'location': city,
                'th': 1,  # Tri par prix
            }
            
            if min_price:
                params['minprice'] = min_price
            if max_price:
                params['maxprice'] = max_price
            
            logger.info(f"Scraping LeBonCoin pour {city}...")
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Chercher les annonces
            listings_elements = soup.find_all('div', class_='item')
            
            for element in listings_elements[:10]:
                try:
                    listing = self._parse_listing(element)
                    if listing:
                        listings.append(listing)
                except Exception as e:
                    logger.warning(f"Erreur lors du parsing d'une annonce: {e}")
                    continue
            
            logger.info(f"✅ {len(listings)} annonces trouvées sur LeBonCoin")
            
        except Exception as e:
            logger.error(f"❌ Erreur lors du scraping LeBonCoin: {e}")
        
        return listings
    
    def _parse_listing(self, element) -> Dict:
        """Parser une annonce"""
        try:
            title = element.find('h2').text.strip()
            price_text = element.find('span', class_='price').text.strip()
            price = int(''.join(filter(str.isdigit, price_text)))
            
            location = element.find('span', class_='location').text.strip()
            
            return {
                'title': title,
                'price': price,
                'location': location,
                'source_site': 'leboncoin',
                'scraped_at': datetime.utcnow(),
            }
        except Exception as e:
            logger.warning(f"Erreur parsing listing: {e}")
            return None


def scrape_all_sites(city: str, min_price: int = None, max_price: int = None) -> List[Dict]:
    """
    Scraper tous les sites immobiliers
    """
    all_listings = []
    
    # SeLoger
    seloger = SeLogerScraper()
    all_listings.extend(seloger.search(city, min_price, max_price))
    
    # LeBonCoin
    leboncoin = LeBonCoinScraper()
    all_listings.extend(leboncoin.search(city, min_price, max_price))
    
    return all_listings
