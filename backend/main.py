from fastapi import FastAPI, Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
#from backend.database import engine, SessionLocal
from backend.database import engine, SessionLocal

from backend import models

from backend import database
from fastapi import FastAPI
from backend.database import engine
from backend import models


# Create tables once
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to Skillmap AI"}


# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load data
import os
data_path = os.path.join(os.path.dirname(__file__), 'data', 'career_data.csv')
df = pd.read_csv(data_path)

# Preprocess features
df["features"] = (df["skills"].str.replace(";", " ") + " " + df["interest"]).str.lower()

# Vectorize
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["features"])

class CareerInput(BaseModel):
    skills: list[str]
    interests: list[str]

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

@app.get("/")
def read_root():
    return {"message": "Welcome to Skillmap AI API"}

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


print("Database connection successful!")


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load data
import os
data_path = os.path.join(os.path.dirname(__file__), 'data', 'career_data.csv')
df = pd.read_csv(data_path)


# Preprocess features
df["features"] = (df["skills"].str.replace(";", " ") + " " + df["interest"]).str.lower()

# Vectorize
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["features"])

class CareerInput(BaseModel):
    skills: list[str]
    interests: list[str]

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
@app.get("/")
def read_root():
    return {"message": "Welcome to Skillmap AI API"}


#DARABASE CREATE
from backend.database import engine  
from backend.models import Base

Base.metadata.create_all(bind=engine)

# Us DB in API
from fastapi import Depends
from sqlalchemy.orm import Session
from backend.database import SessionLocal

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#adzuna api
from backend.routes import adzuna
app.include_router(adzuna.router)

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))  #backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # root




