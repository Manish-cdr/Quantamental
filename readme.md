# Quantamental

A unified platform for **quants, traders, and researchers**. It brings together mathematical tools, AI-driven investment insights, market news, and a live-price CLI in one place.

> **Disclaimer:** Quantamental is a research and educational platform. It is **not financial advice**. Always do your own due diligence. The creators and contributors are not liable for any financial losses incurred from using this platform.

---

## Features

- **Mathematical tools for quants**: linear algebra, statistics, probability distributions, time series, optimization, calculus, Monte Carlo simulation, and Black-Scholes / implied volatility
- **AI investment advisor (Lysa)**: portfolio analysis with recommendations, risk assessment, and suggested allocations
- **Finance news**: latest market headlines via NewsAPI
- **CLI**: real-time price streaming from Finnhub's websocket
- **Web dashboard**: Next.js frontend tying everything together

## Architecture

| Component    | Folder         | Tech                    | Default port |
| ------------ | -------------- | ----------------------- | ------------ |
| Frontend     | `frontend/`    | Next.js, TypeScript, shadcn/ui | 3000 |
| Backend API  | `backend/`     | Go, Gin                 | 8000         |
| AI service   | `ai_services/` | Python, FastAPI, OpenRouter | 5000     |
| CLI          | `cli/`         | Rust                    | n/a          |

## Prerequisites

- [Go](https://go.dev/dl/) 1.23+
- [Python](https://www.python.org/downloads/) 3.12+
- [Bun](https://bun.sh/) (or Node.js 20+ with npm)
- [Rust & Cargo](https://www.rust-lang.org/tools/install) (only for the CLI)

API keys (all have free tiers, except where noted):

- [NewsAPI](https://newsapi.org/): finance news
- [OpenRouter](https://openrouter.ai/keys): AI service (some models need a small credit balance)
- [Finnhub](https://finnhub.io/): CLI live prices

## Getting started

Clone the repo and run each service in its own terminal.

```bash
git clone https://github.com/Manish-cdr/Quantamental.git
cd Quantamental
```

### 1. Backend (Go, port 8000)

```bash
cd backend
cp .env.sample .env        # then set NEWS_API_KEY in .env
go run ./cmd/server
```

Check it: `curl http://localhost:8000/api/mathematicaltools`

### 2. AI service (Python, port 5000)

```bash
cd ai_services
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt python-dotenv
cp .env.sample .env                # then fill in the values below
python main.py
```

`ai_services/.env`:

```
OPENROUTER_API_KEY=your_key
OPENROUTER_MODEL=openai/gpt-oss-20b
ALLOWED_ORIGINS=http://localhost:3000
```

Interactive API docs: http://localhost:5000/docs

### 3. Frontend (Next.js, port 3000)

Create `frontend/.env.local`:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_API_AI_URL=http://localhost:5000
```

```bash
cd frontend
bun install
bun run dev        # or: npm install && npm run dev
```

Open http://localhost:3000. Restart the dev server after changing any `.env` file.

### 4. CLI (Rust, optional)

```bash
cd cli
cargo run -- --token YOUR_FINNHUB_TOKEN --symbols "AAPL,TSLA"
```

For crypto, use symbols like `BINANCE:BTCUSDT`.

## Environment variables

| Variable | Used by | Purpose |
| --- | --- | --- |
| `NEWS_API_KEY` | backend | NewsAPI key for `/api/finance/news` |
| `OPENROUTER_API_KEY` | ai_services | OpenRouter key |
| `OPENROUTER_MODEL` | ai_services | Model slug (see note below) |
| `ALLOWED_ORIGINS` | ai_services | Comma-separated CORS origins; must include the frontend URL |
| `NEXT_PUBLIC_API_URL` | frontend | Go backend base URL |
| `NEXT_PUBLIC_API_AI_URL` | frontend | AI service base URL |
| `FINHUB_API_KEY` | cli | Finnhub token |

> **Never commit `.env` files or real keys.** Only the blank `.env.sample` files belong in the repo.

## API overview

Full request bodies are in [`docs/backend/Mathematical Tools API.md`](docs/backend/Mathematical%20Tools%20API.md) and [`docs/ai services/Request.md`](docs/ai%20services/Request.md).

**Backend (`:8000`)**

- `GET /api/mathematicaltools`
- `POST /api/linear/matrix-multiply`, `/api/linear/matrix-inverse`
- `POST /api/stats/descriptive`, `/api/stats/correlation`
- `POST /api/dist/normal-pdf`, `/api/dist/normal-cdf`
- `POST /api/timeseries/moving-average`, `/api/timeseries/exponential-average`
- `POST /api/opt/golden-section`
- `POST /api/finmath/black-scholes`, `/api/finmath/implied-volatility`
- `POST /api/calculus/derivative`, `/api/calculus/integral`
- `POST /api/sim/monte-carlo`
- `GET /api/finance/news`

**AI service (`:5000`)**

- `GET /health`
- `POST /analyze-portfolio`
- `GET /market-summary`

## Troubleshooting

| Problem | Fix |
| --- | --- |
| `panic: NEWS_API_KEY environment variable is required` | Create `backend/.env` and save it as plain UTF-8/ASCII. On Windows PowerShell use `Set-Content -Encoding ascii .env "NEWS_API_KEY=..."`. |
| `OPTIONS /analyze-portfolio 400 Bad Request` | CORS. Set `ALLOWED_ORIGINS=http://localhost:3000` in `ai_services/.env` and fully restart the service. |
| Frontend fetch goes to `undefined/...` | `frontend/.env.local` is missing or misnamed. Restart `bun run dev`. |
| AI service returns 404 for the model | Free model slugs change. Set `OPENROUTER_MODEL` to a currently available slug. |
| `ModuleNotFoundError: dotenv` | `pip install python-dotenv` |

> The model is configured in `ai_services/config.py` as
> `DEFAULT_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-oss-20b")`.

## Project structure

```
Quantamental/
├── ai_services/   # FastAPI service (Lysa AI advisor)
├── backend/       # Go + Gin REST API (math tools, news)
├── cli/           # Rust live-price CLI
├── frontend/      # Next.js web app
├── docs/          # API and setup docs
├── infra/         # Docker compose
└── tests/         # Connection test scripts
```

## Docker

`infra/docker-compose.yaml` builds the backend and frontend. Note that it does not currently pass `NEWS_API_KEY` to the backend, and the browser cannot resolve the `backend` hostname used for `NEXT_PUBLIC_API_URL`. Running locally as described above is the recommended path for now.

## License

Add a license of your choice (for example MIT) as `LICENSE` in the repo root.
