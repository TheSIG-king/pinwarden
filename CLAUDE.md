# CLAUDE.md — working rules for AI agents on this repository

## Project
Runtime security gateway for MCP (Model Context Protocol): a transparent proxy between
an MCP client and its MCP servers providing full-schema pinning (rug-pull detection),
static poisoning/shadowing detection, a YAML policy engine and a JSONL/OpenTelemetry
audit log. See `docs/ARCHITECTURE.md` and `docs/THREAT_MODEL.md`.

## Governance
- The maintainer (human) is the decision-maker. Each phase ends at a CHECKPOINT:
  stop, report, and wait for an explicit "OK phase N".
- Ask the maintainer FIRST for irreversible or ambiguous decisions: project name,
  license, repo visibility, PyPI publication, deleting code or history.
- If blocked after 2 attempts on the same problem: stop and present options.
- Mentor mode: each phase, at least one key part is implemented by the maintainer
  (statement + tests provided by the agent). Never implement that part for them.

## Language
- Code, comments, commits, README, docs: English.
- Conversation with the maintainer: French.

## Workflow
- Never push to `main`. One PR per phase or several small PRs.
- One feature = one branch / worktree (`feat/<short-name>`).
- Conventional commits: `feat:`, `fix:`, `docs:`, `test:`, `refactor:`, `chore:`, `ci:`.
- The `reviewer` agent reviews every PR before the maintainer; blocking remarks are
  fixed or explicitly justified in the PR.
- Every new dependency is justified in an ADR (`docs/adr/`).

## Quality gates (must pass before any PR)
```bash
uv run ruff check . && uv run ruff format --check . && uv run mypy && uv run pytest
```
- mypy strict on `src/`. No `# type: ignore` without a reason comment.
- Tests: `tests/unit`, `tests/integration` (local MCP servers), `tests/adversarial`.
  Each detector needs positive AND negative tests.

## Security rules (non-negotiable)
- Ethics: NO scanning, connecting to or attacking third-party systems. All malicious
  MCP servers are written and run LOCALLY for tests only.
- No secrets in the repo or logs. Pre-commit (detect-secrets) must stay active.
- Strict input validation (Pydantic), no `eval`/`exec`, no `shell=True`, no unescaped
  shell, no `pickle` on untrusted data, `yaml.safe_load` only.
- Dependencies pinned (`uv.lock`), GitHub Actions pinned by SHA, Docker image non-root.
- Fail closed: when the gateway cannot decide, it blocks (see ADR 0005).

## Honesty
- No estimated or invented numbers. Every figure in README comes from `bench/` and is
  reproducible. No feature announced unless implemented. Known limitations documented.
- Cite sources with links; OWASP IDs/titles must be checked against official sources
  (`docs/research/SOURCES.md`).

## Sub-agents (`.claude/agents/`)
architect (fable → fallback opus), researcher (opus), implementer (opus),
red-team (opus), reviewer (fable → fallback opus; never reviews code it wrote),
docs (sonnet). If a model is unavailable or refuses a local defensive-testing task,
switch to opus and report it at the checkpoint.
