import React from "react";

const LandingPage = ({ query, setQuery, onSearch }) => {
  return (
    <div className="landing-container">
      <section className="hero">
        <h1 className="hero-title">Indonesian Recipe Semantic Search</h1>
        <p className="hero-subtitle">
          Cari resep Indonesia berdasarkan nama atau bahan
        </p>
        <div className="hero-search">
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Cari nama makanan atau bahan"
            className="search-input"
            onKeyDown={(e) => e.key === 'Enter' && onSearch()}
          />
          <button className="search-btn" onClick={onSearch}>
            Cari
          </button>
        </div>
        <p className="empty">Masukkan kata kunci dan tekan Cari</p>
      </section>
    </div>
  );
};

export default LandingPage;
