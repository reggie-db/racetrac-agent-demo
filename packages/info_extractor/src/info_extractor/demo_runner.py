"""Entrypoint for the information extraction brick demo."""

from info_extractor.agent import InfoExtractorAgent
from lfp_logging import logs

LOG = logs.logger()


def run_info_extractor_demo() -> dict[str, str]:
    """Run extraction over a realistic RaceTrac pump operations update."""
    message = (
        "RT-214 reported urgent pump motor fault with repeated breakdown events. "
        "Major concern during morning commute and fueling downtime climbed above normal."
    )
    signal = InfoExtractorAgent().extract(message=message)
    LOG.info("Info extractor output store_id=%s", signal.store_id)
    return signal.model_dump()
