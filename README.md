# ETHOSAI

**Temporal Security & Runtime Integrity for AI Agents**

ETHOSAI is a research prototype for a secure software-release agent combining session-aware authorization with deterministic runtime incident investigation.

## Source bundle

The initial 22-file source package is included as [`ETHOSAI-repository.zip`](ETHOSAI-repository.zip). Download and extract it to obtain the complete local project structure.

## Current status

The local Python reference model and tests are implemented. Amazon Bedrock AgentCore harness, Gateway temporal-policy deployment, IAM, Guardrails, CloudWatch ingestion, and human approval integration are not yet deployed. Do not claim AWS enforcement until those integrations are deployed and tested.

## Quick start

Requires Python 3.11+:

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
ethosai demo
```

See `docs/` in the extracted source bundle for architecture, security rules, threat model, AWS integration plan, and experiment reporting.

Use synthetic artifacts and a sandbox target only. Never connect the prototype to production deployment credentials.