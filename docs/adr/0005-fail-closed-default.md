# ADR-0005: Fail closed by default

- Status: Proposed
- Date: 2026-11-05

## Context
A security proxy that lets traffic through when it cannot decide gives a false sense of
safety. But a proxy that breaks workflows on every hiccup gets uninstalled (THREAT_MODEL AS6).

## Decision
Default mode is `enforce`. In enforce mode, any tool-related situation the gateway cannot
positively validate results in **deny**:
- invalid config/policy → refuse to start (exit non-zero, error on stderr);
- missing/corrupt `mcp.lock` → start but expose no tools, with a hint to run `approve`;
- unpinned, unhashable, drifted or shadowing tool, or a name duplicated within one server's
  `tools/list` → hidden from `tools/list` (all tools with that name), calls refused;
- exception or timeout in any hook → deny that message;
- unparseable/non-strict message (ADR-0006), batch, size/pagination limits → JSON-RPC error;
- unknown method under `tools/*` / `notifications/tools/*` → denied (ADR-0003);
- confirmation not possible (no elicitation support, timeout, decline) → deny;
- audit sink write failure → deny `tools/call` (an unlogged call is not allowed).
Refusals use fixed gateway-authored text and never echo server-provided content.

`monitor` mode (global or per server) is the explicit opt-out: same evaluation, decisions are
logged as `would_deny` but traffic flows. **Monitor never blocks on internal errors**: on a hook
exception it forwards the original message after recording `decision=error` (audit, or stderr
if the sink is down). Protocol-safety rejections (strict parse, batch, size) apply in both modes.

Scoped exception: unknown methods outside `tools/*` pass through, audited (ADR-0003);
invalid YAML never falls back to "allow all".

## Alternatives considered
- **Fail open by default**: better UX, but silently disables protection precisely under attack
  (e.g. a server sending a malformed schema to crash detection).
- **Fail closed everywhere, including unknown methods**: maximal safety, but breaks
  forward-compat with every protocol revision.
- **Prompt the user on every failure**: alert fatigue; not possible on stdio without elicitation.

## Consequences
- First run requires `pinwarden approve`; documentation must make onboarding one command.
- Bugs in the gateway surface as denied calls — integration tests must cover each row above.
- Users can adopt incrementally via `monitor`, then switch to `enforce`.
