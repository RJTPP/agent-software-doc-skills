#!/usr/bin/env python3
"""Synchronize duplicated files and verify drift."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import shutil
import sys
from typing import Any


@dataclass(frozen=True)
class SyncEntry:
    source: Path
    destinations: tuple[Path, ...]


def _is_within_root(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def _resolve_repo_path(raw_path: str, repo_root: Path, label: str) -> Path:
    candidate = Path(raw_path)
    resolved = candidate.resolve() if candidate.is_absolute() else (repo_root / candidate).resolve()
    if not _is_within_root(resolved, repo_root):
        raise ValueError(f"{label} path must be inside repository root: {raw_path}")
    return resolved


def _display(path: Path, repo_root: Path) -> str:
    try:
        return str(path.relative_to(repo_root))
    except ValueError:
        return str(path)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _verify_pair(
    source: Path,
    destination: Path,
    verify_hash: bool,
    repo_root: Path,
) -> tuple[bool, str]:
    if not source.exists():
        return False, f"missing source: {_display(source, repo_root)}"
    if not destination.exists():
        return False, f"missing destination: {_display(destination, repo_root)}"

    source_bytes = source.read_bytes()
    destination_bytes = destination.read_bytes()
    is_match = source_bytes == destination_bytes

    if verify_hash:
        return (
            is_match,
            (
                f"{'MATCH' if is_match else 'DIFF '} {_display(source, repo_root)} -> {_display(destination, repo_root)} "
                f"(sha256 src={_sha256(source)} dst={_sha256(destination)})"
            ),
        )

    return (
        is_match,
        f"{'MATCH' if is_match else 'DIFF '} {_display(source, repo_root)} -> {_display(destination, repo_root)}",
    )


def _entries_from_json_map(map_path: Path, repo_root: Path) -> list[SyncEntry]:
    try:
        payload = json.loads(map_path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ValueError(f"Could not read map file {map_path}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in map file {map_path}: {exc}") from exc

    raw_entries: Any
    if isinstance(payload, dict):
        raw_entries = payload.get("entries")
    else:
        raw_entries = payload

    if not isinstance(raw_entries, list):
        raise ValueError("Map must be a JSON array or an object with an 'entries' array.")

    entries: list[SyncEntry] = []
    for idx, item in enumerate(raw_entries):
        if not isinstance(item, dict):
            raise ValueError(f"Map entry at index {idx} must be an object.")

        source_raw = item.get("source")
        destinations_raw = item.get("destinations")
        if not isinstance(source_raw, str):
            raise ValueError(f"Map entry {idx} missing string 'source'.")
        if not isinstance(destinations_raw, list) or not destinations_raw:
            raise ValueError(f"Map entry {idx} requires non-empty 'destinations' list.")
        if any(not isinstance(value, str) for value in destinations_raw):
            raise ValueError(f"Map entry {idx} destinations must all be strings.")

        source = _resolve_repo_path(source_raw, repo_root, "source")
        destinations = tuple(
            _resolve_repo_path(destination_raw, repo_root, "destination")
            for destination_raw in destinations_raw
        )
        entries.append(SyncEntry(source=source, destinations=destinations))

    return entries


def _resolve_entries(args: argparse.Namespace, repo_root: Path) -> list[SyncEntry]:
    has_inline = bool(args.src or args.dst)

    if has_inline and args.map:
        raise ValueError("Use either --map or --src/--dst, not both.")
    if args.src and not args.dst:
        raise ValueError("--dst is required when --src is provided.")
    if args.dst and not args.src:
        raise ValueError("--src is required when --dst is provided.")

    if args.src and args.dst:
        source = _resolve_repo_path(args.src, repo_root, "source")
        destinations = tuple(
            _resolve_repo_path(destination_raw, repo_root, "destination")
            for destination_raw in args.dst
        )
        return [SyncEntry(source=source, destinations=destinations)]

    if args.map:
        return _entries_from_json_map(Path(args.map), repo_root)

    raise ValueError("Provide either --src with one or more --dst values, or --map.")


def run_sync(entries: list[SyncEntry], check_only: bool, verify_hash: bool, repo_root: Path) -> int:
    errors = 0
    for entry in entries:
        source = entry.source
        if not source.exists():
            print(f"ERROR missing source: {_display(source, repo_root)}", file=sys.stderr)
            errors += len(entry.destinations)
            continue

        for destination in entry.destinations:
            if check_only:
                matches, message = _verify_pair(source, destination, verify_hash, repo_root)
                print(message)
                if not matches:
                    errors += 1
                continue

            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
            matches, message = _verify_pair(source, destination, verify_hash, repo_root)
            print(f"SYNC  {_display(source, repo_root)} -> {_display(destination, repo_root)}")
            print(message)
            if not matches:
                errors += 1

    return 1 if errors else 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Sync duplicated files from canonical source paths. "
            "Provide --src/--dst or --map JSON."
        )
    )
    parser.add_argument(
        "--src",
        default=None,
        help="Source path for one-off sync/check. Must be inside repository root.",
    )
    parser.add_argument(
        "--dst",
        action="append",
        default=[],
        help="Destination path for one-off sync/check. Repeat for multiple destinations.",
    )
    parser.add_argument(
        "--map",
        default=None,
        help="Path to JSON mapping file. Format: [{'source': '...', 'destinations': ['...']}].",
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
    repo_root = Path.cwd().resolve()
    try:
        entries = _resolve_entries(args, repo_root)
    except ValueError as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 1
    return run_sync(entries=entries, check_only=args.check, verify_hash=args.verify_hash, repo_root=repo_root)


if __name__ == "__main__":
    sys.exit(main())
