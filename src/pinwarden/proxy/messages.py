"""Strict JSON-RPC message parsing (ADR 0006).

The policy engine evaluates the *parsed* message, while a server may parse the raw
bytes with a different JSON library. Any input on which two conforming parsers can
disagree is therefore rejected here, so that what we check is what the server sees.

MAINTAINER TASK (Phase 1, mentor mode) — implement ``parse_message``.
Tests: ``tests/unit/test_messages.py``.
"""

from __future__ import annotations

from typing import Any


class MessageError(Exception):
    """The frame is not an acceptable JSON-RPC 2.0 message."""


def parse_message(raw: bytes) -> dict[str, Any]:
    """Parse one frame into a JSON-RPC message object.

    Reject with ``MessageError`` (never any other exception type):
    - bytes that are not valid UTF-8;
    - invalid JSON;
    - **duplicate keys in any object, at any depth** (e.g. ``{"a":1,"a":2}``);
    - the non-standard constants ``NaN``, ``Infinity``, ``-Infinity``;
    - a top-level value that is not an object — this includes JSON-RPC batches
      (arrays), which pinwarden rejects (ADR 0005);
    - a missing ``"jsonrpc"`` member or one that is not exactly the string ``"2.0"``.

    Everything else is returned as a plain ``dict`` (no Pydantic here; typed models
    come later, only for intercepted methods).

    Rules: no ``eval``/``exec``; use only the standard library ``json`` module.
    Hints: ``json.loads`` accepts ``object_pairs_hook`` and ``parse_constant``.
    """
    raise NotImplementedError("Phase 1 maintainer task — see module docstring")
