# Databricks notebook source

from _bootstrap import bootstrap_local_packages, configure_logging, get_spark_session

"""Create Genie-friendly forecast views for pump maintenance and fuel pricing."""

bootstrap_local_packages()
configure_logging()

from common.config import DemoTableRefs  # noqa: E402
from common.sql import (  # noqa: E402
    fuel_price_forecast_view_sql_without_ai,
    fuel_price_forecast_view_sql,
    pump_maintenance_forecast_view_sql_without_ai,
    pump_maintenance_forecast_view_sql,
)
from lfp_logging import logs  # noqa: E402

LOG = logs.logger()
spark = get_spark_session()
refs = DemoTableRefs()

maintenance_sql = pump_maintenance_forecast_view_sql(refs)
pricing_sql = fuel_price_forecast_view_sql(refs)

# These views are intended for Genie space exploration.
try:
    spark.sql(maintenance_sql)
    spark.sql(pricing_sql)
except Exception as exc:
    if "UNRESOLVED_ROUTINE" not in str(exc) or "ai_forecast" not in str(exc):
        raise
    LOG.warning("ai_forecast is unavailable; creating fallback forecast views.")
    spark.sql(pump_maintenance_forecast_view_sql_without_ai(refs))
    spark.sql(fuel_price_forecast_view_sql_without_ai(refs))
LOG.info(
    "Created forecast views for Genie in %s.%s",
    refs.catalog,
    refs.schema,
)
