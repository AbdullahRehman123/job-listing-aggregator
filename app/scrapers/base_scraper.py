import requests
from bs4 import BeautifulSoup
import time
from typing import List
from models.job import Job

class BaseScraper:
    """Base class for all scrapers"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.delay = 2  # Seconds between requests
    
    def fetch_page(self, url: str) -> BeautifulSoup:
        """Fetch and parse a page"""
        time.sleep(self.delay)  # Be respectful
        response = requests.get(url, headers=self.headers, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    
    def scrape(self) -> List[Job]:
        """Override this in child classes"""
        raise NotImplementedError