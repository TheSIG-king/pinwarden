# ADR-0003: Proxy relay strategy — raw JSON-RPC relay with typed parsing of intercepted methods

- Status: Accepted (maintainer, 2026-11-05)
- Date: 2026-11-05

## Context
The gateway must be transparent to arbitrary clients and servers, across protocol revisions,
while inspecting `initialize`, `tools/list`, `tools/call` and `notifications/tools/list_changed`.

## Decision
**Raw message relay.** Each transport yields JSON-RPC messages as `dict`s. The interceptor
dispatches on `method` (and on response `id` via the pending table); only intercepted methods
are parsed with typed models (SDK `mcp.types` where it fits, own `extra="allow"` models
otherwise). Other messages are forwarded byte-for-byte (stdio) or as the parsed dict (HTTP/SSE).
Pinning hashes the **raw received dict**, never a model re-serialization, so fields the SDK
does not know about are still pinned. The SDK is also used to write local test servers/clients.

**No parse differential (ADR-0006).** Frames are parsed strictly: duplicate object keys and
`NaN`/`Infinity` are rejected with a JSON-RPC error. A `tools/call` that passes policy is
forwarded as the **re-serialization of the validated object**, never the raw bytes, so the
upstream receives exactly what was checked.

**Unknown methods.** In `enforce` mode, any unknown method in the tool namespace (`tools/*`,
`notifications/tools/*` other than the intercepted ones) is **denied** (request: JSON-RPC
error; notification: dropped). All other unknown methods pass through and are audited.

## Alternatives considered
| Criterion | Raw relay (chosen) | Re-implement via SDK `ClientSession` + `Server` | Wrap a server in-process |
|---|---|---|---|
| Protocol fidelity | High: unknown fields/methods pass untouched; ids preserved | Lossy: every message is re-modelled; unknown fields dropped or rejected; capabilities re-negotiated by the gateway | High, but only for Python servers we can import |
| Maintenance | Own framing (~100 LOC stdio) + SSE handling for HTTP | Low code, but every SDK release can change behaviour of a man-in-the-middle the SDK was not designed for | Per-server glue |
| Forward-compat (new methods) | Passthrough outside `tools/*` | Each new method must be explicitly bridged, otherwise silently broken | N/A |
| Security | Small attack surface; must handle framing ourselves | Two full protocol stacks to reason about | Shares process with untrusted code — unacceptable |
| Language-agnostic upstream | Yes | Yes | No |

Wrapping is rejected (runs untrusted code in-process, not transparent). SDK re-implementation
is rejected for fidelity and forward-compat: a security proxy that silently drops what it does
not understand creates confusing failures and pushes users to bypass it.

## Consequences
- We own: newline framing and size limits (stdio), SSE parsing/re-emission and session header
  handling (HTTP), request-id correlation and the `pinwarden-` id namespace (ADR-0006).
- A new tool-related method in a future protocol revision is blocked until supported:
  fail-closed wins over forward-compat inside `tools/*` (ADR-0005).
- JSON-RPC batches (removed in recent protocol revisions) are rejected with an error.
- Integration tests must cover at least the two latest protocol revisions using SDK-based
  local fixture servers, plus a hand-written raw server sending unknown fields/methods.
