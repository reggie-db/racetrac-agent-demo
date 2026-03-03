"""Entrypoint for demonstrating the Genie space brick."""

from common.config import DemoTableRefs
from lfp_logging import logs

from genie_space.agent import GenieSpaceAgent

LOG = logs.logger()


def run_genie_demo() -> dict[str, str]:
    """Build one SQL query from a business-facing operations prompt."""
    prompt = "Show pumps with highest breakdown count and downtime this week."
    agent = GenieSpaceAgent(refs=DemoTableRefs())
    sql = agent.build_sql(prompt=prompt)
    LOG.info("Generated SQL length=%s", len(sql))
    return {"prompt": prompt, "sql": sql}
