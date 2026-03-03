"""Supervisor brick that composes outputs from all demo agent bricks."""

from __future__ import annotations

from datetime import date

from common.models import SupervisorDigest
from genie_space.agent import GenieSpaceAgent
from info_extractor.agent import InfoExtractorAgent
from knowledge_assistant.agent import KnowledgeAssistantAgent
from lfp_logging import logs

LOG = logs.logger()


class SupervisorAgent:
    """Compose a single digest from KA, extraction, and Genie responses."""

    def __init__(self) -> None:
        self._knowledge_assistant = KnowledgeAssistantAgent()
        self._info_extractor = InfoExtractorAgent()
        self._genie = GenieSpaceAgent()

    def build_digest(
        self, docs: list[dict[str, str]], store_update: str
    ) -> SupervisorDigest:
        """Build a digest intended for store operations leadership."""
        ka_response = self._knowledge_assistant.answer_question(
            query="What should stores prioritize this week for pump uptime and fuel demand?",
            documents=docs,
        )
        extracted_signal = self._info_extractor.extract(message=store_update)
        genie_sql = self._genie.build_sql(
            prompt="Show stores with top pump breakdown and fuel pricing risk signals."
        )

        digest_items = [
            f"Knowledge assistant recommendation: {ka_response['answer']}",
            (
                "Extracted store signal: "
                f"{extracted_signal.store_id} {extracted_signal.category} "
                f"severity={extracted_signal.severity}"
            ),
            f"Genie query prepared for operators: {genie_sql}",
        ]
        escalation_items = []
        if extracted_signal.severity == "high":
            escalation_items.append(
                f"Escalate {extracted_signal.store_id}: "
                f"{extracted_signal.recommended_action}"
            )

        digest = SupervisorDigest(
            date_key=date.today().isoformat(),
            digest_items=digest_items,
            escalation_items=escalation_items,
        )
        LOG.info("Built supervisor digest with %s items", len(digest.digest_items))
        return digest
