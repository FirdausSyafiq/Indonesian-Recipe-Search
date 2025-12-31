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
    for score, idx in zip(D[0], I[0]):
        # Filter skor minimum
        if score < 0.15:
            continue
            
        m = metadata[idx]
        
        # --- FILTER TAMBAHAN (KEYWORD MATCHING) ---
        # Karena Semantic Search terlalu "kreatif" (menganggap babi mirip kambing),
        # kita bantu dengan filter kata kunci sederhana untuk query pendek.
        
        query_lower = q.lower()
        title_lower = m["title"].lower()
        ingredients_lower = m["ingredients"].lower()
        
        # Jika query pendek (satu kata) dan skornya "meragukan" (di bawah 0.6),
        # pastikan setidaknya ada kemiripan kata (substring match)
        # PENGECUALIAN: Jangan filter jika query bahasa inggris (karena resepnya bahasa indonesia)
        # Ini dilema. "Pig" tidak ada di teks "Kambing", jadi harusnya terfilter.
        # "Chili" tidak ada di teks "Cabe", tapi kita mau ini muncul.
        
        # Strategi: Tampilkan skor di frontend untuk debug user (opsional), 
        # tapi di sini kita kembalikan apa adanya dulu karena memfilter "pig" 
        # secara hardcode akan merusak pencarian "chili" -> "cabe".
        
        results.append({
            "title": m["title"],
            "ingredients": m["ingredients"],
            "steps": m["steps"],
            "url": m["url"],
            "category": m["category"],
            "total_ingredients": m["total_ingredients"],
            "total_steps": m["total_steps"],
            "loves": m["loves"],
            "score": float(score)  # Sertakan skor agar user bisa lihat relevansinya
        })

    return results
