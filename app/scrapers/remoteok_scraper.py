from scrapers.base_scraper import BaseScraper
from models.job import Job
from datetime import datetime
from typing import List
import re

class RemoteOKScraper(BaseScraper):
    """Scraper for RemoteOK.com"""
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://remoteok.com/remote-python-jobs"
        self.source = "RemoteOK"
    
    def scrape(self) -> List[Job]:
        """Scrape Python jobs from RemoteOK"""
        jobs = []
        
        try:
            soup = self.fetch_page(self.base_url)
            
            # Debug: Save HTML to see structure
            with open('debug.html', 'w', encoding='utf-8') as f:
                f.write(soup.prettify())
            print("HTML saved to debug.html - check the structure")
            
            # Try different selectors
            job_listings = soup.find_all('tr', class_='job')
            
            if not job_listings:
                # Try alternative selector
                job_listings = soup.find_all('td', class_='company')
                print(f"Found {len(job_listings)} listings with alternative selector")
            
            print(f"Found {len(job_listings)} job listings")
            
            for idx, listing in enumerate(job_listings[:20]):
                try:
                    job = self._parse_job(listing)
                    if job:
                        jobs.append(job)
                        print(f"{idx+1}. {job.title} at {job.company}")
                except Exception as e:
                    print(f"Error parsing job {idx}: {e}")
                    continue
            
        except Exception as e:
            print(f"Error scraping {self.source}: {e}")
        
        return jobs
    
    def _parse_job(self, listing) -> Job:
        """Parse individual job listing"""
        
        # Get all text from the listing for debugging
        all_text = listing.get_text(strip=True)
        
        # Title - try multiple approaches
        title = None
        title_elem = listing.find('h2')
        if not title_elem:
            title_elem = listing.find('a', class_='preventLink')
        if not title_elem:
            title_elem = listing.find(class_='title')
        
        title = title_elem.text.strip() if title_elem else all_text[:50]
        
        # Company
        company = None
        company_elem = listing.find('h3')
        if not company_elem:
            company_elem = listing.find(class_='company')
        
        company = company_elem.text.strip() if company_elem else "Unknown"
        
        # URL
        link_elem = listing.find('a', href=True)
        url = f"https://remoteok.com{link_elem['href']}" if link_elem else ""
        
        # Technologies
        tags = listing.find_all('a', class_='tag')
        if not tags:
            tags = listing.find_all(class_='tag')
        technologies = [tag.text.strip() for tag in tags if tag.text.strip()]
        
        # Location
        location = "Remote"
        
        return Job(
            title=title,
            company=company,
            location=location,
            job_type="Remote",
            salary=None,
            description=title,
            url=url,
            technologies=technologies,
            experience_level=None,
            posted_date=None,
            source=self.source,
            scraped_at=datetime.now()
        )