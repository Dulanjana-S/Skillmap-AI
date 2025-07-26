import React, { useState } from "react";

function App() {
  const [skills, setSkills] = useState("");
  const [interest, setInterest] = useState("tech");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const [jobListings, setJobListings] = useState([]);
  const [jobsLoading, setJobsLoading] = useState(false);
  const [jobsError, setJobsError] = useState(null);

  const fetchJobs = async (keyword) => {
  setJobsLoading(true);
  setJobsError(null);
  try {
    const response = await fetch(`http://127.0.0.1:8000/jobs?what=${encodeURIComponent(keyword)}`);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    if (data.jobs) {
      setJobListings(data.jobs);
    } else {
      setJobListings([]);
    }
  } catch (error) {
    setJobsError(error.message);
    setJobListings([]);
  }
  setJobsLoading(false);
};



  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);
    setJobListings([]);
    setJobsError(null);

    const inputData = {
      skills: skills.split(",").map((s) => s.trim().toLowerCase()), // array of strings
      interests: [interest.toLowerCase()], // array with one string
    };

    try {
      const response = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(inputData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Server error");
      }

      const data = await response.json();
      setResult(data.recommendation);

      // Fetch jobs for the recommended career
    if (data.recommendation && data.recommendation.length > 0 && data.recommendation[0].career) {
      await fetchJobs(data.recommendation[0].career);
      }

    } catch (error) {
      console.error("Prediction failed:", error);
      setResult([{ career: "Error", fit: 0 }]);
    }

    setLoading(false);
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial" }}>
      <h1>Skillmap AI — Career Predictor</h1>

      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: "1rem" }}>
          <label>Skills (comma-separated):</label>
          <br />
          <input
            type="text"
            value={skills}
            onChange={(e) => setSkills(e.target.value)}
            placeholder="e.g. python, programming"
            style={{ width: "100%", padding: "0.5rem" }}
            required
          />
        </div>

        <div style={{ marginBottom: "1rem" }}>
          <label>Interests:</label>
          <br />
          <select
            value={interest}
            onChange={(e) => setInterest(e.target.value)}
            style={{ width: "100%", padding: "0.5rem" }}
          >
            <option value="tech">Tech</option>
            <option value="business">Business</option>
            <option value="art">Art</option>
            <option value="marketing">Marketing</option>
          </select>
        </div>

        <button type="submit" style={{ padding: "0.5rem 1rem" }}>
          {loading ? "Loading..." : "Get Career Recommendation"}
        </button>
      </form>

      {/* Recommended careers */}
      {result && (
        <div style={{ marginTop: "2rem" }}>
          <h3>Recommended Careers:</h3>
          <ul>
            {result.map((item, index) => (
              <li key={index}>
                <strong>{item.career}</strong> — Fit Score:{" "}
                {item.fit.toFixed(2)}%
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Job listings section */}
      {jobsLoading && <p>Loading job listings...</p>}

      {jobsError && (
        <p style={{ color: "red" }}>Error loading jobs: {jobsError}</p>
      )}

      {jobListings.length > 0 && (
        <div style={{ marginTop: "2rem" }}>
          <h3>Job Listings for {result[0].career}:</h3>
          <ul>
            {jobListings.map((job, index) => (
              <li key={index} style={{ marginBottom: "1rem" }}>
                <a
                  href={job.redirect_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{ fontWeight: "bold", color: "#0077cc" }}
                >
                  {job.title}
                </a>
                <p>{job.location.display_name}</p>
                <p>
                  Salary:{" "}
                  {job.salary_min
                    ? `$${job.salary_min.toLocaleString()}`
                    : "N/A"}{" "}
                  -{" "}
                  {job.salary_max
                    ? `$${job.salary_max.toLocaleString()}`
                    : "N/A"}
                </p>
                <p>{job.description}</p>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;
