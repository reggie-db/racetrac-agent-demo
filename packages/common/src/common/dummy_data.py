"""Dummy data factories for the RaceTrac demo notebooks."""

from __future__ import annotations

import random
from datetime import datetime, timedelta

from faker import Faker

from common.config import DemoTableRefs

_FAKER = Faker()
_SEVERITIES = ["low", "medium", "high"]
_PUMP_PARTS = ["nozzle", "meter", "motor", "seal", "filter", "valve", "hoseline"]
_BREAKDOWN_TYPES = ["flow_drop", "pressure_fault", "sensor_fault", "leak_warning"]


def _build_timestamp(days_back: int) -> datetime:
    """Generate a realistic recent timestamp within a bounded lookback window."""
    base_time = datetime.now() - timedelta(days=random.randint(0, days_back))
    return base_time.replace(
        hour=random.randint(5, 23),
        minute=random.randint(0, 59),
        second=random.randint(0, 59),
        microsecond=0,
    )


def generate_store_transactions(row_count: int = 500) -> list[dict[str, object]]:
    """Create synthetic fuel transaction records for BI and Genie demos."""
    records: list[dict[str, object]] = []
    for _ in range(row_count):
        transaction_time = _build_timestamp(days_back=21)
        records.append(
            {
                "transaction_id": _FAKER.uuid4(),
                "store_id": f"RT-{random.randint(100, 450)}",
                "pump_id": f"P-{random.randint(1, 20):02d}",
                "transaction_ts": transaction_time.isoformat(),
                "fuel_grade": random.choice(
                    ["regular", "midgrade", "premium", "diesel"]
                ),
                "gallons_sold": round(random.uniform(6.0, 27.0), 3),
                "price_per_gallon": round(random.uniform(2.55, 4.85), 3),
                "gross_sales": round(random.uniform(20.0, 130.0), 2),
                "region": random.choice(["south", "southeast", "midwest"]),
            }
        )
    return records


def generate_pump_breakdown_events(row_count: int = 240) -> list[dict[str, object]]:
    """Create synthetic pump breakdown and repair events."""
    records: list[dict[str, object]] = []
    for _ in range(row_count):
        event_time = _build_timestamp(days_back=14)
        records.append(
            {
                "event_id": _FAKER.uuid4(),
                "store_id": f"RT-{random.randint(100, 450)}",
                "pump_id": f"P-{random.randint(1, 20):02d}",
                "event_ts": event_time.isoformat(),
                "part_name": random.choice(_PUMP_PARTS),
                "breakdown_type": random.choice(_BREAKDOWN_TYPES),
                "downtime_minutes": random.randint(15, 240),
                "repair_cost": round(random.uniform(80.0, 1450.0), 2),
                "severity": random.choice(_SEVERITIES),
            }
        )
    return records


def generate_pump_telemetry(row_count: int = 600) -> list[dict[str, object]]:
    """Create synthetic pump telemetry events for maintenance forecasting demos."""
    records: list[dict[str, object]] = []
    for _ in range(row_count):
        event_time = _build_timestamp(days_back=10)
        records.append(
            {
                "telemetry_id": _FAKER.uuid4(),
                "store_id": f"RT-{random.randint(100, 450)}",
                "pump_id": f"P-{random.randint(1, 20):02d}",
                "event_ts": event_time.isoformat(),
                "line_pressure_psi": round(random.uniform(21.5, 64.0), 2),
                "flow_rate_gpm": round(random.uniform(2.1, 14.8), 2),
                "temperature_f": round(random.uniform(35.0, 120.0), 2),
                "vibration_mm_s": round(random.uniform(0.2, 7.5), 2),
                "error_code": random.choice(["NONE", "E101", "E140", "E220", "E304"]),
                "severity": random.choice(_SEVERITIES),
            }
        )
    return records


def generate_knowledge_docs(row_count: int = 80) -> list[dict[str, object]]:
    """Create synthetic document chunks for a pump-operations KA-style demo."""
    templates = [
        "Station manager playbook for {topic} in high-volume fueling locations.",
        "Troubleshooting runbook for {topic} incidents and escalation.",
        "Data ownership guide for {topic} tables in Unity Catalog.",
        "Onboarding notes for {topic} workflows across pump modernization projects.",
    ]
    topics = [
        "pump preventive maintenance",
        "pump breakdown triage",
        "fuel demand forecasting",
        "fuel pricing optimization",
        "daily station ops digest",
    ]

    records: list[dict[str, object]] = []
    for index in range(row_count):
        topic = random.choice(topics)
        text = random.choice(templates).format(topic=topic)
        records.append(
            {
                "doc_id": f"doc-{index + 1:04d}",
                "title": _FAKER.sentence(nb_words=6),
                "content": f"{text} {_FAKER.paragraph(nb_sentences=4)}",
                "topic": topic,
                "last_updated_ts": _build_timestamp(days_back=30).isoformat(),
            }
        )
    return records


def generate_pump_project_mapping(row_count: int = 60) -> list[dict[str, object]]:
    """Create synthetic schema mapping samples for pump modernization projects."""
    records: list[dict[str, object]] = []
    for index in range(row_count):
        records.append(
            {
                "mapping_id": f"map-{index + 1:04d}",
                "source_system": random.choice(["legacy_scada", "vendor_pump_hub"]),
                "source_table": random.choice(
                    ["pump_events", "dispenser_state", "fuel_sales", "repair_tickets"]
                ),
                "source_column": _FAKER.word(),
                "target_system": "racetrac",
                "target_table": random.choice(
                    [
                        "store_transactions",
                        "pump_breakdown_events",
                        "pump_telemetry_signals",
                    ]
                ),
                "target_column": _FAKER.word(),
                "mapping_confidence": round(random.uniform(0.55, 0.97), 3),
            }
        )
    return records


def generate_all_demo_data() -> dict[str, list[dict[str, object]]]:
    """Generate every dataset required for the end-to-end demo flow."""
    refs = DemoTableRefs()
    return {
        refs.transactions: generate_store_transactions(),
        refs.pump_breakdowns: generate_pump_breakdown_events(),
        refs.pump_telemetry: generate_pump_telemetry(),
        refs.knowledge_docs: generate_knowledge_docs(),
        refs.project_mapping: generate_pump_project_mapping(),
    }
