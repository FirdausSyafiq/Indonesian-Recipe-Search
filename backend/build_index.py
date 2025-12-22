import pandas as pd
import numpy as np
import faiss
import json
from sentence_transformers import SentenceTransformer
import re

CSV_PATH = "../dataset/Indonesian_Food_Recipes.csv"   # ganti sesuai nama file dataset Anda
MODEL_NAME = "all-mpnet-base-v2"

def clean(s):
    if pd.isna(s): 
        return ""
    s = str(s).lower()
    s = re.sub(r'\s+', ' ', s)
    return s.strip()

def main():
    df = pd.read_csv(CSV_PATH)

    docs = []
    metadata = []

    for i, row in df.iterrows():

        # ambil kolom sesuai dataset
        title = clean(row["Title Cleaned"])
        ingredients = clean(row["Ingredients Cleaned"])
        steps = clean(row["Steps"])
        category = row.get("Category", "")

        # dokumen SBERT (yang dicari user)
        text = f"{title}. Ingredients: {ingredients}"

        docs.append(text)

        # metadata lengkap untuk ditampilkan di frontend
        metadata.append({
            "title": row["Title"],
            "ingredients": row["Ingredients"],
            "steps": row["Steps"],
            "url": row["URL"],
            "category": category,
            "total_ingredients": row.get("Total ingredients", None),
            "total_steps": row.get("Total Steps", None),
            "loves": row.get("Loves", None),
        })

    print("Loading model…")
    model = SentenceTransformer(MODEL_NAME)

    print("Creating embeddings…")
    embeddings = model.encode(
        docs,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    np.save("embeddings.npy", embeddings)

    with open("metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)

    d = embeddings.shape[1]
    index = faiss.IndexFlatIP(d)
    index.add(embeddings)

    faiss.write_index(index, "faiss.index")

    print("Index created successfully!")
    print("Total recipes indexed:", len(docs))

if __name__ == "__main__":
    main()
