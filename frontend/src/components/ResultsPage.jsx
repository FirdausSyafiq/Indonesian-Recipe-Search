import React, { useState, useEffect } from "react";

const ResultsPage = ({ query, setQuery, results, onSearch, onBack }) => {
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 6;

  // Reset page when results change
  useEffect(() => {
    setCurrentPage(1);
  }, [results]);

  // Logic for displaying current items
  const indexOfLastItem = currentPage * itemsPerPage;
  const indexOfFirstItem = indexOfLastItem - itemsPerPage;
  const currentItems = results.slice(indexOfFirstItem, indexOfLastItem);
  const totalPages = Math.ceil(results.length / itemsPerPage);

  const paginate = (pageNumber) => setCurrentPage(pageNumber);

  return (
    <div className="results-container">
      <h1 className="results-title">Indonesian Recipe Semantic Search</h1>
      <div className="toolbar">
        <button className="back-btn" onClick={onBack} title="Kembali ke Halaman Utama">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <path d="M19 12H5M12 19l-7-7 7-7" />
          </svg>
        </button>
        <div className="hero-search">
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Cari nama makanan atau bahan"
            className="search-input"
            onKeyDown={(e) => e.key === 'Enter' && onSearch()}
          />
          <button onClick={onSearch} className="search-btn">
            Cari
          </button>
        </div>
      </div>

      <div className="results">
        {results.length === 0 ? (
          <p className="empty-results">Tidak ada hasil. Coba kata kunci lain.</p>
        ) : (
          <>
            <div className="results-grid">
              {currentItems.map((r, i) => (
                <article key={i} className="recipe-card">
                  <div className="card-header">
                    <h3 className="recipe-title">{r.title}</h3>
                    <span className="score">{r.score.toFixed(3)}</span>
                  </div>

                  <div className="meta">
                    {r.category ? <span className="badge">{r.category}</span> : null}
                    {r.loves ? <span className="meta-item">❤️ {r.loves}</span> : null}
                    {r.total_ingredients ? (
                      <span className="meta-item">Bahan: {r.total_ingredients}</span>
                    ) : null}
                    {r.total_steps ? (
                      <span className="meta-item">Langkah: {r.total_steps}</span>
                    ) : null}
                  </div>

                  <div className="section">
                    <h4>Bahan</h4>
                    <ul className="text-list">
                      {r.ingredients.split('--').map((item, idx) => {
                        const cleanItem = item.trim();
                        if (!cleanItem) return null;
                        return <li key={idx}>{cleanItem}</li>;
                      })}
                    </ul>
                  </div>
                  <div className="section">
                    <h4>Langkah</h4>
                    <ol className="text-list">
                      {r.steps.split(/\d+\)\s+/).map((item, idx) => {
                        const cleanItem = item.trim();
                        if (!cleanItem) return null;
                        return <li key={idx}>{cleanItem}</li>;
                      })}
                    </ol>
                  </div>

                  {r.url ? (
                    <a
                      href={r.url}
                      target="_blank"
                      rel="noreferrer"
                      className="link"
                    >
                      Lihat resep asli
                    </a>
                  ) : null}
                </article>
              ))}
            </div>

            {/* Pagination Controls */}
            {totalPages > 1 && (
              <div className="pagination">
                <button
                  onClick={() => paginate(currentPage - 1)}
                  disabled={currentPage === 1}
                  className="page-btn prev-next"
                >
                  &laquo; Prev
                </button>
                
                {/* Simple Pagination Logic: Show all if pages <= 7, else show subset */}
                {(() => {
                  const pages = [];
                  if (totalPages <= 7) {
                    for (let i = 1; i <= totalPages; i++) pages.push(i);
                  } else {
                    if (currentPage <= 4) {
                      pages.push(1, 2, 3, 4, 5, '...', totalPages);
                    } else if (currentPage >= totalPages - 3) {
                      pages.push(1, '...', totalPages - 4, totalPages - 3, totalPages - 2, totalPages - 1, totalPages);
                    } else {
                      pages.push(1, '...', currentPage - 1, currentPage, currentPage + 1, '...', totalPages);
                    }
                  }
                  
                  return pages.map((page, index) => (
                    <button
                      key={index}
                      onClick={() => typeof page === 'number' && paginate(page)}
                      disabled={page === '...'}
                      className={`page-btn ${currentPage === page ? 'active' : ''} ${page === '...' ? 'dots' : ''}`}
                    >
                      {page}
                    </button>
                  ));
                })()}

                <button
                  onClick={() => paginate(currentPage + 1)}
                  disabled={currentPage === totalPages}
                  className="page-btn prev-next"
                >
                  Next &raquo;
                </button>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default ResultsPage;
