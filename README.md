# Secure GPU Agent Lab

## Purpose
This project provides a minimal, policy-driven Python agent for safe document processing in a restricted workspace. It is designed to read only approved content, refuse secret material, and keep all output inside allowed directories.

## Folder Structure
- agents/ — agent implementation
- allowed_docs/ — approved input documents
- allowed_output/ — permitted output reports
- logs/ — audit logs
- secrets/ — blocked sensitive content
- tests/ — regression tests
- policy.yaml — simple policy configuration

## Safety Rules
- Reads are limited to paths defined in policy.yaml
- Paths under secrets/ are blocked
- Writes are restricted to allowed_output/ and logs/
- Network access is disabled by policy unless explicitly changed

## How to Run
Run the setup script from the project root:

```bash
./setup.sh
```

## What the Tests Verify
The test suite confirms that:
- allowed_docs/ content can be read
- secrets/ content is refused
- writes outside allowed_output/ and logs/ are blocked
- network access disabled by policy is recognized

## Current Status
The core agent and policy enforcement are implemented, and the test suite passes.

## Next Milestone
Connect the agent to OpenShell / NemoClaw for external task execution while preserving the same safety boundaries.
