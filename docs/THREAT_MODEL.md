# Threat Model

## Assets
Staged artifacts and SHA-256 digests; test outcomes; human approvals; execution traces; IAM roles; incident reports.

## Threat actors
Users attempting policy bypass; malicious artifact instructions; misbehaving agents; cross-session approval attackers; report consumers inducing false claims.

## Threats and mitigations
| Threat | Mitigation |
|---|---|
| Publish before test | Temporal policy requires prior successful test |
| Artifact substitution | Bind test, approval, and publish to digest |
| Cross-session approval reuse | Session-scoped authorization |
| Failed scan bypass | Temporal forbid condition |
| Prompt injection | Treat artifact as untrusted; no policy mutation tool |
| Agent self-approval | Separate human-only identity |
| Evidence tampering | Read-only source evidence |
| False breach claim | Distinguish denied from completed events |
| Missing logs | Mark investigation inconclusive |

Out of scope: production deployment, arbitrary malware detection, proof that a test suite is complete, or guarantees against all prompt injection.
