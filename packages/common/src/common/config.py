"""Shared configuration values for the RaceTrac agent demo."""

from dataclasses import dataclass

DEFAULT_CATALOG = "reggie_pierce"
DEFAULT_SCHEMA = "racetrac_agent_demo"

TRANSACTION_TABLE = "store_transactions"
PUMP_BREAKDOWN_TABLE = "pump_breakdown_events"
PUMP_TELEMETRY_TABLE = "pump_telemetry_signals"
KNOWLEDGE_DOCS_TABLE = "pump_knowledge_documents"
PROJECT_MAPPING_TABLE = "pump_project_mapping"


@dataclass(frozen=True)
class DemoTableRefs:
    """Canonical table references used across all demo bricks."""

    catalog: str = DEFAULT_CATALOG
    schema: str = DEFAULT_SCHEMA
    transactions: str = TRANSACTION_TABLE
    pump_breakdowns: str = PUMP_BREAKDOWN_TABLE
    pump_telemetry: str = PUMP_TELEMETRY_TABLE
    knowledge_docs: str = KNOWLEDGE_DOCS_TABLE
    project_mapping: str = PROJECT_MAPPING_TABLE

    def fq_table(self, table_name: str) -> str:
        """Return a fully-qualified table name for the current catalog/schema."""
        return f"{self.catalog}.{self.schema}.{table_name}"
