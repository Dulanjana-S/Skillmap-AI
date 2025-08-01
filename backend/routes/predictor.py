# backend/routers/predictor.py

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class UserInput(BaseModel):
    skills: list[str]
    interests: list[str]

@router.post("/predict")
async def predict_career(data: UserInput):

    # replace with actual prediction code
    return {
        "recommendation": [
            {"career": "Software Engineer", "fit": 80.0}
        ]
    }
