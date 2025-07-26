import React, { useState } from "react";
 // import './dark-theme.css';    // not loaded in this file, but can be used if needed


function App() {
  const [skills, setSkills] = useState("");
  const [industry, setindustry] = useState("tech");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [jobListings, setJobListings] = useState([]);
  const [jobsLoading, setJobsLoading] = useState(false);

  const fetchJobs = async (keyword) => {
    setJobsLoading(true);
    try {
      const response = await fetch(
        `http://127.0.0.1:8000/jobs?what=${encodeURIComponent(keyword)}`
      );
      const data = await response.json();
      setJobListings(data.jobs || []);
    } catch (error) {
      console.error("Job fetch failed:", error);
      setJobListings([]);
    }
    setJobsLoading(false);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);
    setJobListings([]);

    const inputData = {
      skills: skills.split(",").map((s) => s.trim().toLowerCase()),
      industry: [industry.toLowerCase()],
    };

    try {
      const response = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(inputData),
      });

      const data = await response.json();
      setResult(data.recommendation);

      if (data.recommendation?.length > 0) {
        await fetchJobs(data.recommendation[0].career);
      }
    } catch (error) {
      console.error("Prediction failed:", error);
      setResult([{ career: "Error", fit: 0 }]);
    }

    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white font-sans px-4 py-6">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-3xl font-bold mb-6 text-center text-purple-400">
          Skillmap AI — Career Predictor and Job Finder
        </h1>

        <form
          onSubmit={handleSubmit}
          className="space-y-4 bg-gray-800 p-6 rounded-lg shadow-lg"
        >
          <div>
            <label className="block mb-2 text-sm text-gray-300">
             Add Your Skills (comma-separated):
            </label>
            <input
              type="text"
              value={skills}
              onChange={(e) => setSkills(e.target.value)}
              placeholder="e.g. python, design"
              className="w-full px-4 py-2 rounded bg-gray-700 text-white border border-gray-600 focus:outline-none focus:ring-2 focus:ring-purple-500"
              required
            />
          </div>

          <div>
            <label className="block mb-2 text-sm text-gray-300">industry:</label>
            <select
              value={industry}
              onChange={(e) => setindustry(e.target.value)}
              className="w-full px-4 py-2 rounded bg-gray-700 text-white border border-gray-600 focus:outline-none focus:ring-2 focus:ring-purple-500"
            >
              <option value="technology">Technology</option>
              <option value="engineering">Engineering</option>
              <option value="healthcare">Healthcare</option>
              <option value="marketing">Marketing</option>
              <option value="art & design">Art & Design</option>
              <option value="finance">Finance</option>
              <option value="education">Education</option>
              <option value="business">Business</option>
              <option value="media">Media</option>
              <option value="law & politics">Law & Politics</option>
              <option value="hospitality">Hospitality</option>
              <option value="logistics">Logistics</option>
              <option value="retail & sales">Retail & Sales</option>
              <option value="sports & fitness">Sports & Fitness</option>
              <option value="real estate">Real Estate</option>
              <option value="agriculture">Agriculture</option>
            </select>
          </div>

          <button
            type="submit"
            className="bg-purple-600 hover:bg-purple-700 text-white py-2 px-6 rounded w-full font-semibold transition"
          >
            {loading ? "Loading..." : "Get Career Recommendation and Jobs"}
          </button>
        </form>

        {result && (
          <div className="mt-8 bg-gray-800 p-6 rounded-lg shadow-lg">
            <h2 className="text-xl font-semibold mb-4 text-purple-400">
              Recommended Careers:
            </h2>
            <ul className="space-y-2">
              {result.map((item, index) => (
                <li key={index} className="bg-gray-700 p-3 rounded-lg">
                  <span className="font-medium text-white">{item.career}</span>{" "}
                  —{" "}
                  <span className="text-green-400">
                    Fit Score: {item.fit.toFixed(2)}%
                  </span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {jobsLoading && (
          <p className="text-sm text-gray-300 mt-4">Loading jobs...</p>
        )}

        {!jobsLoading && jobListings.length > 0 && (
          <div className="mt-8 bg-gray-800 p-6 rounded-lg shadow-lg">
            <h2 className="text-xl font-semibold mb-4 text-purple-400">
              Job Listings
            </h2>
            <ul className="space-y-4">
              {jobListings.map((job, idx) => (
                <li key={idx} className="bg-gray-700 p-4 rounded-lg">
                  <h3 className="font-semibold text-white text-lg">{job.title}</h3>
                  <p className="text-gray-300">
                    {job.company?.display_name || "Unknown Company"}
                  </p>
                  <p className="text-gray-400 text-sm">
                    {job.location?.display_name || "Unknown Location"}
                  </p>
                  <a
                    href={job.redirect_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-block mt-2 text-purple-400 hover:underline"
                  >
                    View Job →
                  </a>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
