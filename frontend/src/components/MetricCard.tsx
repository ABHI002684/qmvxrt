
import type { LucideIcon } from "lucide-react";

interface MetricCardProps {
  label: string;
  value: number | null;
  unit: string;
  description: string;
  icon: LucideIcon;
}

export default function MetricCard({
  label,
  value,
  unit,
  description,
  icon: Icon,
}: MetricCardProps) {
  const formattedValue =
    value === null || !Number.isFinite(value)
      ? "—"
      : value.toLocaleString("en-GB", {
          maximumFractionDigits: 1,
          minimumFractionDigits: 1,
        });

  return (
    <article className="metric-card">
      <div className="metric-top">
        <span>{label}</span>
        <div className="metric-icon">
          <Icon size={18} />
        </div>
      </div>

      <div className="metric-value">
        {formattedValue}
        <span>{unit}</span>
      </div>

      <div className="metric-footer">{description}</div>
    </article>
  );
}
