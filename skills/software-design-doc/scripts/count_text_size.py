#!/usr/bin/env python3
# Copy Reference: count_text_size.py
# Version: 1.2.0
# Synced-On: 2026-03-04
# NOTE: This file is intentionally duplicated in:
# - scripts/count_text_size.py
# - skills/software-design-doc/scripts/count_text_size.py
"""Count file text size metrics with optional Markdown section breakdown."""

from __future__ import annotations

import argparse
from glob import glob
import json
from pathlib import Path
import re
import sys
from typing import Any

SCRIPT_VERSION = "1.2.0"
WORD_RE = re.compile(r"\S+")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
FENCE_RE = re.compile(r"^(```+|~~~+)")
FILE_FMT = "{:<{file_w}} {:>8} {:>8} {:>8} {:>7} {:<8} {}"


def _count_text(text: str) -> dict[str, int]:
    return {
        "chars": len(text),
        "words": len(WORD_RE.findall(text)),
        "lines": len(text.splitlines()),
    }


def _is_markdown_file(path: Path) -> bool:
    return path.suffix.lower() in {".md", ".markdown"}


def _normalize_heading_text(raw: str) -> str:
    normalized = raw.strip()
    normalized = re.sub(r"\s+#+\s*$", "", normalized)
    return normalized.strip()


def _markdown_sections(text: str) -> list[dict[str, Any]]:
    lines = text.splitlines()
    headings: list[tuple[int, str, int]] = []
    in_fence = False
    fence_char = ""
    fence_len = 0

    for idx, line in enumerate(lines):
        stripped = line.lstrip()
        fence_match = FENCE_RE.match(stripped)
        if fence_match:
            marker = fence_match.group(1)
            if not in_fence:
                in_fence = True
                fence_char = marker[0]
                fence_len = len(marker)
            elif marker[0] == fence_char and len(marker) >= fence_len:
                in_fence = False
                fence_char = ""
                fence_len = 0
            continue

        if in_fence:
            continue

        heading_match = HEADING_RE.match(stripped)
        if not heading_match:
            continue

        level = len(heading_match.group(1))
        heading_text = _normalize_heading_text(heading_match.group(2))
        headings.append((level, heading_text, idx))

    sections: list[dict[str, Any]] = []
    for heading_idx, (level, heading_text, line_idx) in enumerate(headings):
        next_line_idx = len(lines)
        for next_level, _, candidate_line_idx in headings[heading_idx + 1 :]:
            if next_level <= level:
                next_line_idx = candidate_line_idx
                break

        section_text = "\n".join(lines[line_idx:next_line_idx])
        counts = _count_text(section_text)
        sections.append(
            {
                "heading_level": level,
                "heading_text": heading_text,
                "section_chars": counts["chars"],
                "section_words": counts["words"],
                "section_lines": counts["lines"],
            }
        )

    return sections


def _analyze_path(path: Path, encoding: str, by_heading: bool) -> dict[str, Any]:
    row: dict[str, Any] = {
        "file": str(path),
        "chars": 0,
        "words": 0,
        "lines": 0,
        "is_markdown": _is_markdown_file(path),
        "status": "ok",
        "error": None,
        "sections": [],
    }

    if not path.exists():
        row["status"] = "error"
        row["error"] = "File does not exist."
        return row

    if not path.is_file():
        row["status"] = "error"
        row["error"] = "Path is not a file."
        return row

    try:
        text = path.read_text(encoding=encoding)
    except OSError as exc:
        row["status"] = "error"
        row["error"] = str(exc)
        return row
    except UnicodeDecodeError as exc:
        row["status"] = "error"
        row["error"] = f"Decode error with encoding {encoding}: {exc}"
        return row

    counts = _count_text(text)
    row["chars"] = counts["chars"]
    row["words"] = counts["words"]
    row["lines"] = counts["lines"]

    if by_heading and row["is_markdown"]:
        row["sections"] = _markdown_sections(text)

    return row


def _analyze_stdin(by_heading: bool) -> dict[str, Any]:
    text = sys.stdin.read()
    counts = _count_text(text)
    row: dict[str, Any] = {
        "file": "-",
        "chars": counts["chars"],
        "words": counts["words"],
        "lines": counts["lines"],
        "is_markdown": by_heading,
        "status": "ok",
        "error": None,
        "sections": [],
    }
    if by_heading:
        row["sections"] = _markdown_sections(text)
    return row


def _totals(rows: list[dict[str, Any]]) -> dict[str, int]:
    return {
        "chars": sum(row["chars"] for row in rows),
        "words": sum(row["words"] for row in rows),
        "lines": sum(row["lines"] for row in rows),
        "files": len(rows),
        "errors": sum(1 for row in rows if row["status"] == "error"),
    }


