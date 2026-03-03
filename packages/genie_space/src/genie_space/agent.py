"""Genie-style SQL generation brick for Command the Floor analytics."""

from __future__ import annotations

from common.config import DemoTableRefs
from lfp_logging import logs

LOG = logs.logger()


class GenieSpaceAgent:
    """Translate user prompts into scoped SQL for pump-operations datasets."""

    def __init__(self, refs: DemoTableRefs | None = None) -> None:
        self._refs = refs or DemoTableRefs()

    def build_sql(self, prompt: str) -> str:
        """Return a deterministic SQL query for a supported prompt type."""
        lowered = prompt.lower()
        transactions = self._refs.fq_table(self._refs.transactions)
        pump_breakdowns = self._refs.fq_table(self._refs.pump_breakdowns)
        pump_telemetry = self._refs.fq_table(self._refs.pump_telemetry)

        if "breakdown" in lowered or "maintenance" in lowered:
            sql = f"""
SELECT
  store_id,
  pump_id,
  COUNT(*) AS breakdown_count,
  AVG(downtime_minutes) AS avg_downtime_minutes
FROM {pump_breakdowns}
GROUP BY store_id, pump_id
ORDER BY breakdown_count DESC
LIMIT 15
""".strip()
        elif "telemetry" in lowered or "pressure" in lowered or "flow" in lowered:
            sql = f"""
SELECT
  store_id,
  pump_id,
  AVG(line_pressure_psi) AS avg_pressure_psi,
  AVG(flow_rate_gpm) AS avg_flow_rate_gpm,
  AVG(vibration_mm_s) AS avg_vibration_mm_s
FROM {pump_telemetry}
GROUP BY store_id, pump_id
ORDER BY avg_vibration_mm_s DESC
LIMIT 20
""".strip()
        elif "pricing" in lowered or "forecast" in lowered:
            sql = f"""
SELECT
  store_id,
  fuel_grade,
  DATE(transaction_ts) AS sale_date,
  AVG(price_per_gallon) AS avg_price_per_gallon
FROM {transactions}
GROUP BY store_id, fuel_grade, DATE(transaction_ts)
ORDER BY sale_date DESC
LIMIT 40
""".strip()
        else:
            sql = f"""
SELECT
  store_id,
  fuel_grade,
  SUM(gross_sales) AS total_sales,
  SUM(gallons_sold) AS total_gallons,
  COUNT(*) AS txn_count
FROM {transactions}
GROUP BY store_id, fuel_grade
ORDER BY total_sales DESC
LIMIT 10
""".strip()

        LOG.info("Generated Genie SQL for prompt=%s", prompt)
        return sql
