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

#Create all tables in the database
models.Base.metadata.create_all(bind=engine)

#Initialize FastAPI app
app = FastAPI()

#Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Load and preprocess career data
data_path = os.path.join(os.path.dirname(__file__), "data", "career_data.csv")
df = pd.read_csv(data_path)
df.columns = df.columns.str.lower()

required_columns = {"career", "skills", "industry"}
if not required_columns.issubset(df.columns):
    raise ValueError(f"CSV must contain the following columns: {required_columns}")

df["features"] = (
    df["skills"].fillna("").str.replace(";", " ", regex=False) + " " + df["industry"].fillna("")
).str.lower()

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["features"])

#Input schema
class CareerInput(BaseModel):
    skills: list[str]
    industry: list[str]

@app.get("/")
def read_root():
    return {"message": "Welcome to Skillmap AI API"}

@app.post("/predict")
def predict(input: CareerInput):
    input_text = " ".join(input.skills + input.industry).lower().strip()
    if not input_text:
        return {"recommendation": [{"career": "Input is empty.", "fit": 0.0}]}

    input_vector = vectorizer.transform([input_text])
    similarities = cosine_similarity(input_vector, X)[0]

    #Get indices of top 5 best matches
    top_indices = similarities.argsort()[::-1][:5]
    recommendations = []

    for idx in top_indices:
        score = similarities[idx]
        if score < 0.1:
            continue
        recommendations.append({
            "career": df.iloc[idx]["career"],
            "fit": round(score * 100, 2)
        })

    if not recommendations:
        return {"recommendation": [{"career": "No good match found", "fit": 0.0}]}

    return {"recommendation": recommendations}


#Include Adzuna job routes
app.include_router(adzuna_router, prefix="/jobs", tags=["Jobs"])

#DB session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()