# Indonesian-Recipe-Search

Cara Install :
1. Pada terminal backend ketik :
    python -m venv venv
    venv\Scripts\activate
2. Ketik juga :
   pip install fastapi uvicorn[standard] sentence-transformers faiss-cpu pandas numpy
3. Terakhir ketik :
   python build_index.py
4. Pindah ke terminal frontend ketik :
   npm install

Untuk menjalankan web lakukan :
1. Jalankan backend ketik :
   uvicorn main:app --reload --port 8000
2. Seteleah backend berjalan, jalankan frontend ketik :
   npm run dev
