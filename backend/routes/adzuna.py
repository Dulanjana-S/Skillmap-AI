from fastapi import APIRouter, HTTPException
from backend.services.adzuna_service import fetch_jobs

router = APIRouter()

@router.get("/jobs")
def get_jobs(country: str = "gb", keyword: str = "software", page: int = 1):
    try:
        jobs = fetch_jobs(country=country, keyword=keyword, page=page)
        return jobs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    #test
print("ADZUNA ROUTE LOADED OK")  


