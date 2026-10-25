
import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import type { AnalysisResult } from "../types/analysis";

interface GenerationChartProps {
  results: AnalysisResult[];
}

function formatHour(period: string) {
  return new Date(period).toLocaleTimeString("en-GB", {
    hour: "2-digit",
    minute: "2-digit",
    timeZone: "UTC",
  });
}

export default function GenerationChart({
  results,
}: GenerationChartProps) {
  const chartData = results.map((item) => ({
    time: formatHour(item.period),
    actual: item.actual_mw,
    forecast: item.forecast_mw,
  }));

  return (
    <div className="chart-container">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart
          data={chartData}
          margin={{ top: 12, right: 18, left: 4, bottom: 4 }}
        >
          <CartesianGrid stroke="#e9edf3" strokeDasharray="4 4" />
          <XAxis
            dataKey="time"
            tick={{ fill: "#7b8798", fontSize: 11 }}
            axisLine={false}
            tickLine={false}
            minTickGap={22}
          />
          <YAxis
            tick={{ fill: "#7b8798", fontSize: 11 }}
            axisLine={false}
            tickLine={false}
            width={60}
          />
          <Tooltip
            formatter={(value) => [
              `${Number(value).toLocaleString("en-GB")} MW`,
            ]}
          />
          <Line
            type="monotone"
            dataKey="actual"
            name="Actual generation"
            stroke="#0f9f83"
            strokeWidth={2.5}
            dot={false}
            activeDot={{ r: 5 }}
          />
          <Line
            type="monotone"
            dataKey="forecast"
            name="Forecast generation"
            stroke="#5978e8"
            strokeWidth={2.5}
            dot={false}
            activeDot={{ r: 5 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
