# Backend – Flask + OpenAI Chat

## Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file (see `.env.example`):

```
OPENAI_API_KEY=sk-your-key-here
```

## Run

```bash
python app.py
```

Server runs at `http://127.0.0.1:5000`.

## API

### `POST /chat`

Request body (JSON):

- `message` (required): user message
- `session_id` (optional): conversation id; omit or use same value to keep one thread. Default: `"default"`

Example:

```bash
curl -X POST http://127.0.0.1:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!", "session_id": "user-123"}'
```

Response:

- `200`: `{ "reply": "assistant reply" }`
- `400`: missing `message`
- `503`: `OPENAI_API_KEY` not set
- `500`: OpenAI error

History is stored in memory per `session_id` and is sent to OpenAI with each request. It is lost when the server restarts.

**Test with frontend:** From the project root run `python -m http.server 8080` in the `frontend` folder, then open `http://localhost:8080`. Ensure this backend is running on port 5000 and `OPENAI_API_KEY` is set in `.env`.

### `GET /health`

Returns `{ "status": "ok" }`.
