import requests
from parse_job import extract_skill_metrics

# Target REST API Endpoint (Free German Job Board API - No Key Needed)

API_URL = "https://www.arbeitnow.com/api/job-board-api"

def fetch_live_jobs():
    """Fetches raw job listing data from the remote HTTP REST API."""
    print(f"Connecting to remote endpoint: {API_URL}")

    try:
        # Send HTTP GET Request (Port 443 HTTPS)
        response = requests.get(API_URL, timeout=10)

        # Raise an exception if the HTTP status code is 4xx or 5xx
        response.raise_for_status()

        # Deserialize raw JSON response into Python lists and dictionaries
        payload = response.json()
        raw_jobs = payload.get("data", [])
        print(f"✓ HTTP 200 OK: Successfully retrieved {len(raw_jobs)} live job postings.\n")
        return raw_jobs
    except requests.exceptions.RequestException as error:
        print(f"❌ Network or API error occurred: {error}")
        return []
def transform_api_jobs(raw_jobs):
    """Standardizes live API payload objects into our pipeline's internal format."""
    standardized_jobs = []
    
    for item in raw_jobs:
        # Extract tags/keywords from the API response
        tags = item.get("tags", [])
        
        standardized_jobs.append({
            "id": item.get("slug"),
            "title": item.get("title"),
            "company": item.get("company_name"),
            "location": item.get("location"),
            "skills": tags  # API provides tags like ["Python", "AWS", "Remote"]
        })
        
    return standardized_jobs

if __name__ == "__main__":
    print("=== Week 3: Live API Data Ingestion Pipeline ===\n")
    
    # EXTRACT: Pull raw data from external HTTP API
    raw_api_data = fetch_live_jobs()
    
    if raw_api_data:
        # TRANSFORM: Standardize data structure
        clean_jobs = transform_api_jobs(raw_api_data)
        
        # LOAD / METRICS: Feed clean data into our existing parsing engine
        print("--- Running Analytics Reactor on Live Stream ---")
        metrics = extract_skill_metrics(clean_jobs[:10])  # Process top 10 postings
        
        print("\n--- Live Market Demand Summary ---")
        for skill, count in sorted(metrics.items(), key=lambda x: x[1], reverse=True):
            print(f"• {skill}: {count} posting(s)")
