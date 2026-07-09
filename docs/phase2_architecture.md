# Phase 2 Architecture: Secure Agent to Sandbox Integration

## Purpose
This document describes how the current secure-gpu-agent-lab can later connect to an OpenShell / NemoClaw-style sandbox architecture without changing the existing safety model or introducing heavy dependencies.

## Current Project Safety Model
The current project uses a small, standard-library Python agent with a simple policy file:

- Reads are limited to approved locations.
- Writes are limited to approved output locations.
- Sensitive content under secrets/ is blocked.
- Audit events are appended to logs/.
- Network access is disabled by policy.

This creates a strong foundation for later sandboxed execution because the existing agent already behaves as a constrained policy-enforcing front end.

## Mapping of Current Directories to Future Sandbox Concepts

### allowed_docs/ -> Read Allowlist
The folder allowed_docs/ represents the set of files the agent may read. In the current implementation, this maps to the policy rule allowed_read_paths.

In a future sandbox architecture, allowed_docs/ would become the initial read-only view exposed to the agent or runtime. The sandbox would grant access only to this approved content surface.

### secrets/ -> Blocked or Protected Files
The folder secrets/ is treated as a protected area that the agent must not read or expose. This maps directly to the blocked_read_paths policy.

In a future design, secrets/ would remain outside the sandbox’s data plane and would require explicit, separate authorization to access. The sandbox should never implicitly surface these files to the planner or runtime.

### allowed_output/ -> Write Allowlist
The folder allowed_output/ represents the approved destination for generated reports and artifacts. This maps to the allowed_write_paths policy.

In a future sandbox, allowed_output/ would be the writeable artifact area. The runtime could create reports, logs, or intermediate files only inside this boundary.

### logs/ -> Audit Trail
The folder logs/ is used as the audit location for append-only activity records. This is the current mechanism for tracking prompts, decisions, and generated artifacts.

In a future architecture, logs/ would become the baseline audit store for sandbox requests, policy decisions, and runtime events.

## Mapping of policy.yaml to Future Sandbox Policy
The current policy.yaml file acts as a lightweight policy contract. It can evolve into a richer sandbox policy with explicit rules for:

- allowed read paths
- blocked read paths
- allowed write paths
- network access
- future controls such as tool allowlists or command permissions

The current file format is intentionally simple, which makes it easy to extend without introducing a heavy dependency such as PyYAML.

## Proposed Future Layers

### 1. Agent Planner
The planner decides what task to perform and what data is needed. It should operate over a constrained view of the workspace and produce a request plan instead of directly accessing the filesystem.

Responsibilities:
- interpret the user request
- identify required data sources
- request approval from the policy gate
- produce a structured action plan

### 2. Policy Gate
The policy gate evaluates the planned action against the current policy before anything is executed.

Responsibilities:
- check read/write boundaries
- reject blocked or sensitive paths
- enforce network policy
- approve or deny tool usage

This is the enforcement boundary that currently exists in the Python agent logic.

### 3. Sandbox Connector
The sandbox connector bridges the local agent with the remote or isolated runtime. It translates approved actions into sandbox requests and brings results back into the local workspace.

Responsibilities:
- submit approved operations to the sandbox
- collect outputs
- write only permitted results back to allowed_output/
- maintain audit entries in logs/

### 4. OpenShell / NemoClaw Runtime
The runtime is the isolated execution environment that receives approved actions. It can run commands or tasks in a controlled environment while preserving the external safety boundaries.

Responsibilities:
- execute approved operations
- isolate processes and file access
- expose a narrow set of tools
- return structured outputs to the connector

This project should not depend on installing OpenShell or NemoClaw at this stage; the architecture document is meant to outline the integration path.

### 5. Filesystem / Network / Tools
These are the concrete capabilities the runtime may access. They should be gated by policy and only exposed when explicitly allowed.

Examples:
- Filesystem: read-only access to allowed_docs/ and write access to allowed_output/
- Network: disabled unless policy permits it
- Tools: only a small allowlisted toolset, not arbitrary shell access

## Risks
- The current policy is still simple and may not cover all future runtime behaviors.
- A future runtime could accidentally broaden the effective trust boundary if it is not strictly constrained.
- Audit logging must be tamper-resistant enough to be useful in real deployments.
- Tool access can bypass file-based controls if not carefully limited.

## Open Questions
- Should the sandbox expose a file mount or a narrower API surface?
- How should approvals be represented for write operations or tool execution?
- Should the policy format evolve to include tool and network permissions explicitly?
- How should the system handle long-running or multi-step tasks safely?

## Phase 2 Next Steps
1. Keep the current standard-library agent and policy model intact.
2. Define a minimal request protocol between the agent and a sandbox connector.
3. Add a lightweight sandbox policy schema that extends the current policy.yaml format.
4. Prototype a connector that forwards approved actions to an isolated runtime.
5. Add richer audit entries for policy decisions and sandbox execution results.
