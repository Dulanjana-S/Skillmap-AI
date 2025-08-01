from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
import os
import requests # can switch to httpx for async requests

router = APIRouter()

#hardcoded keys
ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID", "2f056b28")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY", "e9c956417815ba36d292ce02c9b6aa37")
BASE_URL = "https://api.adzuna.com/v1/api/jobs/gb/search/1"

@router.get("/")
def get_jobs(what: str = Query(..., description="Job title or keyword to search")):
    try:
        url = (
            f"{BASE_URL}"
            f"?app_id={ADZUNA_APP_ID}"
            f"&app_key={ADZUNA_APP_KEY}"
            f"&what={what}"
            f"&results_per_page=10"
        )
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # jobs format
        jobs = []
        for job in data.get("results", []):
            jobs.append({
                "title": job.get("title"),
                "location": job.get("location", {}),
                "salary_min": job.get("salary_min"),
                "salary_max": job.get("salary_max"),
                "description": job.get("description"),
                "redirect_url": job.get("redirect_url"),
            })

        return {"jobs": jobs}

    except requests.exceptions.RequestException as e:
        return JSONResponse(status_code=400, content={"error": str(e)})
