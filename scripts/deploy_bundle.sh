#!/usr/bin/env bash
set -euo pipefail

TARGET="${DATABRICKS_BUNDLE_TARGET:-dev}"

databricks bundle validate -t "${TARGET}"
databricks bundle deploy -t "${TARGET}"
