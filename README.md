# WindScope — Wind Forecast Analytics

WindScope is a full-stack analytics dashboard for comparing forecast wind generation against actual generation in the Great Britain electricity system. It retrieves data from the Elexon BMRS API, processes matched observations in a FastAPI backend, and presents forecast performance metrics and hourly comparisons in a React dashboard.

> **Status:** MVP in development. Historical forecast selection and delivery-period coverage are still being validated. Results should be treated as provisional.

## Features

- Retrieve wind forecast and actual generation data from Elexon BMRS.
- Compare forecast generation against observed generation.
- Calculate mean absolute error (MAE), root mean squared error (RMSE), forecast bias, and weighted absolute percentage error (WAPE).
- Display actual versus forecast generation in an interactive chart.
- Explore hourly results in a tabular view.
- Select a delivery date from the dashboard.

## Technology Stack

**Backend**
- Python
- FastAPI
- HTTPX
- Pandas
- Pytest

**Frontend**
- React
- TypeScript
- Vite
- Recharts
- Lucide React

**Data source:** [Elexon BMRS API](https://data.elexon.co.uk/bmrs/api/v1)

## Project Structure

```text
wind-forecast-portal/
├── backend/
│   ├── app/
│   │   ├── api/routes/
│   │   ├── core/
│   │   ├── integrations/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── main.py
│   ├── tests/
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── components/
    │   ├── services/
    │   ├── types/
    │   ├── App.tsx
    │   └── main.tsx
    ├── package.json
    └── vite.config.ts
```

## Prerequisites

- Python 3.11 or another compatible Python version.
- Node.js and npm.
- Internet access to retrieve data from Elexon BMRS.

## Run Locally

### 1. Start the backend

Open a terminal:

```powershell
cd backend
python -m pip install -r requirements.txt
python app/main.py
```

The API should be available at `http://localhost:8000`.

Health check:

```text
http://localhost:8000/api/health
```

### 2. Start the frontend

Open a second terminal from the repository root:

```powershell
cd frontend
npm install
npm run dev
```

Open the local URL printed by Vite, usually `http://localhost:5173`.

The frontend currently requests the API from `http://localhost:8000/api`.

## API Usage

### Health check

```http
GET /api/health
```

### Forecast analysis

```http
GET /api/analysis?date=2026-01-15&cutoff=10:00
```

The analysis endpoint returns the target date, forecast cutoff, aggregate metrics, and matched hourly results.

The currently supported analysis date range is restricted to January 2026.

## Forecast Metrics

| Metric | Meaning |
|---|---|
| MAE | Mean absolute difference between forecast and actual generation, in MW |
| RMSE | Square root of the mean squared forecast error, in MW |
| Bias | Mean signed error, defined as forecast minus actual, in MW |
| WAPE | Sum of absolute errors divided by the sum of absolute actual generation, expressed as a percentage |

A positive bias indicates that forecasts are higher than actual generation on average; a negative bias indicates underforecasting.

## Testing

Run backend tests from the backend directory:

```powershell
python -m pytest -q
```

Build the frontend from the frontend directory:

```powershell
npm run build
```

## Limitations and Next Steps

- Validate historical forecast-vintage selection against the specified cutoff.
- Verify that delivery periods align exactly with the requested target date.
- Validate hourly aggregation of half-hourly actual generation.
- Expand automated tests for API integration, date boundaries, and metric calculations.
- Configure production API URLs and deployment settings before hosting.

## License

See the repository's `LICENSE` file for licensing terms.
