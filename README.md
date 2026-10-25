# WindScope — Wind Forecast Analytics

**Live application:** https://qmvxrt.vercel.app/

**Backend API:** https://wind-forecast-api-oare.onrender.com
**API health check:** https://wind-forecast-api-oare.onrender.com/api/health

## Overview

WindScope is a full-stack analytics application designed to help a UK electricity utility evaluate national wind generation forecasts when making day-ahead electricity procurement decisions.

The application retrieves actual wind generation and forecast data from the Elexon BMRS API, selects forecasts according to a publication-time cutoff, aligns actual and forecast values by delivery hour, and calculates quantitative forecast error metrics.

The dashboard presents summary metrics, an actual-versus-forecast chart, and hourly comparison results.

**Analysis status:** The application is a pilot implementation. Historical forecast-vintage selection, publication-time coverage, and evaluation methodology require further validation. The displayed metrics should be treated as provisional, not as a verified forecasting benchmark.

## Features

- Retrieve actual wind generation and wind forecasts from Elexon BMRS.
- Apply a forecast publication-time cutoff to model information available when a decision is made.
- Select the latest eligible forecast vintage for each delivery period.
- Aggregate half-hourly actual generation into hourly values for comparison with hourly forecasts.
- Calculate MAE, RMSE, forecast bias, and WAPE.
- Visualize actual and forecast generation with an interactive chart.
- Inspect hourly actuals, forecasts, errors, and forecast publication times.
- Expose health and analysis endpoints through a FastAPI REST API.
- Run locally using Docker Compose or through separate backend and frontend development servers.

## Technology Stack

| Area | Technologies |
|---|---|
| Frontend | React, TypeScript, Vite |
| Charts and icons | Recharts, Lucide React |
| Backend | Python, FastAPI, Uvicorn |
| HTTP client and data processing | HTTPX, Pandas |
| Data validation and testing | Pydantic, Pytest |
| Data source | Elexon BMRS API |
| Containers | Docker, Docker Compose, Nginx |
| Deployment | Vercel (frontend), Render (backend) |

## Project Structure

```text
wind-forecast-portal/
├── backend/
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── .env.example
│   ├── requirements.txt
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   │   └── routes/
│   │   │       ├── analysis.py
│   │   │       ├── debug.py
│   │   │       └── health.py
│   │   ├── core/
│   │   │   └── config.py
│   │   ├── integrations/
│   │   │   └── elexon_client.py
│   │   ├── schemas/
│   │   │   └── analysis.py
│   │   └── services/
│   │       ├── analysis_service.py
│   │       ├── forecast_selection.py
│   │       └── metrics.py
│   └── tests/
│       ├── test_metrics.py
│       ├── test_forecast_selection.py
│       └── test_forecast_cutoff.py
├── frontend/
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── .env.example
│   ├── package.json
│   ├── package-lock.json
│   ├── index.html
│   ├── vite.config.ts
│   └── src/
│       ├── components/
│       │   ├── MetricCard.tsx
│       │   ├── GenerationChart.tsx
│       │   └── ResultsTable.tsx
│       ├── services/
│       │   └── analysisService.ts
│       ├── types/
│       │   └── analysis.ts
│       ├── App.tsx
│       ├── App.css
│       ├── index.css
│       └── main.tsx
├── docker-compose.yml
├── .gitignore
├── LICENSE
└── README.md
```

The tree highlights the principal application files; additional configuration and supporting files may exist.

## Prerequisites

For the local development setup:

- Python 3.11 or another compatible Python version.
- Node.js and npm.
- Internet access to retrieve data from Elexon BMRS.

For the containerized setup:

- Docker Engine or another compatible Docker installation.
- Docker Compose.

## Run with Docker

From the repository root:

```bash
docker compose up --build
```

Docker builds the backend and frontend images and starts both services.

Open the application at:

- **Dashboard:** http://localhost
- **Backend health:** http://localhost:8000/api/health
- **Interactive API documentation:** http://localhost:8000/docs

To stop the services, press `Ctrl+C`, then run:

```bash
docker compose down
```

To rebuild after source or dependency changes:

```bash
docker compose up --build
```

