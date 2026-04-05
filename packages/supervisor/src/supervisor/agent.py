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

    def _build_genie_prompt(self, extracted_signal: object) -> str:
        """Build a dynamic Genie prompt from extracted pump signal context."""
        return (
            "Show risk signals for "
            f"{extracted_signal.store_id} {extracted_signal.pump_id} "
            f"with breakdown type {extracted_signal.breakdown_type}, "
            f"fuel grade {extracted_signal.fuel_grade}, and "
            f"downtime {extracted_signal.downtime_minutes} minutes."
        )

    def build_digest(
        self, docs: list[dict[str, str]], store_update: str
    ) -> SupervisorDigest:
        """Build a digest intended for store operations leadership."""
        ka_response = self._knowledge_assistant.answer_question(
            query="What should stores prioritize this week for pump uptime and fuel demand?",
            documents=docs,
        )
        extracted_signal = self._info_extractor.extract(message=store_update)
        genie_prompt = self._build_genie_prompt(extracted_signal=extracted_signal)
        genie_sql = self._genie.build_sql(prompt=genie_prompt)

        digest_items = [
            f"Knowledge assistant recommendation: {ka_response['answer']}",
            (
                "Extracted store signal: "
                f"{extracted_signal.store_id} {extracted_signal.pump_id} "
                f"{extracted_signal.category} severity={extracted_signal.severity} "
                f"part={extracted_signal.part_name} "
                f"breakdown={extracted_signal.breakdown_type} "
                f"downtime={extracted_signal.downtime_minutes}m"
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
