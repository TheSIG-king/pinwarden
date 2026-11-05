# ADR-0001: Record architecture decisions

- Status: Accepted (maintainer, 2026-11-05)
- Date: 2026-11-05

## Context
The project is a security tool maintained by one person with ~5 h/week, assisted by AI agents.
Decisions (protocol strategy, hashing, failure modes, dependencies) must survive context loss
between sessions and be reviewable by the maintainer before code depends on them. CLAUDE.md
requires every new dependency to be justified in an ADR.

## Decision
Use lightweight Architecture Decision Records (Michael Nygard format) in `docs/adr/`:
- File name `NNNN-kebab-title.md`, numbered sequentially, never renumbered.
- Sections: Status, Context, Decision, Alternatives considered, Consequences. ~40 lines max.
- Status lifecycle: `Proposed` → `Accepted` (by the maintainer only) → optionally
  `Superseded by ADR-XXXX` or `Deprecated`. Accepted ADRs are not edited except for status
  and links; a change of mind is a new ADR.
- An ADR is required for: new runtime or dev dependency, protocol/transport strategy, anything
  that changes a security default, lockfile/audit format changes.
- PRs that implement an ADR reference it in the description.

## Alternatives considered
- **No formal record** (README/issues only): cheapest, but rationale gets lost and agents
  re-litigate settled decisions.
- **Heavier templates (MADR full, arc42)**: more structure than a solo project can maintain.

## Consequences
- Small, predictable overhead per decision; agents can read `docs/adr/` as ground truth.
- The maintainer must explicitly accept each ADR; until then implementation is provisional.
