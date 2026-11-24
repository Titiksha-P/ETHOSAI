# AWS Integration Plan

This repository currently contains a local executable reference model, not a deployed AWS service.

## Preflight
- Verify AgentCore managed harness and temporal policy availability in the selected Region.
- Verify a compatible Bedrock model, quotas, account permissions, and pricing.
- Use a sandbox account/environment and configure billing alerts.

## Agent and Gateway
Deploy the release agent with the current AgentCore managed-harness workflow. Expose only the minimum tools through AgentCore Gateway. Preserve the authenticated principal and session ID through the workflow. Do not expose IAM mutation, production deployment, policy administration, or self-approval tools.

## Temporal policy requirements
Implement and validate using current Dogwood syntax:
- `artifact.publish` requires a prior successful `security.test` in the same session.
- The test digest equals the publish request digest.
- Publication requires prior human approval for the same digest and session.
- A failed test blocks publication.
- Missing session history or unavailable authorization fails closed.

The Gateway must independently enforce these requirements. Do not treat the local Python reference model as production authorization.

## Roles
- Artifact reader: read-only staging prefix.
- Test runner: fixed sandbox test command.
- Approval service: authenticated human-only endpoint.
- Publisher: write only to sandbox destination.
- Investigator: read-only sanitized evidence.
- Report writer: write only to incident-report storage.

## Acceptance tests
Demonstrate real Gateway denial for publish-before-test, missing approval, digest substitution, failed-test publication, and cross-session approval reuse. Demonstrate a valid sandbox release and read-only investigator access. Attach actual policy source, sanitized traces, screenshots, and test outputs after execution.
