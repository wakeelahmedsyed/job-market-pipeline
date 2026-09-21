import re
import requests
from parse_job import extract_skill_metrics

# Target REST API Endpoint
API_URL = "https://www.arbeitnow.com/api/job-board-api"

# 1. Target Technical Keyword Taxonomy to scan for
KEYWORDS_TO_SCAN = [
    "Python", "SQL", "AWS", "Docker", "Git", "Linux", "REST",
    "Java", "JavaScript", "React", "Kubernetes", "ETL", "Machine Learning",
    "Data Science", "DevOps", "Azure", "GCP", "Tableau", "Power BI",
    "C++", "Golang", "TypeScript", "Spark", "Kafka", "PostgreSQL"
]

def fetch_live_jobs():
    """Fetches raw job listing data from the remote HTTP REST API."""
    print(f"Connecting to remote endpoint: {API_URL} ...")
    
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        payload = response.json()
        raw_jobs = payload.get("data", [])
        
        print(f"✓ HTTP 200 OK: Successfully retrieved {len(raw_jobs)} live job postings.\n")
        return raw_jobs

    except requests.exceptions.RequestException as error:
        print(f"❌ Network or API error occurred: {error}")
        return []

def extract_skills_from_text(description_text):
    """Scans description text using word boundaries to detect technical keywords."""
    found_skills = []
    
    if not description_text:
        return found_skills

    for keyword in KEYWORDS_TO_SCAN:
        # Use regex word boundaries (\b) to match whole words case-insensitively
        pattern = r'\b' + re.escape(keyword) + r'\b'
        if re.search(pattern, description_text, re.IGNORECASE):
            found_skills.append(keyword)

    return found_skills

def transform_api_jobs(raw_jobs):
    """Standardizes live API payload objects into our pipeline's internal format."""
    standardized_jobs = []
    
    for item in raw_jobs:
        # Read full HTML/text description provided by the API
        description = item.get("description", "")
        detected_skills = extract_skills_from_text(description)
        
        standardized_jobs.append({
            "id": item.get("slug"),
            "title": item.get("title"),
            "company": item.get("company_name"),
            "location": item.get("location"),
            "skills": detected_skills  # Extracted tech skills array
        })
        
    return standardized_jobs

if __name__ == "__main__":
    print("=== Week 3: Live API Data Ingestion Pipeline (Keyword Extraction) ===\n")
    
    # EXTRACT: Fetch raw API payload
    raw_api_data = fetch_live_jobs()
    
    if raw_api_data:
        # TRANSFORM: Scan descriptions for tech keywords
        clean_jobs = transform_api_jobs(raw_api_data)
        
        # LOAD / ANALYTICS: Run skill demand aggregator
        print("--- Running Analytics Reactor on Extracted Keywords ---")
        metrics = extract_skill_metrics(clean_jobs)
        
        print("\n--- Clean Technical Skill Demand Summary ---")
        for skill, count in sorted(metrics.items(), key=lambda x: x[1], reverse=True):
            print(f"• {skill}: {count} posting(s)")