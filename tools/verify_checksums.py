#!/usr/bin/env python3
"""
Verify SHA256 checksums listed in a CHECKSUMS.sha256 file.

Format expected (typical sha256sum):
<sha256>  <relative/path/to/file>

- Ignores blank lines and comment lines starting with '#'
- Fails if any file is missing or checksum mismatches
"""

from __future__ import annotations

import hashlib
import os
import sys
from pathlib import Path


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_checksums_file(checksums_path: Path) -> list[tuple[str, Path]]:
    pairs: list[tuple[str, Path]] = []
    for i, raw in enumerate(checksums_path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue

        # Accept "hash  path" (two spaces) or "hash path"
        parts = line.split()
        if len(parts) < 2:
            raise ValueError(f"Invalid line {i} in {checksums_path}: {raw!r}")

        digest = parts[0].lower()
        relpath = " ".join(parts[1:]).strip()
        pairs.append((digest, Path(relpath)))

    if not pairs:
        raise ValueError(f"No checksums found in {checksums_path}")
    return pairs


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: verify_checksums.py <path/to/CHECKSUMS.sha256>", file=sys.stderr)
        return 2

    checksums_path = Path(argv[1]).resolve()
    if not checksums_path.exists():
        print(f"ERROR: checksums file not found: {checksums_path}", file=sys.stderr)
        return 2

    base_dir = checksums_path.parent
    try:
        pairs = parse_checksums_file(checksums_path)
    except Exception as e:
        print(f"ERROR: failed to parse {checksums_path}: {e}", file=sys.stderr)
        return 2

    failures: list[str] = []

    for expected, rel in pairs:
        target = (base_dir / rel).resolve()

        # Ensure the target lives under base_dir (defense-in-depth)
        try:
            target.relative_to(base_dir.resolve())
        except Exception:
            failures.append(f"{rel}: ERROR path escapes base directory")
            continue

        if not target.exists():
            failures.append(f"{rel}: MISSING")
            continue

        actual = sha256_file(target)
        if actual != expected:
            failures.append(f"{rel}: BAD CHECKSUM\n  expected: {expected}\n  actual:   {actual}")

    if failures:
        print("CHECKSUM VERIFICATION FAILED:\n")
        for msg in failures:
            print(f"- {msg}\n")
        return 1

    print(f"OK: verified {len(pairs)} file(s) from {checksums_path.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
