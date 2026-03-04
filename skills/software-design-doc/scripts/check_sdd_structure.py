#!/usr/bin/env python3
"""Manual structure checker for software-design-doc outputs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
from typing import Any


SDD_REQUIRED_HEADINGS = [
    "## Document Control",
    "## 1. Introduction",
    "## 2. System Overview",
    "## 3. Stakeholders and Design Concerns",
    "## 4. Architecture Overview",
    "## 5. Viewpoints and Views",
    "## 6. Design Elements and Constraints",
    "## 7. Traceability",
    "## 8. Design Rationale",
    "## 9. Risks and Mitigations",
    "## 10. Summary",
]

CORE3_REQUIRED_HEADINGS = [
    "### 5.1 Viewpoint-to-View Mapping",
    "### 6.1 Design Element Catalog (Formal Definitions)",
]

BASE_SUBSECTION_REQUIRED_HEADINGS = [
    "### 1.1 Purpose",
    "### 1.2 Scope",
    "### 1.3 Context",
    "### 1.4 Intended Audience",
    "### 1.5 References",
    "### 1.6 Glossary",
    "### 2.1 Product and Runtime Context",
    "### 2.2 External Systems and Integrations",
    "### 2.3 Operating Constraints",
    "### 3.1 Stakeholder List",
    "### 3.2 Concern Catalog",
    "### 3.3 Non-Functional Targets (Recommended)",
    "### 4.1 Logical Architecture",
    "### 4.2 Deployment and Runtime Topology",
    "### 4.3 Critical Flow Summary",
    "### 5.1 Viewpoint-to-View Mapping",
    "### 5.2 Context View",
    "### 5.3 Composition View",
    "### 5.4 Logical View",
    "### 5.5 Dependency View",
    "### 5.6 Information View",
    "### 5.7 Interface View",
    "### 5.8 Interaction / State / Algorithm Views (as applicable)",
    "### 5.9 Resource View (as applicable)",
    "### 6.1 Design Element Catalog (Formal Definitions)",
    "### 6.2 Interfaces and Data Structures",
    "### 6.3 Relationships",
    "### 6.4 Constraints and Assumptions",
    "### 6.5 Runtime State and Data Notes (Recommended)",
    "### 7.1 Requirement/Concern to Design Mapping",
    "### 7.2 Coverage and Gaps",
    "### 8.1 Key Decisions",
    "### 8.2 Alternatives Considered",
    "### 8.3 Tradeoff Analysis",
]

DEEP_EXTENSION_REQUIRED_HEADINGS = [
    "## 11. Data Design",
    "## 12. Component Design",
    "## 13. Human Interface Design",
    "## 14. Requirements Traceability Matrix",
    "## 15. Appendices",
    "## 16. Design Decisions (Locked)",
]

DEEP_SUBSECTION_REQUIRED_HEADINGS = [
    "### 11.1 ERD Summary",
    "### 11.2 Data Description",
    "### 11.3 Data Dictionary",
    "### 11.4 Client-side Cache/Storage Model",
    "### 12.1 Subsystem Responsibilities",
    "### 12.2 Internal Interfaces",
    "### 12.3 Public/Private API Surface",
    "### 12.4 Failure Handling and Retries",
    "### 13.1 UX Flow Summary",
    "### 13.2 Key Screens/Wireframes",
    "### 13.3 Interaction Constraints",
    "### 14.1 Requirement to Design Mapping Table",
    "### 14.2 Coverage Status and Open Items",
    "### 15.1 Sequence Flows",
    "### 15.2 State Models",
    "### 15.3 Configuration Matrix",
    "### 15.4 Cache Policy",
    "### 15.5 Security and Privacy Notes",
    "### 15.6 Testing Strategy",
    "### 15.7 Risk Register",
    "### 16.1 Architectural Decisions and Rationale",
    "### 16.2 Deferred Decisions",
]

INTERFACE_FIELD_PATTERNS = [
    r"(?i)\bComponent\s*:",
    r"(?i)\bResponsibility\s*:",
    r"(?i)\bInputs\s*:",
    r"(?i)\bOutputs\s*:",
    r"(?i)\bDependencies\s*:",
    r"(?i)\bPublic Functions?\s*:",
]

QUALITY_SCENARIO_FIELD_PATTERNS = [
    r"(?i)\bStimulus\s*:",
    r"(?i)\bEnvironment\s*:",
    r"(?i)\bResponse\s*:",
    r"(?i)\bMeasurement\s*:",
]

GAP_REQUIRED_HEADINGS = [
    "# SDD Gap Report",
    "## Scope and Inputs",
    "## Missing Required Content",
    "## Weak or Implicit Rationale",
    "## Traceability Gaps",
    "## Recommended Fixes (Priority Ordered)",
    "## Coverage Summary",
]


def _parse_heading(heading: str) -> tuple[int, str]:
    match = re.match(r"^(#{1,6})\s+(.+?)\s*$", heading.strip())
    if not match:
        raise ValueError(f"Invalid heading pattern: {heading!r}")
    return len(match.group(1)), _normalize_heading_text(match.group(2))


def _normalize_heading_text(text: str) -> str:
    """Normalize heading text for matching.

    Supports markdown ATX closing hashes such as: ## Title ##
    """
    normalized = text.strip()
    normalized = re.sub(r"\s+#+\s*$", "", normalized)
    return normalized.strip().lower()


def _extract_heading_sequence(markdown_text: str) -> list[tuple[int, str]]:
    found: list[tuple[int, str]] = []
    in_fence = False
    fence_char = ""
    fence_len = 0
    for line in markdown_text.splitlines():
        stripped = line.lstrip()

        fence_match = re.match(r"^(```+|~~~+)", stripped)
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

        match = re.match(r"^(#{1,6})\s+(.+?)\s*$", stripped)
        if not match:
            continue
        level = len(match.group(1))
        text = _normalize_heading_text(match.group(2))
        found.append((level, text))
    return found


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


def _run_heading_checks(
    checks: list[dict[str, Any]],
    check_prefix: str,
    file_path: Path,
    required_headings: list[str],
    enforce_order: bool = False,
) -> None:
    try:
        text = file_path.read_text(encoding="utf-8")
    except OSError as exc:
        _add_check(
            checks,
            f"{check_prefix}-readable",
            False,
            "hard",
            f"Could not read {file_path}: {exc}",
        )
        return

    found_sequence = _extract_heading_sequence(text)
    found_set = set(found_sequence)
    for heading in required_headings:
        level, normalized_text = _parse_heading(heading)
        present = (level, normalized_text) in found_set
        _add_check(
            checks,
            f"{check_prefix}-heading-{normalized_text.replace(' ', '-')}",
            present,
            "soft",
            f"{file_path} contains heading {heading!r} -> {present}",
        )

    if enforce_order:
        required_sequence = [_parse_heading(heading) for heading in required_headings]
        found_iter = iter(found_sequence)
        in_order = all(
            any(found_heading == required_heading for found_heading in found_iter)
            for required_heading in required_sequence
        )

        _add_check(
            checks,
            f"{check_prefix}-heading-order",
            in_order,
            "soft",
            f"{file_path} required headings appear in expected order -> {in_order}",
        )


def _run_pattern_checks(
    checks: list[dict[str, Any]],
    check_prefix: str,
    file_path: Path,
    patterns: list[str],
) -> None:
    try:
        text = file_path.read_text(encoding="utf-8")
    except OSError as exc:
        _add_check(
            checks,
            f"{check_prefix}-readable",
            False,
            "hard",
            f"Could not read {file_path}: {exc}",
        )
        return

    for pattern in patterns:
        present = re.search(pattern, text) is not None
        label = re.sub(r"[^a-z0-9]+", "-", pattern.lower()).strip("-")
        _add_check(
            checks,
            f"{check_prefix}-pattern-{label}",
            present,
            "soft",
            f"{file_path} contains pattern {pattern!r} -> {present}",
        )


def run_checks(
    mode: str,
    docs_dir: Path,
    allow_input_sdd: bool = False,
    profile: str = "ieee-pragmatic",
    require_all_subsections: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    sdd_path = docs_dir / "SDD.md"
    gap_path = docs_dir / "SDD-gap-report.md"

    docs_exists = docs_dir.exists() and docs_dir.is_dir()
    _add_check(
        checks,
        "docs-dir-exists",
        docs_exists,
        "hard",
        f"{docs_dir} exists and is directory -> {docs_exists}",
    )
    if not docs_exists:
        return {
            "mode": mode,
            "docs_dir": str(docs_dir),
            "checks": checks,
        }

    sdd_exists = sdd_path.exists()
    gap_exists = gap_path.exists()

    if mode == "draft+review":
        _add_check(checks, "file-sdd-exists", sdd_exists, "hard", f"{sdd_path} exists -> {sdd_exists}")
        _add_check(checks, "file-gap-exists", gap_exists, "hard", f"{gap_path} exists -> {gap_exists}")
    elif mode == "draft-only":
        _add_check(checks, "file-sdd-exists", sdd_exists, "hard", f"{sdd_path} exists -> {sdd_exists}")
        _add_check(
            checks,
            "file-gap-optional",
            True,
            "soft",
            f"{gap_path} optional in draft-only mode (exists={gap_exists})",
        )
    elif mode == "review-only":
        _add_check(checks, "file-gap-exists", gap_exists, "hard", f"{gap_path} exists -> {gap_exists}")
        if allow_input_sdd:
            _add_check(
                checks,
                "file-sdd-allowed",
                True,
                "soft",
                f"{sdd_path} is allowed in review-only mode for colocated input (exists={sdd_exists})",
            )
        else:
            _add_check(checks, "file-sdd-absent", not sdd_exists, "hard", f"{sdd_path} absent -> {not sdd_exists}")

    if sdd_exists and mode != "review-only":
        _run_heading_checks(checks, "sdd", sdd_path, SDD_REQUIRED_HEADINGS)
        _run_heading_checks(checks, "sdd-core3", sdd_path, CORE3_REQUIRED_HEADINGS)
        if require_all_subsections:
            _run_heading_checks(checks, "sdd-subsections", sdd_path, BASE_SUBSECTION_REQUIRED_HEADINGS)
            _run_pattern_checks(checks, "sdd-interface-fields", sdd_path, INTERFACE_FIELD_PATTERNS)
            _run_pattern_checks(checks, "sdd-quality-scenario", sdd_path, QUALITY_SCENARIO_FIELD_PATTERNS)
        if profile == "implementation-deep":
            _run_heading_checks(checks, "sdd-deep", sdd_path, DEEP_EXTENSION_REQUIRED_HEADINGS)
            if require_all_subsections:
                _run_heading_checks(checks, "sdd-deep-subsections", sdd_path, DEEP_SUBSECTION_REQUIRED_HEADINGS)

    if gap_exists and mode != "draft-only":
        _run_heading_checks(checks, "gap", gap_path, GAP_REQUIRED_HEADINGS)

    return {
        "mode": mode,
        "profile": profile,
        "docs_dir": str(docs_dir),
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Check software-design-doc output structure.")
    parser.add_argument(
        "--mode",
        choices=["draft+review", "draft-only", "review-only"],
        required=True,
        help="Expected output mode.",
    )
    parser.add_argument(
        "--docs-dir",
        default="docs",
        help="Directory containing SDD.md and/or SDD-gap-report.md",
    )
    parser.add_argument(
        "--profile",
        choices=["ieee-pragmatic", "implementation-deep"],
        default="ieee-pragmatic",
        help="Heading validation profile for SDD structure checks.",
    )
    parser.add_argument(
        "--out",
        default=None,
        help="Optional path to write JSON report.",
    )
    parser.add_argument(
        "--allow-soft-sections",
        action="store_true",
        help="Do not fail overall result when only section checks fail.",
    )
    parser.add_argument(
        "--allow-input-sdd",
        action="store_true",
        help="In review-only mode, allow SDD.md to exist as colocated input.",
    )
    parser.add_argument(
        "--require-all-subsections",
        action="store_true",
        help="Require all template subsections (base; and deep subsections when profile is implementation-deep).",
    )
    args = parser.parse_args()

    result = run_checks(
        args.mode,
        Path(args.docs_dir).resolve(),
        allow_input_sdd=args.allow_input_sdd,
        profile=args.profile,
        require_all_subsections=args.require_all_subsections,
    )
    checks = result["checks"]
    hard_fail_count = sum(1 for c in checks if c["severity"] == "hard" and not c["passed"])
    soft_fail_count = sum(1 for c in checks if c["severity"] == "soft" and not c["passed"])
    strict_sections = not args.allow_soft_sections
    passed = hard_fail_count == 0 and (soft_fail_count == 0 or not strict_sections)
    result["hard_fail_count"] = hard_fail_count
    result["soft_fail_count"] = soft_fail_count
    result["strict_sections"] = strict_sections
    result["allow_soft_sections"] = args.allow_soft_sections
    result["allow_input_sdd"] = args.allow_input_sdd
    result["require_all_subsections"] = args.require_all_subsections
    result["passed"] = passed

    for check in checks:
        status = "PASS" if check["passed"] else "FAIL"
        print(f"[{status}] ({check['severity']}) {check['id']}: {check['evidence']}")
    print(
        f"Summary: profile={args.profile} checks={len(checks)} hard_fail={hard_fail_count} soft_fail={soft_fail_count} "
        f"strict_sections={strict_sections} overall={'PASS' if passed else 'FAIL'}"
    )

    if args.out:
        out_path = Path(args.out).resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
        print(f"Wrote JSON report to {out_path}")

    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
