import React, { useEffect, useState } from "react";
import axios from "axios";

const JobResults = ({ skill }) => {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchJobs = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/jobs?skill=${skill}`);
        setJobs(response.data.jobs);
      } catch (err) {
        console.error(err);
        setError("Failed to fetch job results.");
      } finally {
        setLoading(false);
      }
    };

    fetchJobs();
  }, [skill]);

  if (loading) return <p>Loading job listings...</p>;
  if (error) return <p>{error}</p>;
  if (jobs.length === 0) return <p>No jobs found for "{skill}"</p>;

  return (
    <div className="mt-6">
      <h2 className="text-xl font-bold mb-4">Job Opportunities for "{skill}"</h2>
      <div className="grid gap-4">
        {jobs.map((job, index) => (
          <div key={index} className="p-4 border rounded shadow">
            <h3 className="text-lg font-semibold">{job.title}</h3>
            <p><strong>Company:</strong> {job.company}</p>
            <p><strong>Location:</strong> {job.location}</p>
            {job.salary && <p><strong>Salary:</strong> {job.salary}</p>}
            <p className="text-sm mt-2">{job.description.slice(0, 150)}...</p>
            <a
              href={job.url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:underline mt-2 block"
            >
              View Job
            </a>
          </div>
        ))}
      </div>
    </div>
  );
};

export default JobResults;
