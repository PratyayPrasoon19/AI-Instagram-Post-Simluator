# AI-Instagram-Post-Simluator

System to generate Instagram posts and simulate posting using AI agents.

## Frontend (React + Vite)

A production-ready frontend has been added in the `frontend` folder.

### Features
- Topic + tone input (`professional` / `casual`)
- Calls backend `POST /generate-post`
- Displays generated caption (with word count), hashtags, and image
- Instagram-style post preview simulation
- Calls backend `POST /post` to simulate posting
- Shows locally tracked stored/simulated posts list

### Run frontend locally

```bash
cd frontend
npm install
npm run dev
```

The app expects the backend at `http://localhost:3000` by default.

To use another backend URL:

```bash
cd frontend
VITE_API_BASE_URL=http://localhost:8000 npm run dev
```
