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

# Create database tables once
models.Base.metadata.create_all(bind=engine)

# Create FastAPI app only once
app = FastAPI()

# Setup CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load career data
data_path = os.path.join(os.path.dirname(__file__), 'data', 'career_data.csv')
df = pd.read_csv(data_path)
df["features"] = (df["skills"].str.replace(";", " ") + " " + df["interest"]).str.lower()

# Vectorize features
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["features"])

# Input schema for prediction
class CareerInput(BaseModel):
    skills: list[str]
    interests: list[str]

@app.get("/")
def read_root():
    return {"message": "Welcome to Skillmap AI API"}

@app.post("/predict")
def predict(input: CareerInput):
    print("Skills received:", input.skills)
    print("Interests received:", input.interests)

    input_text = " ".join(input.skills + input.interests).lower()
    print("Combined input:", input_text)

    input_vector = vectorizer.transform([input_text])
    sims = cosine_similarity(input_vector, X)[0]
    print("Similarities:", sims.tolist())

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


    return {
        "recommendation": [
            {
                "career": best_career,
                "fit": round(best_score * 100, 2)
            }
        ]
    }



# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Include Adzuna API router with prefix
app.include_router(adzuna_router, prefix="/adzuna", tags=["Adzuna"])
