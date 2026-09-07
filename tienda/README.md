# Tienda de Botellas

Aplicacion web para vender botellas de vidrio y plastico con React/Vite, FastAPI y MongoDB.

## Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

La API lee `../.env` y crea/usa la base `tienda` indicada por `MONGODB_DB_NAME`.

Seed opcional:

```bash
python scripts/seed.py
```

## Frontend

```bash
cd frontend
npm install
npm run dev
```

La UI consume `http://localhost:8000/api` por defecto.
