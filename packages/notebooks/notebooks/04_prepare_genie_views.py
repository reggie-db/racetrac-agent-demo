# Databricks notebook source

from _bootstrap import bootstrap_local_packages, configure_logging, get_spark_session

"""Create Genie-friendly forecast views for pump maintenance and fuel pricing."""

bootstrap_local_packages()
configure_logging()

from common.config import DemoTableRefs  # noqa: E402
from common.sql import (  # noqa: E402
    fuel_price_forecast_view_sql,
    pump_maintenance_forecast_view_sql,
)
from lfp_logging import logs  # noqa: E402

LOG = logs.logger()
spark = get_spark_session()
refs = DemoTableRefs()

maintenance_sql = pump_maintenance_forecast_view_sql(refs)
pricing_sql = fuel_price_forecast_view_sql(refs)

# These views are intended for Genie space exploration and include ai_forecast.
spark.sql(maintenance_sql)
spark.sql(pricing_sql)
LOG.info(
    "Created forecast views for Genie in %s.%s",
    refs.catalog,
    refs.schema,
)
