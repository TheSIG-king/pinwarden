"""Tests for pinwarden.proxy.framing.FrameReader (maintainer task, Phase 1)."""

from __future__ import annotations

import asyncio

import pytest
from hypothesis import given
from hypothesis import strategies as st

from pinwarden.proxy.framing import FrameReader, FramingError

MAX = 1024


def make_reader(data: bytes, *, eof: bool = True, limit: int = 2**16) -> asyncio.StreamReader:
    reader = asyncio.StreamReader(limit=limit)
    reader.feed_data(data)
    if eof:
        reader.feed_eof()
    return reader


async def read_frame(reader: asyncio.StreamReader | FrameReader, max_bytes: int) -> bytes | None:
    """Convenience: accept a raw StreamReader (wrapped once) or an existing FrameReader."""
    frames = reader if isinstance(reader, FrameReader) else FrameReader(reader, max_bytes)
    return await frames.read_frame()


async def test_single_frame_then_eof() -> None:
    reader = FrameReader(make_reader(b'{"jsonrpc":"2.0","id":1,"method":"ping"}\n'), MAX)
    assert await read_frame(reader, MAX) == b'{"jsonrpc":"2.0","id":1,"method":"ping"}'
    assert await read_frame(reader, MAX) is None


async def test_two_frames() -> None:
    reader = FrameReader(make_reader(b"first\nsecond\n"), MAX)
    assert await read_frame(reader, MAX) == b"first"
    assert await read_frame(reader, MAX) == b"second"
    assert await read_frame(reader, MAX) is None


async def test_crlf_terminator_is_stripped() -> None:
    reader = make_reader(b"frame\r\n")
    assert await read_frame(reader, MAX) == b"frame"


async def test_blank_lines_are_skipped() -> None:
    reader = FrameReader(make_reader(b"\n  \n\r\nframe\n\n"), MAX)
    assert await read_frame(reader, MAX) == b"frame"
    assert await read_frame(reader, MAX) is None


async def test_empty_stream_is_clean_eof() -> None:
    assert await read_frame(make_reader(b""), MAX) is None


async def test_utf8_bytes_are_preserved() -> None:
    payload = '{"q":"café ☕ 🛡️"}'.encode()
    assert await read_frame(make_reader(payload + b"\n"), MAX) == payload


async def test_frame_exactly_at_limit_is_accepted() -> None:
    payload = b"x" * MAX
    assert await read_frame(make_reader(payload + b"\n"), MAX) == payload


async def test_frame_over_limit_raises() -> None:
    with pytest.raises(FramingError):
        await read_frame(make_reader(b"x" * (MAX + 1) + b"\n"), MAX)


async def test_oversized_line_detected_without_newline_ever_arriving() -> None:
    """A hostile server streams an endless line: we must fail without waiting for EOF."""
    reader = make_reader(b"x" * (MAX * 8), eof=False)
    with pytest.raises(FramingError):
        await asyncio.wait_for(read_frame(reader, MAX), timeout=2)


async def test_truncated_frame_at_eof_raises() -> None:
    with pytest.raises(FramingError):
        await read_frame(make_reader(b'{"jsonrpc":"2.0"'), MAX)


async def test_max_bytes_larger_than_reader_limit() -> None:
    """MCP messages can exceed asyncio's default 64 KiB reader limit."""
    payload = b"y" * 200_000
    reader = make_reader(payload + b"\n", limit=2**16)
    assert await read_frame(reader, 1_000_000) == payload


async def test_invalid_max_bytes() -> None:
    with pytest.raises(ValueError, match="max_bytes"):
        FrameReader(make_reader(b"x\n"), 0)


async def test_bytes_after_newline_belong_to_next_frame() -> None:
    """Frames split across arbitrary chunk boundaries, fed incrementally."""
    raw = asyncio.StreamReader()
    frames = FrameReader(raw, MAX)
    raw.feed_data(b"ab")
    raw.feed_data(b"c\nde")
    raw.feed_data(b"f\n")
    raw.feed_eof()
    assert await frames.read_frame() == b"abc"
    assert await frames.read_frame() == b"def"
    assert await frames.read_frame() is None


@given(
    st.lists(
        st.binary(min_size=1, max_size=200).filter(
            lambda b: b"\n" not in b and b"\r" not in b and b.strip() != b""
        ),
        max_size=20,
    )
)
async def test_roundtrip_any_sequence_of_frames(frames: list[bytes]) -> None:
    reader = FrameReader(make_reader(b"".join(f + b"\n" for f in frames)), MAX)
    out = []
    while (frame := await read_frame(reader, MAX)) is not None:
        out.append(frame)
    assert out == frames
