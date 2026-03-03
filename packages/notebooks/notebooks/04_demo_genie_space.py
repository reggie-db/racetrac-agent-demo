# Databricks notebook source

from _bootstrap import bootstrap_local_packages, configure_logging, render_output

"""Generate Genie-style SQL for pump maintenance and fuel pricing questions."""

bootstrap_local_packages()
configure_logging()

from common.config import DemoTableRefs  # noqa: E402
from common.sql import fuel_price_forecast_view_sql, pump_maintenance_forecast_view_sql  # noqa: E402
from genie_space.agent import GenieSpaceAgent  # noqa: E402
from lfp_logging import logs  # noqa: E402

LOG = logs.logger()

refs = DemoTableRefs()
prompt = "Which pumps have highest maintenance risk and where is fuel pricing projected to rise?"
sql_statement = GenieSpaceAgent().build_sql(prompt=prompt)
maintenance_view_sql = pump_maintenance_forecast_view_sql(refs)
pricing_view_sql = fuel_price_forecast_view_sql(refs)
LOG.info("Generated SQL for prompt: %s", prompt)
render_output(
    {
        "prompt": prompt,
        "sql": sql_statement,
        "maintenance_forecast_view_sql": maintenance_view_sql,
        "fuel_price_forecast_view_sql": pricing_view_sql,
    },
    display_fn=globals().get("display"),
)
