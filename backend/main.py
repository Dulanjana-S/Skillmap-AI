from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

from backend.database import engine, SessionLocal
from backend import models
from backend.routes.adzuna_routes import router as adzuna_router

# Database Setup
models.Base.metadata.create_all(bind=engine)

# FastAPI app initialization
app = FastAPI()

# Add Adzuna jobs router BEFORE any route definitions
app.include_router(adzuna_router, prefix="/jobs", tags=["Jobs"])

# CORS middleware - allow your React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load & preprocess career data CSV
data_path = os.path.join(os.path.dirname(__file__), 'data', 'career_data.csv')
df = pd.read_csv(data_path)

# Replace semicolons with space in skills, then combine skills + interest in lowercase
df["features"] = (df["skills"].str.replace(";", " ", regex=False) + " " + df["interest"]).str.lower()

# Initialize vectorizer & fit on features
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["features"])

# Input schema for predict route
class CareerInput(BaseModel):
    skills: list[str]
    interests: list[str]

@app.get("/")
def read_root():
    return {"message": "Welcome to Skillmap AI API"}

@app.post("/predict")
def predict(input: CareerInput):
    # Combine skills and interests from input, lowercased, space separated
    input_text = " ".join(input.skills + input.interests).lower()
    
    # Vectorize input text and calculate cosine similarity with career dataset
    input_vector = vectorizer.transform([input_text])
    sims = cosine_similarity(input_vector, X)[0]

    best_index = sims.argmax()
    best_score = sims[best_index]
    best_career = df.iloc[best_index]["career"]

    # If similarity is very low (e.g. < 0.1), treat as no match
    if best_score < 0.1:
        return {
            "recommendation": [
                {
                    "career": "No good match found",
                    "fit": 0.0
                }
            ]
        }

    return {
        "recommendation": [
            {
                "career": best_career,
                "fit": round(best_score * 100, 2)
            }
        ]
    }

# DB session dependency (if needed by other routes)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
