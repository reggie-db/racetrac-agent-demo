import json

import reflex as rx
from common.config import DemoTableRefs
from common.sql import fuel_price_forecast_view_sql, pump_maintenance_forecast_view_sql
from genie_space.demo_runner import run_genie_demo
from genie_space.provisioning import build_genie_space_instruction
from info_extractor.demo_runner import run_info_extractor_demo
from knowledge_assistant.demo_runner import run_knowledge_assistant_demo
from lfp_logging import logs
from supervisor.demo_runner import run_supervisor_demo

"""Reflex application for demonstrating pump operations agent bricks."""

LOG = logs.logger()


def _pretty_json(payload: object) -> str:
    """Convert output payloads into readable JSON for the UI."""
    return json.dumps(payload, indent=2, sort_keys=True, default=str)


class DemoState(rx.State):
    """Application state for running each pump-operations demo brick."""

    knowledge_output: str = "{}"
    extractor_output: str = "{}"
    genie_output: str = "{}"
    supervisor_output: str = "{}"
    forecast_output: str = "{}"
    status_message: str = "Ready"

    def run_knowledge_demo(self) -> None:
        """Run knowledge assistant demo and render output."""
        LOG.info("Running knowledge assistant demo from Reflex app")
        self.knowledge_output = _pretty_json(run_knowledge_assistant_demo())
        self.status_message = "Knowledge assistant demo completed."

    def run_extractor_demo(self) -> None:
        """Run information extraction demo and render output."""
        LOG.info("Running info extractor demo from Reflex app")
        self.extractor_output = _pretty_json(run_info_extractor_demo())
        self.status_message = "Information extraction demo completed."

    def run_genie_demo(self) -> None:
        """Run Genie NL-to-SQL demo and render output."""
        LOG.info("Running Genie demo from Reflex app")
        self.genie_output = _pretty_json(run_genie_demo())
        self.status_message = "Genie SQL demo completed."

    def run_supervisor_demo(self) -> None:
        """Run supervisor orchestration demo and render output."""
        LOG.info("Running supervisor demo from Reflex app")
        self.supervisor_output = _pretty_json(run_supervisor_demo())
        self.status_message = "Supervisor orchestration demo completed."

    def show_forecast_assets(self) -> None:
        """Build and display Genie forecast views and provisioning payload."""
        LOG.info("Building forecast SQL payloads from Reflex app")
        refs = DemoTableRefs()
        payload = {
            "maintenance_forecast_view_sql": pump_maintenance_forecast_view_sql(refs),
            "fuel_price_forecast_view_sql": fuel_price_forecast_view_sql(refs),
            "genie_space_payload": build_genie_space_instruction(refs),
        }
        self.forecast_output = _pretty_json(payload)
        self.status_message = "Forecast view SQL and Genie payload generated."


def _demo_section(
    title: str,
    description: str,
    output: rx.Var[str],
    click_handler: rx.event.EventHandler,
) -> rx.Component:
    """Reusable section renderer for each app demo area."""
    return rx.card(
        rx.vstack(
            rx.heading(title, size="4"),
            rx.text(description, color="gray"),
            rx.button(f"Run {title}", on_click=click_handler),
            rx.code_block(
                output,
                language="json",
                width="100%",
                max_height="22rem",
                wrap_long_lines=True,
            ),
            spacing="3",
            width="100%",
        ),
        width="100%",
    )


def index() -> rx.Component:
    """Main page for the RaceTrac pump operations demo app."""
    return rx.container(
        rx.vstack(
            rx.heading("RaceTrac Pump Operations Agent Demo", size="7"),
            rx.text(
                "Interactive app for knowledge assistant, extraction, Genie SQL, "
                "supervisor orchestration, and ai_forecast-based Genie view setup.",
                size="3",
            ),
            rx.badge(DemoState.status_message, color_scheme="blue"),
            _demo_section(
                title="Knowledge Assistant",
                description="RAG-style guidance for pump maintenance and operations.",
                output=DemoState.knowledge_output,
                click_handler=DemoState.run_knowledge_demo,
            ),
            _demo_section(
                title="Info Extractor",
                description="Extract structured pump incident signals from unstructured updates.",
                output=DemoState.extractor_output,
                click_handler=DemoState.run_extractor_demo,
            ),
            _demo_section(
                title="Genie SQL",
                description="Generate pump breakdown and fuel-pricing SQL from natural language.",
                output=DemoState.genie_output,
                click_handler=DemoState.run_genie_demo,
            ),
            _demo_section(
                title="Supervisor",
                description="Compose a daily pump operations digest across all demo bricks.",
                output=DemoState.supervisor_output,
                click_handler=DemoState.run_supervisor_demo,
            ),
            _demo_section(
                title="Forecast Assets",
                description="Generate ai_forecast view SQL and Genie space setup payload.",
                output=DemoState.forecast_output,
                click_handler=DemoState.show_forecast_assets,
            ),
            spacing="4",
            width="100%",
        ),
        max_width="80rem",
        padding_y="2rem",
    )


app = rx.App()
app.add_page(index, route="/")
