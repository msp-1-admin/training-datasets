#!/usr/bin/env python3
"""
Validate that one or more .jsonl files parse correctly.

Rules enforced:
- File must be UTF-8 decodable
- Each non-empty line must be valid JSON
- Fails fast with filename + line number + error

This does NOT enforce a schema; it only guarantees JSON correctness.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def validate_file(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as e:
        return [f"{path}: ERROR not valid UTF-8: {e}"]

    for lineno, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not line:
            continue
        try:
            json.loads(line)
        except json.JSONDecodeError as e:
            errors.append(
                f"{path}:{lineno}: JSON decode error: {e.msg} (col {e.colno})"
            )
    return errors


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: validate_jsonl.py <file1.jsonl> [file2.jsonl ...]", file=sys.stderr)
        return 2

    paths = [Path(a) for a in argv[1:]]
    failures: list[str] = []

    for p in paths:
        if not p.exists():
            failures.append(f"{p}: MISSING")
            continue
        if p.is_dir():
            failures.append(f"{p}: is a directory (expected file)")
            continue
        failures.extend(validate_file(p))

    if failures:
        print("JSONL VALIDATION FAILED:\n")
        for msg in failures:
            print(f"- {msg}")
        return 1

    print(f"OK: validated {len(paths)} file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
