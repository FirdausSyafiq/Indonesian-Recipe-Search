from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import faiss
import json
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-mpnet-base-v2"

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
def search(q: str, k: int = 30):
    emb = model.encode([q], normalize_embeddings=True)
    D, I = index.search(emb, k)

    results = []
    for score, idx in zip(D[0], I[0]):
        m = metadata[idx]
        results.append({
            "title": m["title"],
            "ingredients": m["ingredients"],
            "steps": m["steps"],
            "url": m["url"],
            "category": m["category"],
            "score": float(score),
            "total_ingredients": m["total_ingredients"],
            "total_steps": m["total_steps"],
            "loves": m["loves"]
        })

    return results
