# Databricks notebook source

from _bootstrap import bootstrap_local_packages, configure_logging, get_spark_session

"""Create default catalog/schema for the RaceTrac demo."""

bootstrap_local_packages()
configure_logging()

from common.config import DEFAULT_CATALOG, DEFAULT_SCHEMA  # noqa: E402
from common.sql import create_schema_sql  # noqa: E402
from lfp_logging import logs  # noqa: E402

LOG = logs.logger()
spark = get_spark_session()

spark.sql(f"CREATE CATALOG IF NOT EXISTS {DEFAULT_CATALOG}")
spark.sql(create_schema_sql(catalog=DEFAULT_CATALOG, schema=DEFAULT_SCHEMA))
LOG.info("Ensured schema exists: %s.%s", DEFAULT_CATALOG, DEFAULT_SCHEMA)