def _to_table(rows: list[dict[str, Any]], by_heading: bool) -> str:
    file_width = max(20, max((len(row["file"]) for row in rows), default=4))
    totals = _totals(rows)
    header_line = FILE_FMT.format("file", "chars", "words", "lines", "md", "status", "error", file_w=file_width)
    divider_line = "-" * len(header_line)

    lines = [
        header_line,
        divider_line,
    ]
    for row in rows:
        lines.append(
            FILE_FMT.format(
                row["file"],
                row["chars"],
                row["words"],
                row["lines"],
                "yes" if row["is_markdown"] else "no",
                row["status"],
                row["error"] or "",
                file_w=file_width,
            )
        )
        if by_heading and row["sections"]:
            heading_width = max(20, max((len(f"h{s['heading_level']}: {s['heading_text']}") for s in row["sections"]), default=7))
            section_fmt = f"  {{:<{heading_width}}} {{:>8}} {{:>8}} {{:>8}}"
            lines.append(section_fmt.format("heading", "chars", "words", "lines"))
            for section in row["sections"]:
                heading_label = f"h{section['heading_level']}: {section['heading_text']}"
                lines.append(
                    section_fmt.format(
                        heading_label,
                        section["section_chars"],
                        section["section_words"],
                        section["section_lines"],
                    )
                )
    lines.append(divider_line)
    lines.append(
        FILE_FMT.format(
            "TOTAL",
            totals["chars"],
            totals["words"],
            totals["lines"],
            "-",
            "mixed" if totals["errors"] else "ok",
            f"files={totals['files']} errors={totals['errors']}",
            file_w=file_width,
        )
    )
    return "\n".join(lines)


def _resolve_inputs(paths: list[str], globs: list[str]) -> list[str]:
    resolved: list[str] = []
    seen: set[str] = set()

    for path in paths:
        if path == "-":
            # Keep repeated stdin markers so downstream logic can emit an explicit error row.
            resolved.append(path)
            continue
        if path not in seen:
            resolved.append(path)
            seen.add(path)

    for pattern in globs:
        for match in sorted(glob(pattern, recursive=True)):
            if match == "-":
                # Defensive only; glob results should not produce '-'.
                resolved.append(match)
                continue
            if match not in seen:
                resolved.append(match)
                seen.add(match)

    return resolved


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Count file chars/words/lines with optional Markdown heading breakdown."
    )
    parser.add_argument("paths", nargs="*", help="One or more file paths. Use '-' to read from stdin.")
    parser.add_argument(
        "--glob",
        action="append",
        default=[],
        help="Glob pattern to expand as input files. Repeat flag for multiple patterns.",
    )
    parser.add_argument(
        "--by-heading",
        action="store_true",
        help="Include per-heading section counts for Markdown files.",
    )
    parser.add_argument(
        "--format",
        choices=["table", "json"],
        default="table",
        help="Output format.",
    )
    parser.add_argument("--out", default=None, help="Optional output file path.")
    parser.add_argument("--encoding", default="utf-8", help="Text encoding for file reads.")
    parser.add_argument(
        "--fail-on-error",
        action="store_true",
        help="Exit with code 1 if any file has status=error.",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Print script version and exit.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.version:
        print(f"count_text_size.py {SCRIPT_VERSION}")
        return 0

    inputs = _resolve_inputs(args.paths, args.glob)
    if not inputs:
        print("count_text_size.py: error: provide at least one path, '-', or --glob pattern", file=sys.stderr)
        return 1

    rows: list[dict[str, Any]] = []
    stdin_consumed = False
    for raw in inputs:
        if raw == "-":
            if stdin_consumed:
                rows.append(
                    {
                        "file": "-",
                        "chars": 0,
                        "words": 0,
                        "lines": 0,
                        "is_markdown": args.by_heading,
                        "status": "error",
                        "error": "stdin already consumed; use '-' only once.",
                        "sections": [],
                    }
                )
                continue
            rows.append(_analyze_stdin(args.by_heading))
            stdin_consumed = True
            continue
        rows.append(_analyze_path(Path(raw), args.encoding, args.by_heading))

    has_error = any(row["status"] == "error" for row in rows)

    payload: str
    totals = _totals(rows)
    if args.format == "json":
        json_rows: list[dict[str, Any]] = []
        for row in rows:
            item = {
                "file": row["file"],
                "chars": row["chars"],
                "words": row["words"],
                "lines": row["lines"],
                "is_markdown": row["is_markdown"],
                "status": row["status"],
                "error": row["error"],
            }
            if args.by_heading and row["sections"]:
                item["sections"] = row["sections"]
            json_rows.append(item)
        payload = json.dumps({"version": SCRIPT_VERSION, "totals": totals, "files": json_rows}, indent=2)
    else:
        payload = _to_table(rows, args.by_heading)

    if args.out:
        out_path = Path(args.out).resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(payload + ("\n" if not payload.endswith("\n") else ""), encoding="utf-8")
    else:
        print(payload)

    return 1 if (has_error and args.fail_on_error) else 0


if __name__ == "__main__":
    sys.exit(main())
