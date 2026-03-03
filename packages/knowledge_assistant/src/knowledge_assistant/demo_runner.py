"""Entrypoint for exercising the knowledge assistant brick."""

from common.dummy_data import generate_knowledge_docs
from lfp_logging import logs

from knowledge_assistant.agent import KnowledgeAssistantAgent

LOG = logs.logger()


def run_knowledge_assistant_demo() -> dict[str, object]:
    """Run a deterministic local demo question against synthetic docs."""
    docs = generate_knowledge_docs(row_count=40)
    agent = KnowledgeAssistantAgent()
    question = "How should stores escalate pump breakdown alerts and maintenance violations?"
    response = agent.answer_question(query=question, documents=docs)
    LOG.info("Knowledge assistant citations: %s", response["citations"])
    return response
