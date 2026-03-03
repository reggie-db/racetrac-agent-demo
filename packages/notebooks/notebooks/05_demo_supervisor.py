# Databricks notebook source

from _bootstrap import (
    bootstrap_local_packages,
    configure_logging,
    get_spark_session,
    render_output,
)

"""Run supervisor orchestration across all demo bricks."""

bootstrap_local_packages()
configure_logging()

from common.config import DemoTableRefs  # noqa: E402
from lfp_logging import logs  # noqa: E402
from supervisor.agent import SupervisorAgent  # noqa: E402

LOG = logs.logger()
spark = get_spark_session()
refs = DemoTableRefs()
docs_rows = spark.table(refs.fq_table(refs.knowledge_docs)).collect()
docs = [
    {"doc_id": row["doc_id"], "title": row["title"], "content": row["content"]}
    for row in docs_rows
]
store_update = (
    "RT-119 critical pump breakdowns and escalating pressure faults during rush hour. "
    "Need district escalation and same-day maintenance plan."
)

digest = SupervisorAgent().build_digest(docs=docs, store_update=store_update)
LOG.info("Supervisor digest generated for date=%s", digest.date_key)
render_output(digest.model_dump(), display_fn=globals().get("display"))
