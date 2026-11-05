# ADR-0002: Python 3.12 + uv stack and runtime dependencies

- Status: Proposed
- Date: 2026-11-05

## Context
Target users install the gateway next to MCP clients on laptops; the official MCP SDK and most
community servers are Python/TypeScript. The maintainer knows Python. Each runtime dependency
enlarges the attack surface of a security tool, so each one must earn its place.

## Decision
Python ≥3.12, packaged with **uv** (`uv.lock` committed, `src/` layout, entry point `pinwarden`).

Runtime dependencies (all pinned via `uv.lock`):
| Package | Why | Used by |
|---|---|---|
| `mcp` (2.3.x) | Typed protocol models for intercepted methods, protocol version constants; transitively brings `httpx`, `starlette`, `uvicorn`, `anyio` | proxy |
| `pydantic` v2 | Strict validation of config, policy, lockfile, audit events | all |
| `pyyaml` | `gateway.yaml`/`policy.yaml`, `safe_load` only | policy, config |
| `structlog` | Structured stderr diagnostics and JSONL rendering with one processor chain | audit, cli |
| `rfc8785` | RFC 8785 JSON canonicalization (ADR-0004); small, pure Python, no deps | pinning |
| `httpx`, `starlette`, `uvicorn` | Phase 2 HTTP proxy; declared **directly** (not relied on transitively) because we import them | proxy/http |

Optional extra `otel`: `opentelemetry-sdk` + `opentelemetry-exporter-otlp`. The JSONL format is
OTel-compatible on its own; the SDK is only needed to *export* to a collector, and it is a
large dependency tree most users won't need.

Not a dependency: CLI framework (stdlib `argparse` is enough), Unicode confusables library
(TR39 subset vendored as generated data with its licence notice).

Dev: pytest, pytest-asyncio, hypothesis, ruff, mypy (strict on `src/`), pre-commit
(+ detect-secrets), pip-audit in CI. Docker: `python:3.12-slim`, non-root user, uv-built venv.

## Alternatives considered
- **TypeScript**: first-class SDK too, but maintainer productivity and hypothesis-style testing favour Python.
- **Go/Rust**: lower latency and single binary, but no official SDK parity and slower solo iteration.
- **pip/poetry**: uv is faster and gives a single lockfile + tool runner.
- **click/typer**: nicer UX, not worth a dependency for 5 subcommands.

## Consequences
- Startup time of a Python process per stdio server (measured in `bench/`, not assumed).
- Pinning `mcp` to `2.3.x` exposes us to SDK API churn; mitigated by ADR-0003 (we use only its types).
- **To verify before Phase 1**: exact `mcp` 2.3.0 module paths for types and its Python floor.
