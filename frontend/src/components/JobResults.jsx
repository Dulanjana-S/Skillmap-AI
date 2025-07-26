import { useEffect, useState } from "react";
import axios from "axios";

const JobResults = ({ skill }) => {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchJobs = async () => {
      try {
        const res = await axios.get(`http://localhost:8000/jobs?skill=${skill}`);
        setJobs(res.data.jobs);
      } catch (err) {
        console.error("Failed to fetch jobs", err);
      } finally {
        setLoading(false);
      }
    };

    fetchJobs();
  }, [skill]);

  if (loading) return <p>Loading jobs...</p>;

  return (
    <div>
      <h2 className="text-xl font-semibold mt-6 mb-4">Job Opportunities</h2>
      {jobs.length === 0 && <p>No job results found for "{skill}".</p>}
      <ul className="space-y-4">
        {jobs.map((job, index) => (
          <li key={index} className="p-4 border rounded shadow">
            <h3 className="text-lg font-bold">{job.title}</h3>
            <p><strong>Company:</strong> {job.company}</p>
            <p><strong>Location:</strong> {job.location}</p>
            {job.salary && <p><strong>Salary:</strong> {job.salary}</p>}
            <p>{job.description.slice(0, 150)}...</p>
            <a href={job.url} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">
              View Job
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default JobResults;


import JobResults from "./JobResults";

const ResultPage = ({ recommendation }) => {
  const skill = "software";

  return (
    <div>
      <h1>Recommended Career: {recommendation}</h1>
      <JobResults skill={skill} />
    </div>
  );
};
