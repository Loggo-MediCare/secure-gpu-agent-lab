# Policy Mapping for Future Sandbox Design

## Current Policy Purpose
The current policy file is a lightweight safety contract for the secure agent. It controls which files may be read, which files are protected, which locations may be written, and whether network access is allowed.

## Read Allowlist Mapping
- allowed_docs/ maps to the current read allowlist.
- This is the approved input surface for document processing.
- In a future sandbox, the same concept would become the visible read-only workspace for the agent.

## Protected File Mapping
- secrets/ maps to blocked or protected files.
- These paths are treated as sensitive and should never be surfaced to the agent runtime.
- In a future design, protected files would remain outside the sandbox data plane unless explicitly approved.

## Write Allowlist Mapping
- allowed_output/ and logs/ map to the current write allowlist.
- Only these locations are permitted for generated reports and audit data.
- In a future sandbox, these would be the sanctioned artifact and audit sinks.

## Audit Trail Mapping
- logs/ maps to the audit trail.
- The agent appends records describing actions and outcomes.
- In a future design, the sandbox would extend this with policy decisions, runtime events, and execution records.

## Sessions Mapping
- sessions will map to session history in a future runtime.
- They would represent the state of a task or conversation over time.
- For now, this remains a planning boundary rather than an implemented feature.

## Memory Mapping
- memory/ maps to approved memory storage.
- memory/quarantine/ maps to quarantined memory storage.
- The future system can use this distinction to separate trusted memory from content that requires review.

## Skills Mapping
- skills/ maps to the skills index surface.
- A future skills index could be represented by a skills/index.json file or similar metadata store.
- This is a planning placeholder and is not implemented yet.

## Secret Redaction Mapping
- secret_redaction: true simulates token masking and secret filtering.
- In future systems, this would help prevent secret-like values from being emitted in prompts, summaries, or logs.
- It is a protective control rather than a real secret vault.

## Default Deny Mapping
- default_action: deny protects the system by requiring explicit authorization for actions that are not clearly safe.
- This aligns with a conservative enterprise security posture.

## Human Approval Mapping
- require_approval_for lists actions that should be gated by human approval in a future design.
- Examples include approve_memory, crystallize_skill, and access_github.
- This provides a path toward enterprise-style controls without introducing live service connections in the current lab.
