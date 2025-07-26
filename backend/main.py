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

# FastAPI App Initialization
app = FastAPI()

#  Add router BEFORE any route definitions
app.include_router(adzuna_router, prefix="/jobs", tags=["Jobs"])

# CORS Middleware 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load & Vectorize Career Data
data_path = os.path.join(os.path.dirname(__file__), 'data', 'career_data.csv')
df = pd.read_csv(data_path)
df["features"] = (df["skills"].str.replace(";", " ") + " " + df["interest"]).str.lower()

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["features"])

#  Input Schema 
class CareerInput(BaseModel):
    skills: list[str]
    interests: list[str]

# Root Route 
@app.get("/")
def read_root():
    return {"message": "Welcome to Skillmap AI API"}

# Predict Route
@app.post("/predict")
def predict(input: CareerInput):
    input_text = " ".join(input.skills + input.interests).lower()
    input_vector = vectorizer.transform([input_text])
    sims = cosine_similarity(input_vector, X)[0]

    best_index = sims.argmax()
    best_score = sims[best_index]
    best_career = df.iloc[best_index]["career"]

    return {
        "recommendation": [
            {
                "career": best_career,
                "fit": round(best_score * 100, 2)
            }
        ]
    }

#  DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
