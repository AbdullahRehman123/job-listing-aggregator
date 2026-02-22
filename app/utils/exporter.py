import pandas as pd
from typing import List
from models.job import Job
from datetime import datetime
from pathlib import Path

def export_to_excel(jobs: List[Job], filename: str = None) -> str:
    """Export jobs to Excel"""

    # Get project root directory
    BASE_DIR = Path(__file__).parent.parent.parent
    DATA_DIR = BASE_DIR / "data"

    # Ensure data directory exists
    DATA_DIR.mkdir(exist_ok=True)

    if not filename:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = DATA_DIR / f"jobs_{timestamp}.xlsx"
    else:
        filename = DATA_DIR / filename
    
    # Convert to dictionaries
    data = [job.to_dict() for job in jobs]
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Export to Excel
    df.to_excel(str(filename), index=False, engine='openpyxl')
    
    print(f"Exported {len(jobs)} jobs to {filename}")
    return filename