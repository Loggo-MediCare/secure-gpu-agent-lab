# Phase 2 Issues: OpenShell / NemoClaw Connection

This file tracks the Phase 2 roadmap for connecting the current policy-driven Python agent to an OpenShell / NemoClaw-style sandbox architecture.

## Issue 1 — Research OpenShell / NemoClaw architecture

### Goal
Understand the minimum OpenShell / NemoClaw architecture needed to connect this lab to a real agent sandbox.

### Tasks
- Identify how OpenShell / NemoClaw is installed and started.
- Document required runtime components.
- Compare current policy.yaml with OpenShell / NemoClaw policy concepts.
- Create docs/phase2_architecture.md.

### Acceptance Criteria
- Architecture note exists.
- Current folders map clearly to sandbox concepts:
  - allowed_docs/
  - secrets/
  - allowed_output/
  - logs/
- No heavy dependencies added yet.

### Safety
Do not connect real secrets, real company data, or live external services.

---

## Issue 2 — Map policy.yaml to OpenShell-style sandbox policy

### Goal
Prepare the existing policy.yaml so it can later map to OpenShell / NemoClaw sandbox rules.

### Tasks
- Review existing policy.yaml.
- Add comments explaining each policy rule.
- Define future fields for:
  - filesystem read allowlist
  - filesystem read blocklist
  - write allowlist
  - network allow / deny
  - human approval requirements
- Add docs/policy_mapping.md.

### Acceptance Criteria
- Existing tests still pass.
- policy.yaml remains simple and readable.
- No real secrets are added.

---

## Issue 3 — Improve audit logs for sandbox-style action tracking

### Goal
Make audit logs more useful before connecting to OpenShell / NemoClaw.

### Tasks
- Add timestamp.
- Add action type:
  - read_allowed
  - read_blocked
  - write_allowed
  - write_blocked
  - network_blocked
- Add target path.
- Add result:
  - allowed
  - blocked
- Add tests for audit log output.

### Acceptance Criteria
- logs/audit.log is human-readable.
- Tests verify blocked secret access is logged.
- Tests verify allowed document access is logged.

---

## Issue 4 — Add human approval simulation for sensitive actions

### Goal
Simulate human-in-the-loop approval before connecting to a real sandbox system.

### Tasks
- Add approval_required rules from policy.yaml.
- Block sensitive actions unless approval is explicitly passed.
- Create a simple approval simulation function.
- Add tests for approved and unapproved actions.

### Acceptance Criteria
- Writes can require approval.
- Delete actions are blocked by default.
- Network access remains disabled.
- Tests pass.

---

## Issue 5 — Create OpenShell / NemoClaw connector stub

### Goal
Create a placeholder connector layer without depending on the real OpenShell / NemoClaw runtime yet.

### Tasks
- Create agents/sandbox_connector.py.
- Define simple functions:
  - check_read(path)
  - check_write(path)
  - check_network(url)
  - record_audit(action)
- Connect safe_agent.py to this stub.
- Keep all behavior identical.

### Acceptance Criteria
- Existing tests still pass.
- safe_agent.py becomes easier to swap into a real sandbox later.
- No heavy dependencies added.

---

## Issue 6 — Add Phase 2 demo script

### Goal
Create one simple demo command that shows the full safety workflow.

### Demo should show
- Reading allowed_docs/ succeeds.
- Reading secrets/ is blocked.
- Writing allowed_output/ succeeds.
- Writing outside allowed_output/ is blocked.
- Network access is denied.
- Audit log records all actions.

### Acceptance Criteria
- Add examples/phase2_demo.py.
- Running the demo produces clear terminal output.
- No real external network calls.
- No real secrets.

---

## Issue 7 — Add Hermes-style session, memory, and skills structure

### Goal
Make this lab closer to a Hermes-style self-improving enterprise agent without connecting real OpenShell / NemoClaw yet.

This issue is now prioritized because the next learning goal is to build the Hermes-style agent core first:
- session history
- memory layer
- reusable skills
- curator workflow

OpenShell / NemoClaw integration will remain a later sandbox/runtime milestone.

### Tasks
- Add `sessions/` for per-run session logs.
- Add `memory/` with:
  - `approved_memory.jsonl`
  - `quarantine_memory.jsonl`
- Add `skills/` with:
  - `index.json`
  - one sample skill
- Add `agents/memory_store.py`.
- Add `agents/skill_registry.py`.
- Add `agents/curator.py`.
- Update `policy.yaml` so memory writes and skill crystallization require approval.
- Add tests to verify:
  - agent cannot read `secrets/`
  - agent cannot directly write approved memory
  - agent can write quarantine memory
  - skills are loaded only by name from `skills/index.json`
  - curator produces a report without deleting anything

### Acceptance Criteria
- Existing tests still pass.
- No real secrets are used.
- No external network calls are made.
- The project remains standard-library only.

### Safety
This issue should not connect real OpenShell, NemoClaw, OpenSSL, GitHub tokens, API keys, or live external services.

### Priority
High.

Hermes-style session, memory, and skills structure should be built before deeper OpenShell / NemoClaw integration.
