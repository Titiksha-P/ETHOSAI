# Contributing

- Create a feature branch.
- Add tests for security-relevant changes.
- Keep authorization deterministic and fail closed.
- Never commit credentials, production artifacts, or sensitive trace payloads.
- Distinguish attempted, denied, and completed actions.
- Run `pytest` and `ruff check src tests` before opening a pull request.
