import json
# 1. Simulated raw job listing data (List of Dictionaries)
raw_job_listings = [
    {
        "id": 101,
        "title": "Werkstudent Software Engineer",
        "company": "TechBerlin GmbH",
        "location": "Berlin",
        "skills": ["Python", "Git", "Linux", "REST APIs"]

    },
    {
        "id": 102,
        "title": "Junior Solutions Architect",
        "company": "CloudCloud Munich",
        "location": "Munich",
        "skills": ["AWS", "Python", "SQL", "Docker"]
    },
    {
        "id": 103,
        "title": "Data Pipeline Werkstudent",
        "company": "DataFlow Frankfurt",
        "location": "Frankfurt",
        "skills": ["Python", "SQL", "ETL", "Git"]
    }
]

def extract_skill_metrics(jobs):
    """Processes raw job objects and calculates skill frequencies."""
    skill_counts = {}

    for job in jobs:
        print(f"Processing Role: {job['title']} at {job['company']} ({job['location']})")
        for skill in job['skills']:
            skill_counts[skill] = skill_counts.get(skill, 0) + 1
    return skill_counts

if __name__ == "__main__":
    print("--- Starting Job Data Processor ---\n")
    results = extract_skill_metrics(raw_job_listings)

    print("\n--- Skill Demand Summary ---")
    for skill, count in sorted(results.items(), key=lambda x: x[1], reverse=True):
        print(f" - {skill}:{count} job posting(s)")

