#!/usr/bin/env python3
# Copy Reference: check_doc_artifacts.py
# Version: 0.1.0
# Synced-On: 2026-04-10
# NOTE: This file is intentionally duplicated in:
# - scripts/check_doc_artifacts.py
# - skills/software-design-doc/scripts/check_doc_artifacts.py
"""Validate dated documentation artifact history directories."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
from typing import Any

SCRIPT_VERSION = "0.1.0"
DATE_FILE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}\.md$")


def _add_check(
    checks: list[dict[str, Any]],
    check_id: str,
    passed: bool,
    severity: str,
    evidence: str,
) -> None:
    checks.append(
        {
            "id": check_id,
            "passed": passed,
            "severity": severity,
            "evidence": evidence,
        }
    )


def run_checks(
    artifact_root: Path,
    doc_kind: str,
    artifact_kind: str,
    min_count: int = 1,
) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    root_exists = artifact_root.exists() and artifact_root.is_dir()
    _add_check(
        checks,
        "artifact-root-exists",
        root_exists,
        "hard",
        f"{artifact_root} exists and is directory -> {root_exists}",
    )
    if not root_exists:
        return {
            "artifact_root": str(artifact_root),
            "doc_kind": doc_kind,
            "artifact_kind": artifact_kind,
            "checks": checks,
        }

    target_dir = artifact_root / doc_kind / artifact_kind
    target_exists = target_dir.exists() and target_dir.is_dir()
    _add_check(
        checks,
        "artifact-dir-exists",
        target_exists,
        "hard",
        f"{target_dir} exists and is directory -> {target_exists}",
    )
    if not target_exists:
        return {
            "artifact_root": str(artifact_root),
            "doc_kind": doc_kind,
            "artifact_kind": artifact_kind,
            "checks": checks,
        }

    markdown_files = sorted(path for path in target_dir.iterdir() if path.is_file() and path.suffix.lower() == ".md")
    dated_files = [path for path in markdown_files if DATE_FILE_RE.match(path.name)]

    _add_check(
        checks,
        "artifact-count-minimum",
        len(dated_files) >= min_count,
        "hard",
        f"{target_dir} has {len(dated_files)} dated markdown artifact(s); required >= {min_count}",
    )
    _add_check(
        checks,
        "artifact-filenames-dated",
        len(markdown_files) == len(dated_files),
        "hard",
        f"{target_dir} markdown files all use YYYY-MM-DD.md naming -> {len(markdown_files) == len(dated_files)}",
    )

    latest_artifact = dated_files[-1] if dated_files else None
    if latest_artifact is not None:
        readable = True
        try:
            latest_artifact.read_text(encoding="utf-8")
        except OSError:
            readable = False
        _add_check(
            checks,
            "latest-artifact-readable",
            readable,
            "hard",
            f"{latest_artifact} readable -> {readable}",
        )

    return {
        "artifact_root": str(artifact_root),
        "doc_kind": doc_kind,
        "artifact_kind": artifact_kind,
        "target_dir": str(target_dir),
        "latest_artifact": str(latest_artifact) if latest_artifact is not None else None,
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Check dated documentation artifact history directories.")
    parser.add_argument(
        "--artifact-root",
        default=".agent-doc-skills",
        help="Root directory containing artifact history by document kind.",
    )
    parser.add_argument(
        "--doc-kind",
        required=True,
        help="Document kind under the artifact root, for example 'sdd' or 'prd'.",
    )
    parser.add_argument(
        "--artifact-kind",
        choices=["gaps", "drift"],
        required=True,
        help="Artifact history kind to validate.",
    )
    parser.add_argument(
        "--min-count",
        type=int,
        default=1,
        help="Minimum number of dated markdown artifacts required.",
    )
    parser.add_argument(
        "--out",
        default=None,
        help="Optional path to write JSON report.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {SCRIPT_VERSION}",
    )
    args = parser.parse_args()

    result = run_checks(
        artifact_root=Path(args.artifact_root).resolve(),
        doc_kind=args.doc_kind,
        artifact_kind=args.artifact_kind,
        min_count=args.min_count,
    )
    checks = result["checks"]
    hard_fail_count = sum(1 for check in checks if check["severity"] == "hard" and not check["passed"])
    passed = hard_fail_count == 0
    result["hard_fail_count"] = hard_fail_count
    result["passed"] = passed

    for check in checks:
        status = "PASS" if check["passed"] else "FAIL"
        print(f"[{status}] ({check['severity']}) {check['id']}: {check['evidence']}")
    print(
        "Summary: "
        f"doc_kind={args.doc_kind} artifact_kind={args.artifact_kind} checks={len(checks)} "
        f"hard_fail={hard_fail_count} overall={'PASS' if passed else 'FAIL'}"
    )

    if args.out:
        out_path = Path(args.out).resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
        print(f"Wrote JSON report to {out_path}")

    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
