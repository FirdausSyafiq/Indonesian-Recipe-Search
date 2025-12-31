# Indonesian-Recipe-Search

## A. Instalasi Awal (Hanya Sekali)
Lakukan langkah ini hanya jika baru pertama kali download atau clone project ini.

### 1. Setup Backend
Buka terminal di folder root project, lalu masuk ke folder backend:
```bash
cd backend
```

Buat environment dan install library:
```bash
python -m venv venv
venv\Scripts\activate
pip install fastapi uvicorn[standard] sentence-transformers faiss-cpu pandas numpy
```

Build index pencarian (pastikan file dataset sudah ada):
```bash
python build_index.py
```

### 2. Setup Frontend
Buka terminal baru, masuk ke folder frontend:
```bash
cd frontend
```

Install dependencies:
```bash
npm install
```

---

## B. Cara Menjalankan (Setiap Kali Ingin Menggunakan)
Jika sudah pernah install, cukup lakukan langkah ini setiap menyalakan PC.

### Terminal 1 (Backend)
1. Buka terminal di folder project.
2. Masuk ke folder backend:
   ```bash
   cd backend
   ```
3. **PENTING:** Aktifkan virtual environment:
   ```powershell
   venv\Scripts\activate
   ```
   *(Pastikan muncul tulisan `(venv)` di kiri)*
4. Jalankan server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

### Terminal 2 (Frontend)
1. Buka terminal baru di folder project.
2. Masuk ke folder frontend:
   ```bash
   cd frontend
   ```
3. Jalankan web:
   ```bash
   npm run dev
   ```
4. Buka browser dan akses link yang muncul (biasanya `http://localhost:5173`).
