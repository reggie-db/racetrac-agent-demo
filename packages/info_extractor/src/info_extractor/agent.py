"""Information extraction brick for unstructured store operation updates."""

from __future__ import annotations

import re

from common.models import ExtractedStoreSignal
from lfp_logging import logs

LOG = logs.logger()

_STORE_PATTERN = re.compile(r"(RT-\d{3,4})", flags=re.IGNORECASE)
_PUMP_PATTERN = re.compile(r"(P-\d{1,2}|pump\s*\d{1,2})", flags=re.IGNORECASE)
_DOWNTIME_PATTERN = re.compile(r"(\d+)\s*(minutes|mins|min)", flags=re.IGNORECASE)
_PART_KEYWORDS = ("motor", "nozzle", "meter", "seal", "filter", "valve", "hoseline")
_BREAKDOWN_KEYWORDS = ("flow_drop", "pressure_fault", "sensor_fault", "leak_warning")
_FUEL_KEYWORDS = ("regular", "midgrade", "premium", "diesel")


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


def _extract_pump_id(message: str) -> str:
    """Extract pump identifier from a free-form operations message."""
    pump_match = _PUMP_PATTERN.search(message)
    if not pump_match:
        return "P-UNKNOWN"
    token = pump_match.group(1).upper().replace(" ", "")
    if token.startswith("PUMP"):
        token = token.replace("PUMP", "P-")
    if token.startswith("P-"):
        return token
    return f"P-{token}"


def _extract_keyword(message: str, keywords: tuple[str, ...], fallback: str) -> str:
    """Extract first matching keyword from text or return fallback."""
    lowered = message.lower()
    for keyword in keywords:
        if keyword in lowered:
            return keyword
    return fallback


def _extract_downtime_minutes(message: str) -> int:
    """Extract downtime in minutes from the message when present."""
    match = _DOWNTIME_PATTERN.search(message)
    if not match:
        return 0
    return int(match.group(1))


class InfoExtractorAgent:
    """Extract structured operations signals from natural language updates."""

    def extract(self, message: str) -> ExtractedStoreSignal:
        """Return one structured signal from an unstructured message."""
        store_match = _STORE_PATTERN.search(message)
        store_id = store_match.group(1).upper() if store_match else "RT-UNKNOWN"
        pump_id = _extract_pump_id(message)
        category = _infer_category(message)
        severity = _infer_severity(message)
        part_name = _extract_keyword(message, _PART_KEYWORDS, "unknown_part")
        breakdown_type = _extract_keyword(
            message, _BREAKDOWN_KEYWORDS, "unspecified_breakdown"
        )
        fuel_grade = _extract_keyword(message, _FUEL_KEYWORDS, "unspecified_grade")
        downtime_minutes = _extract_downtime_minutes(message)
        result = ExtractedStoreSignal(
            store_id=store_id,
            pump_id=pump_id,
            category=category,
            severity=severity,
            part_name=part_name,
            breakdown_type=breakdown_type,
            fuel_grade=fuel_grade,
            downtime_minutes=downtime_minutes,
            summary=message.strip(),
            recommended_action=_recommended_action(
                category=category, severity=severity
            ),
        )
        LOG.info(
            "Extracted signal store_id=%s pump_id=%s category=%s severity=%s",
            result.store_id,
            result.pump_id,
            result.category,
            result.severity,
        )
        return result
