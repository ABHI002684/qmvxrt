export interface AnalysisMetrics {
  periods: number;
  mae: number | null;
  rmse: number | null;
  bias: number | null;
  wape: number | null;
}

export interface AnalysisResult {
  period: string;
  actual_mw: number;
  forecast_mw: number;
  error_mw: number;
  publish_time: string;
}

export interface AnalysisResponse {
  target_date: string;
  cutoff: string;
  metrics: AnalysisMetrics;
  results: AnalysisResult[];
}