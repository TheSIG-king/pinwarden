"""Tests for pinwarden.proxy.messages.parse_message (maintainer task, Phase 1)."""

from __future__ import annotations

import contextlib
import json
from typing import Any

import pytest
from hypothesis import given
from hypothesis import strategies as st

from pinwarden.proxy.messages import MessageError, parse_message


def test_valid_request() -> None:
    msg = parse_message(b'{"jsonrpc":"2.0","id":1,"method":"tools/list"}')
    assert msg == {"jsonrpc": "2.0", "id": 1, "method": "tools/list"}


def test_valid_notification_and_response() -> None:
    assert parse_message(b'{"jsonrpc":"2.0","method":"notifications/initialized"}')
    assert parse_message(b'{"jsonrpc":"2.0","id":"a","result":{}}')


def test_unicode_is_decoded() -> None:
    msg = parse_message('{"jsonrpc":"2.0","method":"m","params":{"q":"é🛡️"}}'.encode())
    assert msg["params"]["q"] == "é🛡️"


@pytest.mark.parametrize(
    "raw",
    [
        pytest.param(b"\xff\xfe{}", id="invalid-utf8"),
        pytest.param(b"{bad json", id="invalid-json"),
        pytest.param(b"", id="empty"),
        pytest.param(b"42", id="top-level-number"),
        pytest.param(b'"2.0"', id="top-level-string"),
        pytest.param(b'[{"jsonrpc":"2.0","id":1,"method":"ping"}]', id="batch"),
        pytest.param(b'{"id":1,"method":"ping"}', id="missing-jsonrpc"),
        pytest.param(b'{"jsonrpc":"1.0","id":1,"method":"ping"}', id="wrong-version"),
        pytest.param(b'{"jsonrpc":2.0,"id":1,"method":"ping"}', id="version-not-string"),
    ],
)
def test_rejected_inputs(raw: bytes) -> None:
    with pytest.raises(MessageError):
        parse_message(raw)


@pytest.mark.parametrize(
    "raw",
    [
        pytest.param(b'{"jsonrpc":"2.0","jsonrpc":"2.0","id":1}', id="top-level"),
        pytest.param(
            b'{"jsonrpc":"2.0","id":1,"method":"tools/call","method":"ping"}',
            id="duplicate-method-routing",
        ),
        pytest.param(
            b'{"jsonrpc":"2.0","id":1,"method":"tools/call",'
            b'"params":{"name":"read","arguments":{"path":"/ok","path":"/etc/passwd"}}}',
            id="nested-argument",
        ),
        pytest.param(
            b'{"jsonrpc":"2.0","id":1,"result":{"a":[{"k":1,"k":2}]}}',
            id="inside-array",
        ),
    ],
)
def test_duplicate_keys_rejected_at_any_depth(raw: bytes) -> None:
    with pytest.raises(MessageError):
        parse_message(raw)


@pytest.mark.parametrize("const", ["NaN", "Infinity", "-Infinity"])
def test_non_finite_constants_rejected(const: str) -> None:
    raw = f'{{"jsonrpc":"2.0","id":1,"result":{{"x":{const}}}}}'.encode()
    with pytest.raises(MessageError):
        parse_message(raw)


def test_only_message_error_escapes() -> None:
    """Deeply nested input must not leak RecursionError or anything else."""
    raw = b'{"jsonrpc":"2.0","id":1,"result":' + b"[" * 100_000 + b"]" * 100_000 + b"}"
    with contextlib.suppress(MessageError):
        parse_message(raw)


json_values = st.recursive(
    st.none()
    | st.booleans()
    | st.integers(min_value=-(2**53), max_value=2**53)
    | st.floats(allow_nan=False, allow_infinity=False)
    | st.text(),
    lambda children: (
        st.lists(children, max_size=4) | st.dictionaries(st.text(max_size=8), children, max_size=4)
    ),
    max_leaves=20,
)


@given(params=st.dictionaries(st.text(max_size=8), json_values, max_size=5))
def test_roundtrip_valid_messages(params: dict[str, Any]) -> None:
    msg = {"jsonrpc": "2.0", "id": 7, "method": "tools/call", "params": params}
    assert parse_message(json.dumps(msg, ensure_ascii=False).encode()) == msg
