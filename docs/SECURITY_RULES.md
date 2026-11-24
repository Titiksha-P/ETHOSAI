# ETHOSAI Security Rules

| ID | Rule | Intended enforcement |
|---|---|---|
| R01 | Read only approved staging artifacts and sanitized traces. | IAM, S3 prefix scope, validation |
| R02 | Successful test must precede publication. | AgentCore Gateway temporal policy |
| R03 | Test, approval, and publication must bind to the same digest. | Temporal policy and digest validation |
| R04 | Failed test blocks publication. | Temporal forbid condition |
| R05 | Only authenticated humans can approve. | Separate human-only endpoint |
| R06 | Agent cannot modify IAM or policy configuration. | No tool exposure; least privilege |
| R07 | Retrieved content and traces are untrusted. | Input isolation and Guardrails |
| R08 | Demo publishes only to sandbox. | Tool target allowlist and IAM |
| R09 | Investigator cannot modify source evidence. | Read-only evidence access |
| R10 | Missing or conflicting evidence fails closed. | Deterministic validation |

A denied action is an attempted violation, not a successful compromise. A model statement is not proof that a tool operation succeeded. Missing evidence must be reported as inconclusive.
