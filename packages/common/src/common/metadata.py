"""Table and column metadata for rich dummy-data documentation."""

from __future__ import annotations

from common.config import DemoTableRefs

TABLE_DESCRIPTIONS: dict[str, str] = {
    "store_transactions": (
        "Synthetic fuel transaction facts at store and pump grain, used for demand, "
        "pricing, and operations analytics demos."
    ),
    "pump_breakdown_events": (
        "Synthetic pump incident and repair history used for reliability and "
        "maintenance-triage scenarios."
    ),
    "pump_telemetry_signals": (
        "Synthetic time-series telemetry for pumps, including pressure, flow, "
        "temperature, vibration, and device error states."
    ),
    "pump_knowledge_documents": (
        "Synthetic knowledge corpus for operations runbooks, maintenance guidance, "
        "and forecasting playbooks used by the assistant demos."
    ),
    "pump_project_mapping": (
        "Synthetic source-to-target project mapping records for pump modernization "
        "data integration examples."
    ),
}

COLUMN_DESCRIPTIONS: dict[str, dict[str, str]] = {
    "store_transactions": {
        "transaction_id": "Unique identifier for a fuel transaction event.",
        "store_id": "RaceTrac store identifier.",
        "pump_id": "Pump or dispenser identifier within a store.",
        "transaction_ts": "Timestamp when the fuel transaction occurred.",
        "fuel_grade": "Fuel grade sold in the transaction.",
        "gallons_sold": "Fuel volume sold in gallons.",
        "price_per_gallon": "Effective unit price per gallon at transaction time.",
        "gross_sales": "Total sale amount captured for the transaction.",
        "region": "Operational region used for planning and reporting.",
    },
    "pump_breakdown_events": {
        "event_id": "Unique identifier for a pump incident record.",
        "store_id": "RaceTrac store identifier where the incident occurred.",
        "pump_id": "Pump or dispenser identifier associated with the incident.",
        "event_ts": "Timestamp when the incident was observed.",
        "part_name": "Pump component involved in the incident.",
        "breakdown_type": "Incident category describing the observed failure mode.",
        "downtime_minutes": "Minutes of service interruption caused by the incident.",
        "repair_cost": "Estimated or observed repair cost in USD.",
        "severity": "Severity classification for routing and escalation.",
    },
    "pump_telemetry_signals": {
        "telemetry_id": "Unique identifier for a telemetry sample.",
        "store_id": "RaceTrac store identifier for the telemetry source.",
        "pump_id": "Pump or dispenser identifier for the telemetry source.",
        "event_ts": "Timestamp for the telemetry sample.",
        "line_pressure_psi": "Fuel line pressure reading in PSI.",
        "flow_rate_gpm": "Fuel flow rate reading in gallons per minute.",
        "temperature_f": "Ambient or device temperature in degrees Fahrenheit.",
        "vibration_mm_s": "Pump vibration level in millimeters per second.",
        "error_code": "Device error code captured at sample time.",
        "severity": "Operational severity state at sample time.",
    },
    "pump_knowledge_documents": {
        "doc_id": "Unique identifier for a knowledge document chunk.",
        "title": "Short title for the document chunk.",
        "content": "Document content used for retrieval and answer synthesis.",
        "topic": "Primary operations topic associated with the chunk.",
        "last_updated_ts": "Timestamp of the latest document update.",
    },
    "pump_project_mapping": {
        "mapping_id": "Unique identifier for a mapping record.",
        "source_system": "Originating system for the source data field.",
        "source_table": "Originating table in the source system.",
        "source_column": "Originating source column name.",
        "target_system": "Destination system for transformed data.",
        "target_table": "Destination target table name.",
        "target_column": "Destination target column name.",
        "mapping_confidence": "Confidence score for the source-to-target mapping.",
    },
}


def _escape_sql_literal(value: str) -> str:
    """Escape single quotes to safely embed comments in SQL literals."""
    return value.replace("'", "''")


def build_metadata_sql(refs: DemoTableRefs) -> list[str]:
    """Generate SQL statements that apply rich table and column comments."""
    statements: list[str] = []
    for table_name, table_comment in TABLE_DESCRIPTIONS.items():
        fq_table = refs.fq_table(table_name)
        statements.append(
            f"COMMENT ON TABLE {fq_table} IS '{_escape_sql_literal(table_comment)}'"
        )
        for column_name, column_comment in COLUMN_DESCRIPTIONS[table_name].items():
            statements.append(
                "ALTER TABLE "
                f"{fq_table} ALTER COLUMN {column_name} "
                f"COMMENT '{_escape_sql_literal(column_comment)}'"
            )
    return statements
