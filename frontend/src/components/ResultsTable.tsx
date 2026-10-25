
import type { AnalysisResult } from "../types/analysis";

interface ResultsTableProps {
  results: AnalysisResult[];
}

function formatNumber(value: number) {
  return value.toLocaleString("en-GB", {
    minimumFractionDigits: 1,
    maximumFractionDigits: 1,
  });
}

function formatHour(period: string) {
  return new Date(period).toLocaleTimeString("en-GB", {
    hour: "2-digit",
    minute: "2-digit",
    timeZone: "UTC",
  });
}

export default function ResultsTable({ results }: ResultsTableProps) {
  return (
    <div className="table-scroll">
      <table>
        <thead>
          <tr>
            <th>Delivery period (UTC)</th>
            <th>Actual (MW)</th>
            <th>Forecast (MW)</th>
            <th>Error (MW)</th>
            <th>Published (UTC)</th>
          </tr>
        </thead>

        <tbody>
          {results.map((item, index) => (
            <tr key={`${item.period}-${index}`}>
              <td className="period-cell">{formatHour(item.period)}</td>
              <td>{formatNumber(item.actual_mw)}</td>
              <td>{formatNumber(item.forecast_mw)}</td>
              <td
                className={
                  item.error_mw > 0 ? "error-positive" : "error-negative"
                }
              >
                {item.error_mw > 0 ? "+" : ""}
                {formatNumber(item.error_mw)}
              </td>
              <td>
                {new Date(item.publish_time).toLocaleString("en-GB", {
                  day: "2-digit",
                  month: "short",
                  hour: "2-digit",
                  minute: "2-digit",
                  timeZone: "UTC",
                })}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
