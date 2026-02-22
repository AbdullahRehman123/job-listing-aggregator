from scrapers.remoteok_scraper import RemoteOKScraper
from utils.exporter import export_to_excel

def main():
    print("Starting job scraping...")
    
    # Initialize scraper
    scraper = RemoteOKScraper()
    
    # Scrape jobs
    jobs = scraper.scrape()
    
    # Export to Excel
    if jobs:
        export_to_excel(jobs)
        print(f"\nTotal jobs scraped: {len(jobs)}")
    else:
        print("No jobs found")

if __name__ == "__main__":
    main()