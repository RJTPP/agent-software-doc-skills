#!/usr/bin/env python3
"""Manual structure checker for software-design-doc canonical SDD outputs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
from typing import Any

INDEX_FILE = "index.md"

BASE_FILE_ORDER = [
    INDEX_FILE,
    "01-introduction.md",
    "02-03-system-context-and-concerns.md",
    "04-architecture-overview.md",
    "05-viewpoints-and-views.md",
    "06-design-elements-and-constraints.md",
    "07-08-traceability-and-rationale.md",
    "09-10-risks-and-summary.md",
]

DEEP_FILE_ORDER = [
    "11-data-design.md",
    "12-component-design.md",
    "13-human-interface-design.md",
    "14-requirements-traceability-matrix.md",
    "15-appendices.md",
    "16-design-decisions-locked.md",
]

FILE_HEADINGS: dict[str, list[str]] = {
    INDEX_FILE: [
        "# Software Design Description",
        "## Document Control",
        "## Document Map",
    ],
    "01-introduction.md": [
        "## 1. Introduction",
        "### 1.1 Purpose",
        "### 1.2 Scope",
        "### 1.3 Context",
        "### 1.4 Intended Audience",
        "### 1.5 References",
        "### 1.6 Glossary",
    ],
    "02-03-system-context-and-concerns.md": [
        "## 2. System Overview",
        "### 2.1 Product and Runtime Context",
        "### 2.2 External Systems and Integrations",
        "### 2.3 Operating Constraints",
        "## 3. Stakeholders and Design Concerns",
        "### 3.1 Stakeholder List",
        "### 3.2 Concern Catalog",
        "### 3.3 Non-Functional Targets (Recommended)",
    ],
    "04-architecture-overview.md": [
        "## 4. Architecture Overview",
        "### 4.1 Logical Architecture",
        "### 4.2 Deployment and Runtime Topology",
        "### 4.3 Critical Flow Summary",
    ],
    "05-viewpoints-and-views.md": [
        "## 5. Viewpoints and Views",
        "### 5.1 Viewpoint-to-View Mapping",
        "### 5.2 Context View",
        "### 5.3 Composition View",
        "### 5.4 Logical View",
        "### 5.5 Dependency View",
        "### 5.6 Information View",
        "### 5.7 Interface View",
        "### 5.8 Interaction / State / Algorithm Views (as applicable)",
        "### 5.9 Resource View (as applicable)",
    ],
    "06-design-elements-and-constraints.md": [
        "## 6. Design Elements and Constraints",
        "### 6.1 Design Element Catalog (Formal Definitions)",
        "### 6.2 Interfaces and Data Structures",
        "### 6.3 Relationships",
        "### 6.4 Constraints and Assumptions",
        "### 6.5 Runtime State and Data Notes (Recommended)",
    ],
    "07-08-traceability-and-rationale.md": [
        "## 7. Traceability",
        "### 7.1 Requirement/Concern to Design Mapping",
        "### 7.2 Coverage and Gaps",
        "## 8. Design Rationale",
        "### 8.1 Key Decisions",
        "### 8.2 Alternatives Considered",
        "### 8.3 Tradeoff Analysis",
    ],
    "09-10-risks-and-summary.md": [
        "## 9. Risks and Mitigations",
        "## 10. Summary",
    ],
    "11-data-design.md": [
        "## 11. Data Design",
        "### 11.1 ERD Summary",
        "### 11.2 Data Description",
        "### 11.3 Data Dictionary",
        "### 11.4 Client-side Cache/Storage Model",
    ],
    "12-component-design.md": [
        "## 12. Component Design",
        "### 12.1 Subsystem Responsibilities",
        "### 12.2 Internal Interfaces",
        "### 12.3 Public/Private API Surface",
        "### 12.4 Failure Handling and Retries",
    ],
    "13-human-interface-design.md": [
        "## 13. Human Interface Design",
        "### 13.1 UX Flow Summary",
        "### 13.2 Key Screens/Wireframes",
        "### 13.3 Interaction Constraints",
    ],
    "14-requirements-traceability-matrix.md": [
        "## 14. Requirements Traceability Matrix",
        "### 14.1 Requirement to Design Mapping Table",
        "### 14.2 Coverage Status and Open Items",
    ],
    "15-appendices.md": [
        "## 15. Appendices",
        "### 15.1 Sequence Flows",
        "### 15.2 State Models",
        "### 15.3 Configuration Matrix",
        "### 15.4 Cache Policy",
        "### 15.5 Security and Privacy Notes",
        "### 15.6 Testing Strategy",
        "### 15.7 Risk Register",
    ],
    "16-design-decisions-locked.md": [
        "## 16. Design Decisions (Locked)",
        "### 16.1 Architectural Decisions and Rationale",
        "### 16.2 Deferred Decisions",
    ],
}

CORE3_REQUIRED_HEADINGS: dict[str, list[str]] = {
    "04-architecture-overview.md": ["## 4. Architecture Overview"],
    "05-viewpoints-and-views.md": ["### 5.1 Viewpoint-to-View Mapping"],
    "06-design-elements-and-constraints.md": ["### 6.1 Design Element Catalog (Formal Definitions)"],
}

INDEX_REQUIRED_LINKS = BASE_FILE_ORDER[1:]
DEEP_REQUIRED_LINKS = DEEP_FILE_ORDER

INTERFACE_FIELD_PATTERNS = [
    ("component", r"(?i)\bComponent\s*:"),
    ("responsibility", r"(?i)\bResponsibility\s*:"),
    ("inputs", r"(?i)\bInputs\s*:"),
    ("outputs", r"(?i)\bOutputs\s*:"),
    ("dependencies", r"(?i)\bDependencies\s*:"),
    ("public-functions", r"(?i)\bPublic Functions?\s*:"),
]

QUALITY_SCENARIO_FIELD_PATTERNS = [
    ("stimulus", r"(?i)\bStimulus\s*:"),
    ("environment", r"(?i)\bEnvironment\s*:"),
    ("response", r"(?i)\bResponse\s*:"),
    ("measurement", r"(?i)\bMeasurement\s*:"),
]


def _parse_heading(heading: str) -> tuple[int, str]:
    match = re.match(r"^(#{1,6})\s+(.+?)\s*$", heading.strip())
    if not match:
        raise ValueError(f"Invalid heading pattern: {heading!r}")
    return len(match.group(1)), _normalize_heading_text(match.group(2))


def _normalize_heading_text(text: str) -> str:
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


def _read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return None


def _run_heading_checks(
    checks: list[dict[str, Any]],
    check_prefix: str,
    file_path: Path,
    required_headings: list[str],
    enforce_order: bool = False,
    severity: str = "soft",
) -> None:
    text = _read_text(file_path)
    if text is None:
        _add_check(
            checks,
            f"{check_prefix}-readable",
            False,
            "hard",
            f"Could not read {file_path}",
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
            severity,
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
            severity,
            f"{file_path} required headings appear in expected order -> {in_order}",
        )


def _run_pattern_checks(
    checks: list[dict[str, Any]],
    check_prefix: str,
    file_path: Path,
    patterns: list[tuple[str, str]],
    severity: str = "soft",
) -> None:
    text = _read_text(file_path)
    if text is None:
        _add_check(
            checks,
            f"{check_prefix}-readable",
            False,
            "hard",
            f"Could not read {file_path}",
        )
        return

    for label, pattern in patterns:
        present = re.search(pattern, text) is not None
        _add_check(
            checks,
            f"{check_prefix}-pattern-{label}",
            present,
            severity,
            f"{file_path} contains pattern {pattern!r} -> {present}",
        )


def _run_index_link_checks(
    checks: list[dict[str, Any]],
    index_path: Path,
    required_links: list[str],
    severity: str = "soft",
) -> None:
    text = _read_text(index_path)
    if text is None:
        _add_check(
            checks,
            "index-readable",
            False,
            "hard",
            f"Could not read {index_path}",
        )
        return

    for filename in required_links:
        escaped = re.escape(filename)
        linked = re.search(rf"\[[^\]]+\]\({escaped}\)", text) is not None
        _add_check(
            checks,
            f"index-link-{filename}",
            linked,
            severity,
            f"{index_path} links to {filename} -> {linked}",
        )


def _required_files_for_profile(profile: str) -> list[str]:
    files = list(BASE_FILE_ORDER)
    if profile == "implementation-deep":
        files.extend(DEEP_FILE_ORDER)
    return files


def run_checks(
    mode: str,
    docs_dir: Path,
    profile: str = "ieee-pragmatic",
    require_all_subsections: bool = False,
    strict_review_input: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

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
            "profile": profile,
            "docs_dir": str(docs_dir),
            "checks": checks,
        }

    required_sdd_files = _required_files_for_profile(profile)
    index_path = docs_dir / INDEX_FILE

    for filename in required_sdd_files:
        file_path = docs_dir / filename
        severity = "hard" if mode not in {"review-only", "drift-check"} else "input"
        _add_check(
            checks,
            f"file-{filename}-exists",
            file_path.exists(),
            severity,
            f"{file_path} exists -> {file_path.exists()}",
        )

    if index_path.exists():
        index_severity = "soft" if mode not in {"review-only", "drift-check"} else "input"
        _run_heading_checks(
            checks,
            "index",
            index_path,
            FILE_HEADINGS[INDEX_FILE],
            enforce_order=True,
            severity=index_severity,
        )
        index_required_links = list(INDEX_REQUIRED_LINKS)
        if profile == "implementation-deep":
            index_required_links.extend(DEEP_REQUIRED_LINKS)
        _run_index_link_checks(checks, index_path, index_required_links, severity=index_severity)

    for filename in required_sdd_files:
        if filename == INDEX_FILE:
            continue
        file_path = docs_dir / filename
        if not file_path.exists():
            continue
        _run_heading_checks(
            checks,
            filename.replace(".md", ""),
            file_path,
            FILE_HEADINGS[filename],
            enforce_order=require_all_subsections,
            severity="soft" if mode not in {"review-only", "drift-check"} else "input",
        )

    for filename, headings in CORE3_REQUIRED_HEADINGS.items():
        file_path = docs_dir / filename
        if file_path.exists() and mode not in {"review-only", "drift-check"}:
            _run_heading_checks(checks, f"core3-{filename}", file_path, headings)

    design_elements_path = docs_dir / "06-design-elements-and-constraints.md"
    concerns_path = docs_dir / "02-03-system-context-and-concerns.md"
    if design_elements_path.exists() and mode not in {"review-only", "drift-check"} and require_all_subsections:
        _run_pattern_checks(checks, "sdd-interface-fields", design_elements_path, INTERFACE_FIELD_PATTERNS)
    if concerns_path.exists() and mode not in {"review-only", "drift-check"} and require_all_subsections:
        _run_pattern_checks(checks, "sdd-quality-scenario", concerns_path, QUALITY_SCENARIO_FIELD_PATTERNS)

    return {
        "mode": mode,
        "profile": profile,
        "docs_dir": str(docs_dir),
        "strict_review_input": strict_review_input,
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Check software-design-doc canonical SDD structure.")
    parser.add_argument(
        "--mode",
        choices=["draft+review", "draft-only", "review-only", "drift-check"],
        required=True,
        help="Expected output mode.",
    )
    parser.add_argument(
        "--docs-dir",
        default="docs/sdd",
        help="Directory containing the canonical SDD document set.",
    )
    parser.add_argument(
        "--profile",
        choices=["ieee-pragmatic", "implementation-deep"],
        default="ieee-pragmatic",
        help="File and heading validation profile for SDD structure checks.",
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
        "--require-all-subsections",
        action="store_true",
        help="Require all template subsections and per-file heading order checks.",
    )
    parser.add_argument(
        "--strict-review-input",
        action="store_true",
        help="In review-only or drift-check mode, fail overall validation when reviewed input files, links, or headings are missing.",
    )
    args = parser.parse_args()

    result = run_checks(
        args.mode,
        Path(args.docs_dir).resolve(),
        profile=args.profile,
        require_all_subsections=args.require_all_subsections,
        strict_review_input=args.strict_review_input,
    )
    checks = result["checks"]
    hard_fail_count = sum(1 for c in checks if c["severity"] == "hard" and not c["passed"])
    soft_fail_count = sum(1 for c in checks if c["severity"] == "soft" and not c["passed"])
    input_fail_count = sum(1 for c in checks if c["severity"] == "input" and not c["passed"])
    strict_sections = not args.allow_soft_sections
    strict_review = args.mode in {"review-only", "drift-check"} and args.strict_review_input
    passed = (
        hard_fail_count == 0
        and (soft_fail_count == 0 or not strict_sections)
        and (input_fail_count == 0 or not strict_review)
    )
    result["hard_fail_count"] = hard_fail_count
    result["soft_fail_count"] = soft_fail_count
    result["strict_sections"] = strict_sections
    result["allow_soft_sections"] = args.allow_soft_sections
    result["require_all_subsections"] = args.require_all_subsections
    result["strict_review_input"] = args.strict_review_input
    result["input_fail_count"] = input_fail_count
    result["passed"] = passed

    for check in checks:
        status = "PASS" if check["passed"] else "FAIL"
        print(f"[{status}] ({check['severity']}) {check['id']}: {check['evidence']}")
    print(
        f"Summary: profile={args.profile} checks={len(checks)} hard_fail={hard_fail_count} soft_fail={soft_fail_count} "
        f"input_fail={input_fail_count} strict_sections={strict_sections} strict_review_input={strict_review} "
        f"overall={'PASS' if passed else 'FAIL'}"
    )

    if args.out:
        out_path = Path(args.out).resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
        print(f"Wrote JSON report to {out_path}")

    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
