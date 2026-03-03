#!/usr/bin/env bash
set -euo pipefail

uv run --project packages/pump_ops_app reflex run --env prod
