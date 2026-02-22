from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Job:
    """Job listing data model"""
    title: str
    company: str
    location: str
    job_type: str  # remote, hybrid, onsite
    salary: Optional[str]
    description: str
    url: str
    technologies: list
    experience_level: Optional[str]
    posted_date: Optional[str]
    source: str  # remoteok, weworkremotely, etc
    scraped_at: datetime
    
    def to_dict(self):
        return {
            'title': self.title,
            'company': self.company,
            'location': self.location,
            'job_type': self.job_type,
            'salary': self.salary,
            'description': self.description[:200],  # Truncate
            'url': self.url,
            'technologies': ','.join(self.technologies),
            'experience_level': self.experience_level,
            'posted_date': self.posted_date,
            'source': self.source,
            'scraped_at': self.scraped_at.strftime('%Y-%m-%d %H:%M:%S')
        }