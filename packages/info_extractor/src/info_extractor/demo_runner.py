"""Entrypoint for the information extraction brick demo."""

from lfp_logging import logs

from info_extractor.agent import InfoExtractorAgent

LOG = logs.logger()


def run_info_extractor_demo() -> dict[str, object]:
    """Run extraction over a realistic RaceTrac pump operations update."""
    message = (
        "RT-214 pump 07 reported urgent motor pressure_fault with repeated breakdown events "
        "and 47 minutes of downtime during morning commute."
    )
    signal = InfoExtractorAgent().extract(message=message)
    LOG.info("Info extractor output store_id=%s", signal.store_id)
    return signal.model_dump()
