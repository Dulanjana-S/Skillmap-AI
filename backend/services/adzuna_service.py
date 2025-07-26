import requests
import os

# Use environment variables for security (optional but better)
ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID", "2f056b28")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY", "e9c956417815ba36d292ce02c9b6aa37")

BASE_URL = "https://api.adzuna.com/v1/api/jobs"

def fetch_jobs(country: str = "gb", keyword: str = "software", page: int = 1):
    # url = f"https://api.adzuna.com/v1/api/jobs/gb/search/1?app_id=2f056b28&app_key=e9c956417815ba36d292ce02c9b6aa37&what=software&results_per_page=10&page=1"
    url = f"https://api.adzuna.com/v1/api/jobs/gb/search/1"

    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "what": keyword,
        "results_per_page": 10,
        
    }

    headers = {"Content-Type": "application/json"}
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()
