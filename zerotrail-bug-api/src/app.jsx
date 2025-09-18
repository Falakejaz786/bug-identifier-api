// src/App.jsx
import { useState } from "react";

export default function App() {
  const [language, setLanguage] = useState("python");
  const [code, setCode] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [samples, setSamples] = useState([]);

  // POST /find-bug
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setResult(null);

    if (!code.trim()) {
      setError("Please enter a code snippet!");
      return;
    }

    setLoading(true);
    try {
      const res = await fetch("/find-bug", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ language, code }),
      });

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || "Failed to fetch bug analysis.");
      }

      const data = await res.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // GET /sample-cases
  const fetchSamples = async () => {
    setError("");
    try {
      const res = await fetch("/sample-cases");
      if (!res.ok) throw new Error("Failed to fetch sample cases");
      const data = await res.json();
      setSamples(data);
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-start bg-gray-50 p-4">
      <h1 className="text-3xl font-bold mb-6">AI-Powered Bug Identifier</h1>

      <form
        onSubmit={handleSubmit}
        className="w-full max-w-xl space-y-4 bg-white p-6 rounded shadow"
      >
        <div>
          <label className="block mb-1 font-medium">Language</label>
          <select
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
            className="w-full border p-2 rounded"
          >
            <option value="python">Python</option>
            <option value="javascript">JavaScript</option>
            <option value="c">C</option>
          </select>
        </div>

        <div>
          <label className="block mb-1 font-medium">Code Snippet</label>
          <textarea
            rows={10}
            value={code}
            onChange={(e) => setCode(e.target.value)}
            className="w-full border p-2 rounded font-mono"
            placeholder="Paste your code here..."
          ></textarea>
        </div>

        {error && <p className="text-red-500">{error}</p>}

        <div className="flex gap-2">
          <button
            type="submit"
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
            disabled={loading}
          >
            {loading ? "Analyzing..." : "Find Bug"}
          </button>
          <button
            type="button"
            onClick={fetchSamples}
            className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
          >
            Load Sample Cases
          </button>
        </div>
      </form>

      {result && (
        <div className="mt-6 w-full max-w-xl bg-white p-4 rounded shadow">
          <h2 className="text-xl font-semibold mb-2">Analysis Result</h2>
          <p><strong>Bug Type:</strong> {result.bug_type}</p>
          <p><strong>Description:</strong> {result.description}</p>
          {result.suggestion && <p><strong>Suggestion:</strong> {result.suggestion}</p>}
        </div>
      )}

      {samples.length > 0 && (
        <div className="mt-6 w-full max-w-xl bg-white p-4 rounded shadow">
          <h2 className="text-xl font-semibold mb-2">Sample Cases</h2>
          {samples.map((s, i) => (
            <div key={i} className="mb-4 border-b pb-2">
              <p><strong>Bug Type:</strong> {s.bug_type}</p>
              <p><strong>Description:</strong> {s.description}</p>
              {s.suggestion && <p><strong>Suggestion:</strong> {s.suggestion}</p>}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
