"""Entrypoint for the supervisor orchestration brick demo."""

from common.dummy_data import generate_knowledge_docs
from lfp_logging import logs

from supervisor.agent import SupervisorAgent

LOG = logs.logger()


def run_supervisor_demo() -> dict[str, object]:
    """Generate a daily digest across demo brick outputs."""
    docs = generate_knowledge_docs(row_count=50)
    store_update = (
        "RT-305 flagged critical pump motor degradation and repeated "
        "breakdown alarms with rising fuel-demand volatility."
    )
    digest = SupervisorAgent().build_digest(docs=docs, store_update=store_update)
    LOG.info("Supervisor digest date=%s", digest.date_key)
    return digest.model_dump()
