---
name: "Phase 2: Add human approval simulation"
about: "Simulate human-in-the-loop approval for sensitive actions"
title: "Phase 2: Add human approval simulation for sensitive actions"
labels: phase-2, approval, safety
assignees: ""
---

## Goal
Simulate human-in-the-loop approval before connecting to a real sandbox system.

## Tasks
- [ ] Add approval_required rules from policy.yaml.
- [ ] Block sensitive actions unless approval is explicitly passed.
- [ ] Create a simple approval simulation function.
- [ ] Add tests for approved and unapproved actions.

## Acceptance Criteria
- [ ] Writes can require approval.
- [ ] Delete actions are blocked by default.
- [ ] Network access remains disabled.
- [ ] Tests pass.
