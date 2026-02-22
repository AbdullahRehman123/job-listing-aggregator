from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from models.job import Job
from datetime import datetime
from typing import List
import time

class RemoteOKScraper:
    """Scraper for RemoteOK.com using Selenium"""
    
    def __init__(self):
        self.base_url = "https://remoteok.com/remote-python-jobs"
        self.source = "RemoteOK"
        self.driver = None
    
    def setup_driver(self):
        """Setup Selenium WebDriver"""
        options = Options()
        options.add_argument('--headless')  # Run in background
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
    
    def scrape(self) -> List[Job]:
        """Scrape Python jobs from RemoteOK"""
        jobs = []
        
        try:
            self.setup_driver()
            self.driver.get(self.base_url)
            
            # Wait for jobs to load
            time.sleep(5)
            
            # Find job elements (they have class 'job' but not 'placeholder')
            job_elements = self.driver.find_elements(By.CSS_SELECTOR, 'tr.job:not(.placeholder)')
            
            print(f"Found {len(job_elements)} job listings")
            
            for idx, element in enumerate(job_elements[:20]):
                try:
                    job = self._parse_job(element)
                    if job:
                        jobs.append(job)
                        print(f"{idx+1}. {job.title} at {job.company}")
                except Exception as e:
                    print(f"Error parsing job {idx}: {e}")
                    continue
            
        except Exception as e:
            print(f"Error scraping {self.source}: {e}")
        finally:
            if self.driver:
                self.driver.quit()
        
        return jobs
    
    def _parse_job(self, element) -> Job:
        """Parse individual job listing"""
        
        # Title
        try:
            title = element.find_element(By.CSS_SELECTOR, 'h2[itemprop="title"]').text.strip()
        except:
            title = "N/A"
        
        # Company
        try:
            company = element.find_element(By.CSS_SELECTOR, 'h3[itemprop="name"]').text.strip()
        except:
            company = "Unknown"
        
        # URL
        try:
            url = element.get_attribute('data-url')
            if url:
                url = f"https://remoteok.com{url}"
        except:
            url = ""
        
        # Technologies (tags)
        technologies = []
        try:
            tag_elements = element.find_elements(By.CSS_SELECTOR, 'a.tag')
            technologies = [tag.text.strip() for tag in tag_elements if tag.text.strip()]
        except:
            pass
        
        # Salary
        salary = None
        try:
            salary = element.find_element(By.CSS_SELECTOR, 'div.salary').text.strip()
        except:
            pass
        
        return Job(
            title=title,
            company=company,
            location="Remote",
            job_type="Remote",
            salary=salary,
            description=title,
            url=url,
            technologies=technologies,
            experience_level=None,
            posted_date=None,
            source=self.source,
            scraped_at=datetime.now()
        )