"""Genie space provisioning helpers for the RaceTrac demo."""

from common.config import DemoTableRefs
from common.sql import fuel_price_forecast_view_sql, pump_maintenance_forecast_view_sql


def build_genie_space_instruction(
    refs: DemoTableRefs | None = None,
) -> dict[str, object]:
    """Return a payload-style instruction object for creating a Genie space."""
    table_refs = refs or DemoTableRefs()
    return {
        "name": "racetrac-command-the-floor-demo",
        "description": (
            "Genie space for station managers to query pump uptime, maintenance, and pricing signals "
            "without writing SQL."
        ),
        "catalog": table_refs.catalog,
        "schema": table_refs.schema,
        "default_tables": [
            table_refs.transactions,
            table_refs.pump_breakdowns,
            table_refs.pump_telemetry,
        ],
        "default_views": [
            "vw_pump_maintenance_forecast",
            "vw_fuel_price_forecast",
        ],
        "view_sql": [
            pump_maintenance_forecast_view_sql(table_refs),
            fuel_price_forecast_view_sql(table_refs),
        ],
        "starter_prompts": [
            "Which pumps have highest projected maintenance risk next week?",
            "Where is projected fuel pricing increasing fastest by grade?",
            "What stores combine high breakdown risk with high fuel demand?",
        ],
    }
