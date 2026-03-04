#!/usr/bin/env python3
"""Synchronize intentionally duplicated scripts and verify drift."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
from pathlib import Path
import shutil
import sys


@dataclass(frozen=True)
class SyncEntry:
    source: Path
    destinations: tuple[Path, ...]


SYNC_MAP: tuple[SyncEntry, ...] = (
    SyncEntry(
        source=Path("scripts/count_text_size.py"),
        destinations=(Path("skills/software-design-doc/scripts/count_text_size.py"),),
    ),
)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _verify_pair(source: Path, destination: Path, verify_hash: bool) -> tuple[bool, str]:
    if not source.exists():
        return False, f"missing source: {source}"
    if not destination.exists():
        return False, f"missing destination: {destination}"

    source_bytes = source.read_bytes()
    destination_bytes = destination.read_bytes()
    is_match = source_bytes == destination_bytes

    if verify_hash:
        return (
            is_match,
            (
                f"{'MATCH' if is_match else 'DIFF '} {source} -> {destination} "
                f"(sha256 src={_sha256(source)} dst={_sha256(destination)})"
            ),
        )

    return is_match, f"{'MATCH' if is_match else 'DIFF '} {source} -> {destination}"


def run_sync(check_only: bool, verify_hash: bool) -> int:
    errors = 0
    for entry in SYNC_MAP:
        source = entry.source
        if not source.exists():
            print(f"ERROR missing source: {source}", file=sys.stderr)
            errors += len(entry.destinations)
            continue

        for destination in entry.destinations:
            if check_only:
                matches, message = _verify_pair(source, destination, verify_hash)
                print(message)
                if not matches:
                    errors += 1
                continue

            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
            matches, message = _verify_pair(source, destination, verify_hash)
            print(f"SYNC  {source} -> {destination}")
            print(message)
            if not matches:
                errors += 1

    return 1 if errors else 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sync duplicated scripts from canonical source paths."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check for drift only; do not copy files.",
    )
    parser.add_argument(
        "--verify-hash",
        action="store_true",
        help="Print SHA-256 hashes for source and destination while comparing.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    return run_sync(check_only=args.check, verify_hash=args.verify_hash)


if __name__ == "__main__":
    sys.exit(main())
