from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import faiss
import json
from sentence_transformers import SentenceTransformer

MODEL_NAME = "firqaaa/indo-sentence-bert-base"

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

# --- KONFIGURASI THRESHOLD ---
# Ambang batas kemiripan (0.0 - 1.0)
# Didapatkan dari hasil evaluasi F1-Score pada dataset validasi.
# Jika skor < SIMILARITY_THRESHOLD, resep dianggap tidak relevan.
SIMILARITY_THRESHOLD = 0.50

@app.get("/search")
def search(q: str, k: int = 100):
    emb = model.encode([q], normalize_embeddings=True)
    D, I = index.search(emb, k)

    results = []
    
    for score, idx in zip(D[0], I[0]):
        # Filter Sederhana: Hanya ambil yang skornya di atas threshold
        if score < SIMILARITY_THRESHOLD:
            continue
            
        m = metadata[idx]
        
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
