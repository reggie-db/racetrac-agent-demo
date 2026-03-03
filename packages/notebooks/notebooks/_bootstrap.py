import logging
import sys
from pathlib import Path

from lfp_logging import logs

"""Bootstrap utilities for notebook execution in local and Databricks contexts."""

LOG = logs.logger()


def bootstrap_local_packages() -> None:
    """Add workspace package paths to sys.path for direct notebook execution."""
    current_file = Path(__file__).resolve()
    workspace_root = current_file.parents[3]
    package_dirs = [
        workspace_root / "packages" / "common" / "src",
        workspace_root / "packages" / "knowledge_assistant" / "src",
        workspace_root / "packages" / "info_extractor" / "src",
        workspace_root / "packages" / "genie_space" / "src",
        workspace_root / "packages" / "supervisor" / "src",
    ]
    for package_dir in package_dirs:
        package_path = str(package_dir)
        if package_path not in sys.path:
            sys.path.append(package_path)


def configure_logging() -> None:
    """Configure concise notebook logging output for demo readability."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )


def get_spark_session():
    """Return an active Spark session or create one for local validation."""
    from pyspark.sql import SparkSession

    return SparkSession.getActiveSession() or SparkSession.builder.getOrCreate()


def render_output(value: object, display_fn: object | None = None) -> None:
    """Display notebook output if available, otherwise log a readable fallback."""
    if callable(display_fn):
        display_fn(value)
        return
    LOG.info("Output: %s", value)
