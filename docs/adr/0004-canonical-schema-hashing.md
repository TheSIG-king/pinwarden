# ADR-0004: Canonical schema hashing and the `mcp.lock` format

- Status: Proposed
- Date: 2026-11-05

## Context
Rug-pull detection needs a stable fingerprint of everything the LLM may see about a tool,
reproducible across Python versions and platforms, and a lockfile a human can review in a diff.

## Decision
- **Canonicalization: RFC 8785 (JCS)** via the `rfc8785` package, then **SHA-256**, stored as
  `sha256:<hex>`. No Unicode normalization (NFC/NFKC) before hashing: confusable or invisible
  characters must change the hash.
- **Included: the whole tool object as received**, i.e. `name`, `title`, `description`,
  `inputSchema` (all nested properties, `enum`, `default`, `$defs`, `examples`…),
  `outputSchema`, `annotations`, `icons`, **and any unknown/future field**. Deny-by-default:
  a field we did not anticipate is pinned rather than ignored.
- **Excluded (provisional, see open decision): `_meta`**, hashed separately as `meta_hash`
  (drift = `WARN`). Per server, `serverInfo` and `initialize.instructions` are hashed (drift = `WARN`).
- **Unhashable tool** (`rfc8785` raises on integers beyond ±2^53 or lone surrogates): status
  `UNPINNED`, hidden, `ERROR` event — never a hook crash (ADR-0005). `approve` refuses it.
- **Lockfile `mcp.lock`**: JSON (pretty, sorted keys, LF), next to `gateway.yaml` by default
  (`--lock` to override), written atomically (temp file + rename), created only by
  `pinwarden approve`. Content: `lock_version`, `hash_alg`, and per server → per tool:
  `hash`, `meta_hash`, `approved_at`, `accepted_rules` (detection rule ids explicitly accepted),
  and the canonical `snapshot` (needed to render a readable diff on drift).

## Open decision (maintainer)
Not resolved here: (a) should drift of `initialize.instructions` block rather than `WARN`
(it reaches the LLM); (b) should `_meta` stay excluded from the pin (some clients may surface
it). Both are listed as T2 residual risk in THREAT_MODEL until decided.

## Alternatives considered
- **`json.dumps(sort_keys=True, separators=(',',':'), ensure_ascii=False)`**: zero dependency,
  but number formatting (`1e21`, `-0.0`, floats like `0.1` vs ES6 shortest form) and escaping
  rules are Python-specific and undocumented as a contract; hashes would not be reproducible by
  non-Python tooling. JCS is a published standard with test vectors.
- **Allowlist of fields** (name/description/inputSchema only): misses `outputSchema`,
  `annotations`, `title` and future fields — the exact gap rug-pulls exploit.
- **Hash only, no snapshot**: drift could not be explained as a readable diff.
- **TOML/YAML lockfile**: YAML parsing is a larger attack surface; JSON maps 1:1 to the data.

## Consequences
- One small dependency (`rfc8785`); hashes reproducible by any JCS implementation.
- Lockfile contains full schemas — may be large, but is reviewable in git.
- A server that legitimately changes a cosmetic field (e.g. `icons`) triggers re-approval;
  accepted as the price of completeness.
