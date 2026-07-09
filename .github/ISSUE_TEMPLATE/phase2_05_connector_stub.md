---
name: "Phase 2: Create OpenShell / NemoClaw connector stub"
about: "Create a placeholder connector layer before real runtime integration"
title: "Phase 2: Create OpenShell / NemoClaw connector stub"
labels: phase-2, connector, openshell, nemoclaw
assignees: ""
---

## Goal
Create a placeholder connector layer without depending on the real OpenShell / NemoClaw runtime yet.

## Tasks
- [ ] Create agents/sandbox_connector.py.
- [ ] Define simple functions:
  - check_read(path)
  - check_write(path)
  - check_network(url)
  - record_audit(action)
- [ ] Connect safe_agent.py to this stub.
- [ ] Keep all behavior identical.

## Acceptance Criteria
- [ ] Existing tests still pass.
- [ ] safe_agent.py becomes easier to swap into a real sandbox later.
- [ ] No heavy dependencies added.
