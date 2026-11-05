# Contributing

Thanks for your interest! This project is small and security-focused, so the bar for
correctness and test coverage is high, but contributions of attack cases are especially
welcome.

## Setup
```bash
# requires uv (https://docs.astral.sh/uv/)
uv sync
uv run pre-commit install
```

## Before opening a PR
```bash
uv run ruff check . && uv run ruff format --check . && uv run mypy && uv run pytest
```
- Small PRs, one topic each, branched from `main` (`feat/…`, `fix/…`, `docs/…`).
- [Conventional commits](https://www.conventionalcommits.org/): `feat:`, `fix:`,
  `docs:`, `test:`, `refactor:`, `chore:`, `ci:`.
- New behaviour comes with tests. Detectors need **positive and negative** tests.
- New runtime dependency? Add an ADR in `docs/adr/` explaining why.

## Contributing attack cases
Attack cases live in `attacks/` (format documented there from Phase 3). Each case must:
- be runnable **locally** (no network access to third-party systems);
- be labelled with its OWASP category and expected outcome (`block` / `alert`);
- not contain real secrets or real malware payloads.

## Security issues
See [SECURITY.md](SECURITY.md) — never in public issues.

## License
By contributing you agree that your contributions are licensed under Apache-2.0.
