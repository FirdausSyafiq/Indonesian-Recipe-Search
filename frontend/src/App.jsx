import { useState, useEffect } from "react";
import "./App.css";
import LandingPage from "./components/LandingPage";
import ResultsPage from "./components/ResultsPage";

// Toast Component
const Toast = ({ message, onClose }) => {
  useEffect(() => {
    const timer = setTimeout(onClose, 3000);
    return () => clearTimeout(timer);
  }, [onClose]);

  return (
    <div className="toast-container">
      <span className="toast-icon">⚠️</span>
      <span>{message}</span>
    </div>
  );
};

function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [page, setPage] = useState("home");
  const [toast, setToast] = useState(null);

  const showToast = (message) => {
    setToast(message);
  };

  const search = async () => {
    try {
      const res = await fetch(
        `http://localhost:8000/search?q=${encodeURIComponent(query)}`
      );
      const data = await res.json();
      setResults(data);
    } catch (error) {
      console.error("Error searching:", error);
      setResults([]);
    }
  };

  const handleSearch = () => {
    if (!query.trim()) {
      showToast("Silakan masukkan kata kunci pencarian!");
      return;
    }
    search().then(() => setPage("results"));
  };

  const handleResultsSearch = () => {
    if (!query.trim()) {
      showToast("Silakan masukkan kata kunci pencarian!");
      return;
    }
    search();
  };

  return (
    <div className="app-root">
      {toast && <Toast message={toast} onClose={() => setToast(null)} />}
      
      {page === "home" ? (
        <LandingPage 
          query={query} 
          setQuery={setQuery} 
          onSearch={handleSearch} 
        />
      ) : (
        <ResultsPage
          query={query}
          setQuery={setQuery}
          results={results}
          onSearch={handleResultsSearch}
          onBack={() => setPage("home")}
        />
      )}
    </div>
  );
}

export default App;
