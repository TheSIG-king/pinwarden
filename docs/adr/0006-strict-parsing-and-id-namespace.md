# ADR-0006: Strict parsing, validated re-serialization and the gateway id namespace

- Status: Proposed
- Date: 2026-11-05

## Context
The gateway decides on a parsed `dict` but, in a raw relay (ADR-0003), could forward the raw
bytes. Any difference between how the gateway and the upstream parse the same bytes is a
policy bypass: with `{"name":"read_file","name":"delete_file"}` Python keeps the last key,
another parser may keep the first. `NaN`/`Infinity` are accepted by Python's `json` but are not
JSON. Separately, the gateway originates its own requests (elicitation, paginated `tools/list`)
on connections whose id space belongs to the peers.

## Decision
- **Strict parse of every frame** (dispatch itself reads `method`/`id`, so a duplicated
  `method` key is a routing differential): `json.loads` with an `object_pairs_hook` that raises
  on duplicate keys and a `parse_constant` that raises on `NaN`/`Infinity`/`-Infinity`.
  Failure → JSON-RPC `-32700`/`-32600` error to the sender if an id is recoverable, otherwise
  drop; never forwarded; audited. Same in `monitor` (protocol safety).
- **Forward what was checked.** A `tools/call` allowed by policy is forwarded as
  `json.dumps(validated_obj, ensure_ascii=False, allow_nan=False)` of the exact object the
  policy evaluated (not a Pydantic re-dump, not the raw bytes). Non-intercepted messages are
  still relayed byte-for-byte: they were strictly parsed, so their bytes are unambiguous.
- **Reserved id prefix `pinwarden-`** (`pinwarden-<uuid4>`) for **all** gateway-originated
  requests in both directions: `elicitation/create` to the client, `tools/list` page fetches
  to the server. A peer request using a string id with that prefix is rejected (`-32600`), and
  a response with such an id that is not in the pending table is dropped and audited.
- **Pending table keyed by `(json_type, raw_value)`**, one table per direction: `1`, `1.0` and
  `"1"` are three distinct ids (Python's `1 == 1.0` must not merge them). Booleans/null/objects
  as request ids are rejected.

## Alternatives considered
- **Forward raw bytes after checking the parsed dict**: simplest, but is the differential.
- **Re-serialize every message**: removes the differential everywhere but alters formatting of
  traffic we do not inspect, for no gain once strict parsing makes the bytes unambiguous.
- **Rewrite peer ids into a gateway space**: avoids the prefix rule but breaks `Mcp-Session-Id`
  correlation and makes audit ids differ from client logs.

## Consequences
- Large integers survive (Python ints are exact); key order may change on re-serialization,
  which JSON-RPC permits. A peer that emits duplicate keys is incompatible by design.
- Tests: duplicate keys at every nesting level, `NaN` in arguments, prefix spoofing in both
  directions, `1`/`1.0`/`"1"` id collisions.
