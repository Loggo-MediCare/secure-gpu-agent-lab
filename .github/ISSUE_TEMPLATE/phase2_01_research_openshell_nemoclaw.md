---
name: "Phase 2: Research OpenShell / NemoClaw architecture"
about: "Research the minimum sandbox architecture needed for Phase 2"
title: "Phase 2: Research OpenShell / NemoClaw architecture"
labels: phase-2, research, openshell, nemoclaw
assignees: ""
---

## Goal
Understand the minimum OpenShell / NemoClaw architecture needed to connect this lab to a real agent sandbox.

## Tasks
- [ ] Identify how OpenShell / NemoClaw is installed and started.
- [ ] Document required runtime components.
- [ ] Compare current policy.yaml with OpenShell / NemoClaw policy concepts.
- [ ] Create docs/phase2_architecture.md.

## Acceptance Criteria
- [ ] Architecture note exists.
- [ ] Current folders map clearly to sandbox concepts:
  - allowed_docs/
  - secrets/
  - allowed_output/
  - logs/
- [ ] No heavy dependencies added yet.

## Safety
Do not connect real secrets, real company data, or live external services.
