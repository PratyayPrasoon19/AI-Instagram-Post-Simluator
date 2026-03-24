# AI-Instagram-Post-Simluator

System to generate Instagram posts and simulate posting using AI agents.

## Features

- Generate Instagram caption (max ~150 words), hashtags, and an image.
- Simulate posting with `/post/{post_id}`.
- View post history with `/history`.
- Vue.js frontend to:
  - Enter topic + tone.
  - Generate post via `/generate-post`.
  - Preview a realistic Instagram-style card.
  - Trigger simulated posting and redirect to a dedicated posted-page route.
  - View generated history and open any history item in an Instagram-style popup modal.

## Backend (FastAPI)

### Run

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Backend runs at `http://localhost:8000`.

## Frontend (Vue + Vite)

### Run

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`.

### Environment

You can optionally set backend base URL:

```bash
# frontend/.env
VITE_API_BASE_URL=http://localhost:8000
```

## API Endpoints

- `POST /generate-post`
  - Body: `{ "topic": "...", "tone": "professional|casual" }`
- `POST /post/{post_id}`
- `GET /history`

Generated images are served from `/generated/...` paths.
