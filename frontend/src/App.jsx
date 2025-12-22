import { useState } from "react";

function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);

  const search = async () => {
    const res = await fetch(
      `http://localhost:8000/search?q=${encodeURIComponent(query)}`
    );
    const data = await res.json();
    setResults(data);
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Indonesian Recipe Semantic Search</h1>

      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Cari nama makanan atau bahan"
        style={{ padding: 8, width: "60%" }}
      />

      <button onClick={search} style={{ marginLeft: 10 }}>
        Cari
      </button>

      <ul>
        {results.map((r, i) => (
          <li key={i}>
            <h3>{r.title} ({r.score.toFixed(3)})</h3>
            <p><b>Ingredients:</b> {r.ingredients}</p>
            <p><b>Steps:</b> {r.steps}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
