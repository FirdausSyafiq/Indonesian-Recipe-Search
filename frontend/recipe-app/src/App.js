import { useState } from "react";

function App() {
  const [q, setQ] = useState("");
  const [results, setResults] = useState([]);

  const search = async () => {
    const res = await fetch(`http://localhost:8000/search?q=${q}`);
    const data = await res.json();
    setResults(data);
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Recipe Semantic Search</h1>
      <input
        value={q}
        onChange={(e) => setQ(e.target.value)}
        placeholder="Cari bahan atau nama makanan"
        style={{ padding: 8, width: "60%", marginRight: 10 }}
      />
      <button onClick={search}>Search</button>

      <ul>
        {results.map((r, i) => (
          <li key={i} style={{ marginTop: 20 }}>
            <h3>{r.title} ({r.score.toFixed(3)})</h3>
            <p><b>Bahan:</b> {r.ingredients}</p>
            <p><b>Cara membuat:</b> {r.steps}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
