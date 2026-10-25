import type { AnalysisResponse } from "../types/analysis";

const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000"
).replace(/\/+$/, "") + "/api";

export async function fetchAnalysis(
  date: string,
  cutoff = "10:00",
): Promise<AnalysisResponse> {
  const params = new URLSearchParams({ date, cutoff });

  const response = await fetch(
    `${API_BASE_URL}/analysis?${params.toString()}`,
  );

  if (!response.ok) {
    const body = await response.json().catch(() => null);
    throw new Error(
      body?.detail ?? `Failed to fetch analysis (${response.status})`,
    );
  }

  return response.json() as Promise<AnalysisResponse>;
}