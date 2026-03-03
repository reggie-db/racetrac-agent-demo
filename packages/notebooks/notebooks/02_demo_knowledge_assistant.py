# Databricks notebook source

from _bootstrap import (
    bootstrap_local_packages,
    configure_logging,
    get_spark_session,
    render_output,
)

"""Run the knowledge assistant brick against synthetic knowledge docs."""

bootstrap_local_packages()
configure_logging()

from common.config import DemoTableRefs  # noqa: E402
from knowledge_assistant.agent import KnowledgeAssistantAgent  # noqa: E402
from lfp_logging import logs  # noqa: E402

LOG = logs.logger()
spark = get_spark_session()
refs = DemoTableRefs()
docs_rows = spark.table(refs.fq_table(refs.knowledge_docs)).collect()
documents = [
    {"doc_id": row["doc_id"], "title": row["title"], "content": row["content"]}
    for row in docs_rows
]

question = "How should the developer team start with pump maintenance and fuel forecasting demos?"
response = KnowledgeAssistantAgent().answer_question(
    query=question, documents=documents
)
LOG.info("Knowledge assistant response citations=%s", response["citations"])
render_output(response, display_fn=globals().get("display"))
