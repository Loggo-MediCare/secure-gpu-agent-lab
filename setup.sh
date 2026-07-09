#!/usr/bin/env bash
set -euo pipefail

echo "Running tests..."
python3 -m unittest discover -s tests -p "test_*.py"

echo "Running safe agent..."
python3 agents/safe_agent.py

echo "Done."
echo "Report: allowed_output/project_report.md"
echo "Audit log: logs/audit.log"
