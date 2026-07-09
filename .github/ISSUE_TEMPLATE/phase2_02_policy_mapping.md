---
name: "Phase 2: Map policy.yaml to sandbox policy"
about: "Prepare policy.yaml for future OpenShell / NemoClaw mapping"
title: "Phase 2: Map policy.yaml to OpenShell-style sandbox policy"
labels: phase-2, policy, sandbox
assignees: ""
---

## Goal
Prepare the existing policy.yaml so it can later map to OpenShell / NemoClaw sandbox rules.

## Tasks
- [ ] Review existing policy.yaml.
- [ ] Add comments explaining each policy rule.
- [ ] Define future fields for:
  - filesystem read allowlist
  - filesystem read blocklist
  - write allowlist
  - network allow / deny
  - human approval requirements
- [ ] Add docs/policy_mapping.md.

## Acceptance Criteria
- [ ] Existing tests still pass.
- [ ] policy.yaml remains simple and readable.
- [ ] No real secrets are added.
