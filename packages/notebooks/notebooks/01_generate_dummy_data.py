# Databricks notebook source

from _bootstrap import bootstrap_local_packages, configure_logging, get_spark_session

"""Generate and persist synthetic RaceTrac datasets used by all bricks."""

bootstrap_local_packages()
configure_logging()

from common.config import DemoTableRefs  # noqa: E402
from common.dummy_data import generate_all_demo_data  # noqa: E402
from common.metadata import build_metadata_sql  # noqa: E402
from lfp_logging import logs  # noqa: E402

LOG = logs.logger()
spark = get_spark_session()

refs = DemoTableRefs()
datasets = generate_all_demo_data()

for table_name, records in datasets.items():
    frame = spark.createDataFrame(records)
    frame.write.mode("overwrite").saveAsTable(refs.fq_table(table_name))
    LOG.info("Wrote %s rows to %s", len(records), refs.fq_table(table_name))

for metadata_statement in build_metadata_sql(refs):
    spark.sql(metadata_statement)
LOG.info("Applied rich table and column descriptions for demo datasets.")
