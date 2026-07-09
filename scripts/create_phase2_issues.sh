#!/usr/bin/env bash
set -euo pipefail

REPO="Loggo-MediCare/secure-gpu-agent-lab"

if ! command -v gh >/dev/null 2>&1; then
  echo "GitHub CLI 'gh' is not installed."
  echo "Install it first, then run: gh auth login"
  exit 1
fi

gh issue create \
  --repo "$REPO" \
  --title "Phase 2: Research OpenShell / NemoClaw architecture" \
  --label "phase-2,research,openshell,nemoclaw" \
  --body-file ".github/ISSUE_TEMPLATE/phase2_01_research_openshell_nemoclaw.md"

gh issue create \
  --repo "$REPO" \
  --title "Phase 2: Map policy.yaml to OpenShell-style sandbox policy" \
  --label "phase-2,policy,sandbox" \
  --body-file ".github/ISSUE_TEMPLATE/phase2_02_policy_mapping.md"

gh issue create \
  --repo "$REPO" \
  --title "Phase 2: Improve audit logs for sandbox-style action tracking" \
  --label "phase-2,audit,security" \
  --body-file ".github/ISSUE_TEMPLATE/phase2_03_audit_logs.md"

gh issue create \
  --repo "$REPO" \
  --title "Phase 2: Add human approval simulation for sensitive actions" \
  --label "phase-2,approval,safety" \
  --body-file ".github/ISSUE_TEMPLATE/phase2_04_human_approval.md"

gh issue create \
  --repo "$REPO" \
  --title "Phase 2: Create OpenShell / NemoClaw connector stub" \
  --label "phase-2,connector,openshell,nemoclaw" \
  --body-file ".github/ISSUE_TEMPLATE/phase2_05_connector_stub.md"

gh issue create \
  --repo "$REPO" \
  --title "Phase 2: Add demo script for policy-controlled agent workflow" \
  --label "phase-2,demo" \
  --body-file ".github/ISSUE_TEMPLATE/phase2_06_demo_script.md"

echo "Phase 2 issues created."
