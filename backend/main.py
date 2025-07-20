from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

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
