import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
import joblib

# Load CSV data
def load_data():
    df = pd.read_csv("data/career_data.csv")
    df['skills'] = df['skills'].apply(lambda x: x.split(';'))
    return df

# Encode features
def prepare_features(df):
    mlb = MultiLabelBinarizer()
    X_skills = mlb.fit_transform(df['skills'])

    # Encode interest
    df['interest_code'] = df['interest'].astype('category').cat.codes
    interest_codes = df['interest_code'].values.reshape(-1, 1)

    # Combine skills + interest
    X = np.hstack([X_skills, interest_codes])
    y = df['career']
    return X, y, mlb

# Train and save model
def train_and_save_model():
    df = load_data()
    X, y, mlb = prepare_features(df)

    model = RandomForestClassifier(random_state=42)
    model.fit(X, y)

    preds = model.predict(X)
    acc = (preds == y).mean()
    print(f"Model training accuracy: {acc:.2f}")

    joblib.dump(model, "models/career_model.pkl")
    joblib.dump(mlb, "models/mlb.pkl")

# Prediction for testing
def get_career_recommendation(user):
    model = joblib.load("models/career_model.pkl")
    mlb = joblib.load("models/mlb.pkl")

    input_skills = user.skills
    input_interest = user.interests[0].lower()

    interest_map = {"tech": 0, "business": 1, "art": 2, "marketing": 3}
    interest_code = interest_map.get(input_interest, 0)

    skill_vector = mlb.transform([input_skills])
    full_input = np.hstack([skill_vector, [[interest_code]]])

    prediction = model.predict(full_input)[0]
    confidence = max(model.predict_proba(full_input)[0]) * 100

    return [{"career": prediction, "fit": round(confidence, 2)}]

# Run and test
if __name__ == "__main__":
    train_and_save_model()

    # Quick test
    class DummyUser:
        def __init__(self):
            self.skills = ['programming', 'python']
            self.interests = ['tech']

    result = get_career_recommendation(DummyUser())
    print("Test prediction:", result)
