# 🎯 Skillmap AI – Career Predictor and Job Finder

**Skillmap AI** is an intelligent web application that helps users discover the best career paths based on their skills and interests.  
It uses **machine learning** for predictions and integrates with the **Adzuna API** to fetch real-time job opportunities related to those careers.

---

🚀 Live Demo  
Coming soon...

---

## 🧠 Features

✅ AI-powered **career prediction** (FastAPI + scikit-learn)  
✅ **Multiple** recommended career paths  
✅ **Real-time job listings** using Adzuna API  
✅ **Get Jobs** button fetches relevant jobs after prediction  
✅ Clean and responsive **React UI**  
✅ **PostgreSQL** integration via Supabase  

---

## 📸 Screenshots

> _Add relevant screenshots here once deployed_

---

## ⚙️ Tech Stack

| Layer        | Technology              |
|--------------|--------------------------|
| Frontend     | React, Tailwind CSS      |
| Backend      | FastAPI, Python, scikit-learn |
| Database     | PostgreSQL (Supabase)    |
| Job Listings | Adzuna API               |

---

## 📂 Project Structure

```
Skillmap-AI/
├── frontend/               # React frontend
│   └── src/
├── backend/                # FastAPI backend
│   ├── main.py
│   ├── routes/
│   ├── models/
│   ├── database/
│   └── data/career_data.csv
└── README.md
```

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Dulanjana-S/Skillmap-AI
cd skillmap-ai
```

---

### 2. Backend Setup (FastAPI)

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn backend.main:app --reload
```

Create a `.env` file in the `backend/` directory:

```env
ADZUNA_APP_ID=your_adzuna_app_id
ADZUNA_APP_KEY=your_adzuna_app_key
DATABASE_URL=your_supabase_postgres_url
```

---

### 3. Frontend Setup (React)

```bash
cd frontend
npm install
npm start
```

---

## 🔗 API Routes

### Career Prediction

```http
POST /predict
Content-Type: application/json

{
  "skills": ["python", "data analysis"],
  "industry": ["software"]
}
```

### Get Jobs

```http
GET /jobs/?what=software
```

---

## 🔐 Environment Variables Summary

| Variable           | Description                        |
|--------------------|------------------------------------|
| `ADZUNA_APP_ID`    | Your Adzuna app ID                 |
| `ADZUNA_APP_KEY`   | Your Adzuna API key                |
| `DATABASE_URL`     | Supabase PostgreSQL connection URL|

---

## 📈 Roadmap

- [x] Build machine learning model  
- [x] Connect to Adzuna API  
- [x] Show multiple careers  
- [x] Fetch matching jobs  
- [ ] Add filters (location, salary)  
- [ ] Add employer job posting module  
- [ ] Add authentication & user profiles  

---

## 🛣️ Future Improvements

- Add job filters: location, salary range, job type  
- Career Path Roadmaps feature:  
  - 🎓 Education & certifications needed  
  - 🧠 Skills and projects to build  
  - 🧪 Suggested internships or jobs  
  - 🧭 Step-by-step visual timeline  
- User authentication and profile saving  
- Employers can post jobs to your local job DB  
- Bookmark careers and job listings  
- Add resume analyzer for smarter predictions  

---

## 🤝 Contributing

Contributions are welcome!  
Feel free to fork, submit issues, or send a pull request.

---

## 📄 License

MIT License © 2025 [DulanjanaS]

---

## 🌟 Show Your Support

Give a ⭐ if you like this project, or share it with others who might benefit!
