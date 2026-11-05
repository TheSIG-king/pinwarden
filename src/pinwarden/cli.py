"""Command-line entry point.

Phase 0 only exposes ``--version``. Subcommands (``run``, ``approve``, ``scan``)
arrive in later phases; see docs/ARCHITECTURE.md.
"""

from __future__ import annotations

import argparse
from collections.abc import Sequence

from pinwarden import __version__


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pinwarden",
        description="Runtime security gateway between MCP clients and MCP servers.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    parser.parse_args(argv)
    parser.print_help()
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
