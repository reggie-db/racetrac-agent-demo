# Databricks notebook source

from _bootstrap import bootstrap_local_packages, configure_logging, render_output

"""Run info extraction over a realistic pump operations update."""

bootstrap_local_packages()
configure_logging()

from info_extractor.agent import InfoExtractorAgent  # noqa: E402
from lfp_logging import logs  # noqa: E402

LOG = logs.logger()

sample_update = (
    "RT-331 urgent pump pressure fault on dispenser island. "
    "Repeated breakdown alarms indicate escalating downtime risk."
)
signal = InfoExtractorAgent().extract(message=sample_update)
LOG.info(
    "Signal extracted for store=%s category=%s severity=%s",
    signal.store_id,
    signal.category,
    signal.severity,
)
render_output(signal.model_dump(), display_fn=globals().get("display"))
