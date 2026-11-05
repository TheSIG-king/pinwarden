"""stdio framing: split a byte stream into newline-delimited JSON-RPC frames.

The MCP stdio transport sends one JSON-RPC message per line (UTF-8, ``\\n``-terminated,
no embedded newlines). This module only deals with *bytes and lines*; turning a frame
into a message is ``pinwarden.proxy.messages``' job.

This is the first code that touches bytes coming from an untrusted MCP server, so it
must never buffer more than ``max_bytes`` (+ a small constant) for a single frame.

MAINTAINER TASK (Phase 1, mentor mode) — implement ``FrameReader``.
Tests: ``tests/unit/test_framing.py``.
"""

from __future__ import annotations

import asyncio


class FramingError(Exception):
    """The stream can no longer be split into frames safely.

    After this is raised the caller must treat the stream as unusable (close it):
    we do not try to resynchronise on the next newline.
    """


class FrameReader:
    """Reads newline-delimited frames from an ``asyncio.StreamReader``.

    Keeps its **own** buffer: do not rely on ``StreamReader.readline``/``readuntil``,
    whose behaviour depends on the reader's internal ``limit`` (64 KiB by default),
    which is set by whoever created the reader, not by us.
    """

    def __init__(self, reader: asyncio.StreamReader, max_bytes: int) -> None:
        """``max_bytes`` must be >= 1, otherwise ``ValueError``."""
        raise NotImplementedError("Phase 1 maintainer task — see module docstring")

    async def read_frame(self) -> bytes | None:
        """Return the next frame.

        Contract:
        - Returns the line content **without** its terminator (``\\n`` or ``\\r\\n``).
        - Blank lines (empty or whitespace-only) are skipped.
        - Returns ``None`` on a clean EOF (no pending bytes).
        - Raises ``FramingError`` if:
          * a line (without its terminator) is longer than ``max_bytes`` bytes — detected as
            soon as more than ``max_bytes`` bytes without a newline have been received, i.e.
            **without** waiting for the newline or EOF, and without buffering much more than
            ``max_bytes``;
          * EOF occurs in the middle of a line (truncated frame).
        - Works whatever the wrapped reader's own ``limit`` is (MCP messages can be MiB).

        Hint: read fixed-size chunks with ``StreamReader.read(n)`` and split them yourself;
        bytes after a newline belong to the *next* frame.
        """
        raise NotImplementedError("Phase 1 maintainer task — see module docstring")
