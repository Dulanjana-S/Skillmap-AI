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

# -------------- Database Setup --------------
models.Base.metadata.create_all(bind=engine)

# -------------- FastAPI App Initialization --------------
app = FastAPI()

# -------------- CORS Middleware --------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------- Load Career Data --------------
data_path = os.path.join(os.path.dirname(__file__), 'data', 'career_data.csv')
df = pd.read_csv(data_path)
df.columns = df.columns.str.lower()  # <-- Normalize column names


# Debug: check columns
print("Loaded CSV Columns:", df.columns.tolist())

# Ensure required columns are present
required_columns = {"career", "skills", "industry"}
if not required_columns.issubset(df.columns):
    raise ValueError(f"CSV must contain the following columns: {required_columns}")

# Combine 'skills' and 'industry' into a single feature string
df["features"] = (
    df["skills"].fillna("").str.replace(";", " ", regex=False) + " " + df["industry"].fillna("")
).str.lower()

# Vectorize features
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["features"])

# -------------- Request Schema --------------
class CareerInput(BaseModel):
    skills: list[str]
    industry: list[str]

# -------------- Routes --------------
@app.get("/")
def read_root():
    return {"message": "Welcome to Skillmap AI API"}

@app.post("/predict")
def predict(input: CareerInput):
    # Join user input
    input_text = " ".join(input.skills + input.industry).lower().strip()

    if not input_text:
        return {
            "recommendation": [
                {
                    "career": "Input is empty. Please enter your skills and interests.",
                    "fit": 0.0
                }
            ]
        }

    # Vectorize and calculate similarity
    input_vector = vectorizer.transform([input_text])
    similarities = cosine_similarity(input_vector, X)[0]
    best_index = similarities.argmax()
    best_score = similarities[best_index]

    if best_score < 0.1:
        return {
            "recommendation": [
                {
                    "career": "No good match found",
                    "fit": 0.0
                }
            ]
        }

    recommended_career = df.iloc[best_index]["career"]
    return {
        "recommendation": [
            {
                "career": recommended_career,
                "fit": round(best_score * 100, 2)
            }
        ]
    }

# -------------- Include Job Listing Routes (Adzuna) --------------
app.include_router(adzuna_router, prefix="/jobs", tags=["Jobs"])

# -------------- Dependency for DB Session --------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
