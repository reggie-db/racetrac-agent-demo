"""Information extraction brick for unstructured store operation updates."""

from __future__ import annotations

import re

from common.models import ExtractedStoreSignal
from lfp_logging import logs

LOG = logs.logger()

_STORE_PATTERN = re.compile(r"(RT-\d{3,4})", flags=re.IGNORECASE)


def _infer_category(message: str) -> str:
    """Infer the category from common pump operations keywords."""
    lowered = message.lower()
    if "pump" in lowered or "motor" in lowered or "maintenance" in lowered:
        return "maintenance"
    if "breakdown" in lowered or "fault" in lowered or "downtime" in lowered:
        return "breakdown"
    if "forecast" in lowered or "pricing" in lowered or "fuel demand" in lowered:
        return "forecasting"
    return "general"


def _infer_severity(message: str) -> str:
    """Infer severity from message tone and keywords."""
    lowered = message.lower()
    if "critical" in lowered or "urgent" in lowered or "major" in lowered:
        return "high"
    if "watch" in lowered or "elevated" in lowered:
        return "medium"
    return "low"


def _recommended_action(category: str, severity: str) -> str:
    """Map extracted signal attributes into an operations recommendation."""
    if category == "maintenance" and severity == "high":
        return "Dispatch field technician and stage replacement part within 1 hour."
    if category == "breakdown":
        return "Open breakdown ticket and route to store manager and pump vendor queue."
    if category == "forecasting":
        return "Validate Genie forecast view outputs and publish price recommendation."
    return "Log issue in daily supervisor digest for triage."


class InfoExtractorAgent:
    """Extract structured operations signals from natural language updates."""

    def extract(self, message: str) -> ExtractedStoreSignal:
        """Return one structured signal from an unstructured message."""
        store_match = _STORE_PATTERN.search(message)
        store_id = store_match.group(1).upper() if store_match else "RT-UNKNOWN"
        category = _infer_category(message)
        severity = _infer_severity(message)
        result = ExtractedStoreSignal(
            store_id=store_id,
            category=category,
            severity=severity,
            summary=message.strip(),
            recommended_action=_recommended_action(
                category=category, severity=severity
            ),
        )
        LOG.info(
            "Extracted signal store_id=%s category=%s severity=%s",
            result.store_id,
            result.category,
            result.severity,
        )
        return result
