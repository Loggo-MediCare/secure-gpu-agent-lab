---
name: "Phase 2: Improve audit logs"
about: "Improve audit logs for sandbox-style action tracking"
title: "Phase 2: Improve audit logs for sandbox-style action tracking"
labels: phase-2, audit, security
assignees: ""
---

## Goal
Make audit logs more useful before connecting to OpenShell / NemoClaw.

## Tasks
- [ ] Add timestamp.
- [ ] Add action type:
  - read_allowed
  - read_blocked
  - write_allowed
  - write_blocked
  - network_blocked
- [ ] Add target path.
- [ ] Add result:
  - allowed
  - blocked
- [ ] Add tests for audit log output.

## Acceptance Criteria
- [ ] logs/audit.log is human-readable.
- [ ] Tests verify blocked secret access is logged.
- [ ] Tests verify allowed document access is logged.
