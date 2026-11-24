# Architecture

## Components
- Release agent: Amazon Bedrock AgentCore managed harness.
- Gateway: narrow tool surface with temporal authorization.
- Temporal policy: same-session prerequisites and artifact-digest binding.
- Lambda tools: read staged metadata, run controlled tests, publish to sandbox.
- Human approval: separate authenticated path, not callable by the agent.
- Evidence: AgentCore Observability and CloudWatch traces plus application audit events.
- Investigator: deterministic event correlation and classification, optional AI explanation.
- Report store: dedicated incident-report write operation.

## Workflow
`read artifact -> run tests -> human approval -> publish`

Publication must be denied unless the same session contains a successful test and human approval for the exact same digest, with no failed test for that digest.

## Trust boundaries
User requests and artifact contents are untrusted. Agent reasoning is not an authorization authority. Gateway is the tool authorization boundary; IAM is the cloud permission boundary. The investigator has read-only evidence access. The publisher targets a sandbox only.