The frontend image uses Nginx to serve the compiled React application. Its API URL is supplied at image build time through `VITE_API_BASE_URL`.

## Run Locally Without Docker

### Backend

From the repository root, open a terminal and run:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app/main.py
```

The backend should be available at `http://localhost:8000`.

### Frontend

Open a second terminal at the repository root:

```powershell
cd frontend
npm ci
```

Ensure the local `frontend/.env` file contains:

```dotenv
VITE_API_BASE_URL=http://localhost:8000
```

Start the development server:

```powershell
npm run dev
```

Open the URL shown by Vite, normally http://localhost:5173.

The backend must be running for the dashboard to retrieve analysis results.

## Data Source

The application uses the [Elexon BMRS API](https://data.elexon.co.uk/bmrs/api/v1) and restricts the analysis to national wind generation data available from Elexon.

- **FUELHH:** Actual generation observations. Records with `fuelType = WIND` are used. Actuals are reported at half-hourly resolution.
- **WINDFOR:** Wind generation forecasts. Relevant fields include `startTime`, `publishTime`, and `generation`.

Actual observations are aggregated to hourly values to align with the hourly forecast data used by the application.

## Forecast Evaluation Methodology

For a delivery date and decision cutoff, the application:

1. Retrieves wind actuals and forecast observations from Elexon.
2. Excludes forecast publications later than the specified cutoff.
3. Selects the latest eligible forecast vintage for each delivery period.
4. Aggregates half-hourly actual generation to hourly values.
5. Matches actual and forecast observations by delivery hour.
6. Calculates the forecast error metrics from matched observations.

The current implementation supports delivery dates in January 2026. Full validation of historical forecast availability and publication-time filtering remains outstanding.

## Metrics

| Metric | Definition |
|---|---|
| MAE | Mean absolute error, in MW |
| RMSE | Root mean squared error, in MW |
| Bias | Mean signed error, defined as forecast minus actual, in MW |
| WAPE | Sum of absolute errors divided by the sum of actual generation, expressed as a percentage |

A positive bias indicates overforecasting on average; a negative bias indicates underforecasting.

These metrics quantify forecast error. They do not by themselves prescribe how much electricity the utility should buy, because procurement decisions also depend on demand, market prices, and other operational constraints outside this prototype's scope.

## API Endpoints

### Health check

```http
GET /api/health
```

### Forecast analysis

```http
GET /api/analysis?date=2026-01-15&cutoff=10:00
```

The analysis endpoint returns the target date, cutoff timestamp, aggregate metrics, and hourly results.

The current prototype restricts supported delivery dates to January 2026.

## Testing

Run backend tests:

```powershell
cd backend
$env:PYTHONPATH = "."
python -m pytest -q
```

Build the frontend:

```powershell
cd frontend
npm ci
npm run build
```

The automated backend tests cover metric calculations, forecast vintage selection, and cutoff behavior.

## Deployment

### Frontend — Vercel

- Application: https://qmvxrt.vercel.app/
- Root directory: `frontend`
- Build command: `npm run build`
- Output directory: `dist`
- Environment variable: `VITE_API_BASE_URL=https://wind-forecast-api-oare.onrender.com`

### Backend — Render

- API base URL: https://wind-forecast-api-oare.onrender.com
- Root directory: `backend`
- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

Configure `CORS_ORIGINS` in Render to include the deployed Vercel origin and any required local development origins.

The free Render instance may spin down after inactivity, increasing the response time of the first request.

## Known Limitations

- Forecast-vintage selection and historical data coverage need further validation.
- The supported delivery date range is currently limited to January 2026.
- Half-hourly actuals are aggregated into hourly values.
- External API availability and free-hosting cold starts can affect response time.
- The metrics are provisional and are not a verified forecasting benchmark.
- Procurement recommendations are outside the current scope; the app provides forecast information and error quantification.

## AI Assistance

The application architecture, core business logic, data processing workflows, forecast selection methodology, and evaluation metrics were independently designed and implemented by me. AI tools were used as supplementary development aids for code refinement, improving readability and consistency, and polishing documentation. All technical decisions, implementation choices, and validation of the application were reviewed and remain my responsibility.
## License

Refer to the repository's `LICENSE` file for the applicable terms.
