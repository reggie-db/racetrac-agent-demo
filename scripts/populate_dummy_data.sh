#!/usr/bin/env bash
set -euo pipefail

TARGET="${DATABRICKS_BUNDLE_TARGET:-dev}"

databricks bundle run racetrac_dummy_data_prep -t "${TARGET}"
