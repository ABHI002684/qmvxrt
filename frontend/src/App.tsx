
import { useEffect, useState } from "react";
import {
  Activity,
  AlertCircle,
  BarChart3,
  CalendarDays,
  CheckCircle2,
  Clock3,
  Cloud,
  Gauge,
  RefreshCw,
  Target,
  TrendingUp,
  Wind,
} from "lucide-react";

import MetricCard from "./components/MetricCard";
import GenerationChart from "./components/GenerationChart";
import ResultsTable from "./components/ResultsTable";
import { fetchAnalysis } from "./services/analysisService";
import type { AnalysisResponse } from "./types/analysis";
import "./App.css";

function App() {
  const [date, setDate] = useState("2026-01-15");
  const [analysis, setAnalysis] = useState<AnalysisResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function loadAnalysis() {
      setLoading(true);
      setError(null);

      try {
        const data = await fetchAnalysis(date, "10:00");

        if (!cancelled) {
          setAnalysis(data);
        }
      } catch (err) {
        if (!cancelled) {
          setError(
            err instanceof Error
              ? err.message
              : "Unable to load wind forecast analysis.",
          );
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    void loadAnalysis();

    return () => {
      cancelled = true;
    };
  }, [date]);

  const metrics = analysis?.metrics;

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">
            <Wind size={23} />
          </div>
          <div>
            <h1>WindScope</h1>
            <span>Forecast intelligence</span>
          </div>
        </div>

        <div className="sidebar-section-label">WORKSPACE</div>

        <nav className="sidebar-nav">
          <a className="nav-link active" href="#overview">
            <BarChart3 size={18} />
            Overview
          </a>
          <a className="nav-link" href="#analysis">
            <Activity size={18} />
            Forecast analysis
          </a>
        </nav>

        <div className="sidebar-bottom">
          <div className="connection-indicator">
            <span className="status-dot" />
            <div>
              <strong>Elexon BMRS</strong>
              <span>Data source</span>
            </div>
          </div>
          <p>Wind generation analytics</p>
        </div>
      </aside>

      <main className="main-content" id="overview">
        <header className="topbar">
          <div className="breadcrumbs">
            Workspace <span>/</span> Overview
          </div>
          <div className="api-status">
            <span className="status-dot" />
            API connected
          </div>
        </header>

        <section className="page-heading">
          <div>
            <div className="eyebrow">
              <Wind size={15} />
              RENEWABLE ENERGY INTELLIGENCE
            </div>
            <h2>Wind forecast overview</h2>
            <p>
              Compare predicted wind generation against actual output across
              the Great Britain electricity system.
            </p>
          </div>

          <label className="date-control">
            <CalendarDays size={17} />
            <span>Delivery date</span>
            <input
              aria-label="Delivery date"
              type="date"
              min="2026-01-01"
              max="2026-01-31"
              value={date}
              onChange={(event) => setDate(event.target.value)}
            />
          </label>
        </section>

        <div className="notice-banner">
          <AlertCircle size={19} />
          <div>
            <strong>Provisional analysis</strong>
            <p>
              Historical forecast selection and delivery-period coverage
              require further validation. Treat these metrics as indicative,
              not as a verified benchmark.
            </p>
          </div>
        </div>

        <section className="overview-strip">
          <div className="overview-item">
            <div className="overview-icon">
              <CalendarDays size={18} />
            </div>
            <div>
              <span>Delivery date</span>
              <strong>{date}</strong>
            </div>
          </div>

          <div className="overview-item">
            <div className="overview-icon">
              <Clock3 size={18} />
            </div>
            <div>
              <span>Forecast cutoff</span>
              <strong>10:00 UK time</strong>
            </div>
          </div>

          <div className="overview-item">
            <div className="overview-icon">
              <CheckCircle2 size={18} />
            </div>
            <div>
              <span>Matched periods</span>
              <strong>{analysis?.metrics.periods ?? "—"}</strong>
            </div>
          </div>

          <div className="overview-item">
            <div className="overview-icon">
              <Cloud size={18} />
            </div>
            <div>
              <span>Data provider</span>
              <strong>Elexon BMRS</strong>
            </div>
          </div>
        </section>

        <section className="section-block" id="analysis">
          <div className="section-heading">
            <div>
              <h3>Forecast performance</h3>
              <p>Accuracy indicators calculated from matched observations.</p>
            </div>
            {loading && (
              <span className="loading-label">
                <RefreshCw size={14} className="spin" />
                Updating
              </span>
            )}
          </div>

          {error && (
            <div className="error-banner" role="alert">
              <AlertCircle size={19} />
              <div>
                <strong>Unable to load analysis</strong>
                <p>{error}</p>
                <button
                  type="button"
                  className="retry-button"
                  onClick={() => setDate((current) => current)}
                >
                  Retry by selecting another date
                </button>
              </div>
            </div>
          )}

          <div className="metrics-grid">
            <MetricCard
              label="Mean absolute error"
              value={metrics?.mae ?? null}
              unit="MW"
              description="Average absolute forecast error"
              icon={Target}
            />
            <MetricCard
              label="Root mean squared error"
              value={metrics?.rmse ?? null}
              unit="MW"
              description="Penalises larger errors"
              icon={Gauge}
            />
            <MetricCard
              label="Forecast bias"
              value={metrics?.bias ?? null}
              unit="MW"
              description="Positive means overforecast"
              icon={TrendingUp}
            />
            <MetricCard
              label="Weighted absolute error"
              value={metrics?.wape ?? null}
              unit="%"
              description="Error relative to actual output"
              icon={Activity}
            />
          </div>
        </section>

        <section className="panel chart-panel">
          <div className="panel-heading">
            <div>
              <h3>Actual vs forecast generation</h3>
              <p>Hourly wind generation · MW · All times UTC</p>
            </div>
            <div className="chart-legend">
              <span><i className="legend-actual" /> Actual</span>
              <span><i className="legend-forecast" /> Forecast</span>
            </div>
          </div>

          {loading && !analysis ? (
            <div className="empty-state">Loading generation data…</div>
          ) : error && !analysis ? (
            <div className="empty-state">Chart unavailable until the API responds.</div>
          ) : analysis?.results.length ? (
            <GenerationChart results={analysis.results} />
          ) : (
            <div className="empty-state">No matched generation data for this date.</div>
          )}
        </section>

        <section className="panel results-panel">
          <div className="panel-heading">
            <div>
              <h3>Hourly breakdown</h3>
              <p>Observed generation, selected forecast and signed error.</p>
            </div>
            <span className="record-count">
              {analysis?.results.length ?? 0} records
            </span>
          </div>

          {analysis?.results.length ? (
            <ResultsTable results={analysis.results} />
          ) : (
            <div className="empty-state">
              {loading ? "Loading results…" : "No results available."}
            </div>
          )}
        </section>

        <footer className="page-footer">
          <span>WindScope · Wind generation forecast analysis</span>
          <span>Source: Elexon BMRS API</span>
        </footer>
      </main>
    </div>
  );
}

export default App;
