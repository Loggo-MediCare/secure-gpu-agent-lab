---
name: "Phase 2: Add demo script"
about: "Create a demo showing the full policy-controlled workflow"
title: "Phase 2: Add demo script for policy-controlled agent workflow"
labels: phase-2, demo
assignees: ""
---

## Goal
Create one simple demo command that shows the full safety workflow.

## Demo should show
- [ ] Reading allowed_docs/ succeeds.
- [ ] Reading secrets/ is blocked.
- [ ] Writing allowed_output/ succeeds.
- [ ] Writing outside allowed_output/ is blocked.
- [ ] Network access is denied.
- [ ] Audit log records all actions.

## Acceptance Criteria
- [ ] Add examples/phase2_demo.py.
- [ ] Running the demo produces clear terminal output.
- [ ] No real external network calls.
- [ ] No real secrets.
