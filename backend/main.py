from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import faiss
import json
from sentence_transformers import SentenceTransformer

MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"

app = FastAPI()

# CORS (agar frontend React bisa mengakses backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Loading SBERT model…")
model = SentenceTransformer(MODEL_NAME)

print("Loading FAISS index & metadata…")
index = faiss.read_index("faiss.index")
metadata = json.load(open("metadata.json"))

@app.get("/search")
def search(q: str, k: int = 100):
    emb = model.encode([q], normalize_embeddings=True)
    D, I = index.search(emb, k)

    # Logika Adaptif untuk Model Multilingual (paraphrase-multilingual-MiniLM-L12-v2):
    # TEMUAN DEBUGGING:
    # - "pig" vs "kambing" scorenya TINGGI SEKALI (~0.58)! Ini masalah model yang menganggap
    #   semua "daging hewan" itu mirip.
    # - "asdasd" scorenya ~0.10 - 0.16.
    # - "cabe" vs resep cabe scorenya ~0.18 - 0.22.
    
    # KESIMPULAN:
    # Kita tidak bisa hanya mengandalkan threshold angka skor saja, karena "pig" (salah)
    # skornya 0.58, sedangkan "cabe" (benar) skornya cuma 0.20.
    # Ini anomali model multilingual pada data resep spesifik ini.

    # SOLUSI HYBRID:
    # 1. Filter Sampah Mutlak: Jika skor < 0.15, buang (ini menyaring 'asdasd').
    # 2. Tapi untuk kasus "pig" (skor tinggi tapi salah konteks), kita biarkan dulu,
    #    karena sulit membedakan "pig" vs "goat" hanya dari angka vektor di model ini.
    #    (Kecuali kita ganti model lagi, tapi user minta solusi cepat).
    
    if len(D[0]) > 0 and D[0][0] < 0.15:
        return []

    results = []
    
    # Preprocessing query sederhana untuk pencarian keyword (case insensitive)
    # + QUERY EXPANSION (Sinonim)
    query_terms = q.lower().split()
    expanded_terms = set(query_terms) # Gunakan set agar tidak ada duplikat
    
    # Kamus sinonim sederhana (Bisa ditambah sesuai kebutuhan)
    synonyms = {
        "cabai": "cabe",
        "cabe": "cabai",
        "lombok": "cabe",
        "telur": "telor",
        "telor": "telur",
        "ayam": "daging ayam",
        "sapi": "daging sapi"
    }
    
    # Tambahkan sinonim ke dalam pencarian keyword
    for term in query_terms:
        if term in synonyms:
            expanded_terms.add(synonyms[term])
            
    # Convert kembali ke list untuk iterasi
    search_keywords = list(expanded_terms)
    
    for score, idx in zip(D[0], I[0]):
        # 1. Filter Sampah Mutlak
        if score < 0.15:
            continue
            
        m = metadata[idx]
        title_lower = m["title"].lower()
        ingredients_lower = m["ingredients"].lower()
        
        # --- LOGIKA HYBRID (VECTOR + KEYWORD) ---
        is_relevant = False
        
        # Kategori 1: High Confidence (Skor Vektor Tinggi)
        # Jika skor > 0.50, kita percaya penuh pada Semantic Search
        if score > 0.50:
            is_relevant = True
            
        # Kategori 2: Low Confidence (Skor Vektor Rendah 0.15 - 0.50)
        # Validasi manual: Cek apakah ada kata kunci query di Judul/Bahan?
        else:
            # Cek apakah SALAH SATU kata kunci (termasuk sinonim) muncul di teks
            # Contoh: Query "Cabai", tapi teksnya "Cabe rawit" -> MATCH karena sinonim!
            match_found = any(term in title_lower or term in ingredients_lower for term in search_keywords)
            
            if match_found:
                is_relevant = True
            else:
                # Skor kecil DAN tidak ada kata yang cocok = Kemungkinan besar tidak relevan
                # Contoh: Query "Kambing", Hasil "Babi Kecap" (Skor 0.4 tapi kata 'kambing' tidak ada)
                is_relevant = False
        
        if is_relevant:
            results.append({
                "title": m["title"],
                "ingredients": m["ingredients"],
                "steps": m["steps"],
                "url": m["url"],
                "category": m["category"],
                "total_ingredients": m["total_ingredients"],
                "total_steps": m["total_steps"],
                "loves": m["loves"],
                "score": float(score)
            })

    return results
