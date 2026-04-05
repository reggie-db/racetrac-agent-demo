"""SQL helpers shared by notebooks and agent package demos."""

from common.config import DemoTableRefs


def create_schema_sql(catalog: str, schema: str) -> str:
    """Return SQL that ensures the demo schema exists."""
    return f"CREATE SCHEMA IF NOT EXISTS {catalog}.{schema}"


def table_select_sql(table_name: str, refs: DemoTableRefs) -> str:
    """Return a consistent select statement for demo exploration."""
    return f"SELECT * FROM {refs.fq_table(table_name)}"


def top_store_sales_sql(refs: DemoTableRefs) -> str:
    """Return an operations query for top stores by fuel sales and volume."""
    transactions_table = refs.fq_table(refs.transactions)
    return f"""
SELECT
  store_id,
  SUM(gross_sales) AS total_sales,
  SUM(gallons_sold) AS total_gallons,
  AVG(price_per_gallon) AS avg_price_per_gallon,
  COUNT(*) AS txn_count
FROM {transactions_table}
GROUP BY store_id
ORDER BY total_sales DESC
LIMIT 10
""".strip()


def pump_maintenance_forecast_view_sql(refs: DemoTableRefs) -> str:
    """Return SQL for a Genie-ready view forecasting pump downtime risk."""
    telemetry_table = refs.fq_table(refs.pump_telemetry)
    return f"""
CREATE OR REPLACE VIEW {refs.catalog}.{refs.schema}.vw_pump_maintenance_forecast AS
SELECT
  store_id,
  pump_id,
  DATE(event_ts) AS event_date,
  AVG(vibration_mm_s) AS avg_vibration_mm_s,
  AVG(line_pressure_psi) AS avg_pressure_psi,
  ai_forecast(
    AVG(vibration_mm_s),
    DATE(event_ts)
  ) OVER (PARTITION BY store_id, pump_id ORDER BY DATE(event_ts)) AS projected_vibration_risk
FROM {telemetry_table}
GROUP BY store_id, pump_id, DATE(event_ts)
""".strip()


def pump_maintenance_forecast_view_sql_without_ai(refs: DemoTableRefs) -> str:
    """Return SQL for Genie view when ai_forecast is unavailable."""
    telemetry_table = refs.fq_table(refs.pump_telemetry)
    return f"""
CREATE OR REPLACE VIEW {refs.catalog}.{refs.schema}.vw_pump_maintenance_forecast AS
SELECT
  store_id,
  pump_id,
  DATE(event_ts) AS event_date,
  AVG(vibration_mm_s) AS avg_vibration_mm_s,
  AVG(line_pressure_psi) AS avg_pressure_psi,
  AVG(vibration_mm_s) AS projected_vibration_risk
FROM {telemetry_table}
GROUP BY store_id, pump_id, DATE(event_ts)
""".strip()


def fuel_price_forecast_view_sql(refs: DemoTableRefs) -> str:
    """Return SQL for a Genie-ready view forecasting station fuel price bands."""
    transactions_table = refs.fq_table(refs.transactions)
    return f"""
CREATE OR REPLACE VIEW {refs.catalog}.{refs.schema}.vw_fuel_price_forecast AS
SELECT
  store_id,
  fuel_grade,
  DATE(transaction_ts) AS sale_date,
  AVG(price_per_gallon) AS avg_price_per_gallon,
  ai_forecast(
    AVG(price_per_gallon),
    DATE(transaction_ts)
  ) OVER (PARTITION BY store_id, fuel_grade ORDER BY DATE(transaction_ts)) AS projected_price_per_gallon
FROM {transactions_table}
GROUP BY store_id, fuel_grade, DATE(transaction_ts)
""".strip()


def fuel_price_forecast_view_sql_without_ai(refs: DemoTableRefs) -> str:
    """Return SQL for Genie view when ai_forecast is unavailable."""
    transactions_table = refs.fq_table(refs.transactions)
    return f"""
CREATE OR REPLACE VIEW {refs.catalog}.{refs.schema}.vw_fuel_price_forecast AS
SELECT
  store_id,
  fuel_grade,
  DATE(transaction_ts) AS sale_date,
  AVG(price_per_gallon) AS avg_price_per_gallon,
  AVG(price_per_gallon) AS projected_price_per_gallon
FROM {transactions_table}
GROUP BY store_id, fuel_grade, DATE(transaction_ts)
""".strip()
