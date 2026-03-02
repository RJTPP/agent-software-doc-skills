---
name: software-design-doc
description: Draft, review, and update Software Design Documents using an IEEE 1016-2009-inspired structure with pragmatic completeness checks and output structure validation. Use this whenever a user asks to write an SDD, assess SDD quality/completeness, align design docs to IEEE 1016 concepts, map PRD requirements to design, produce architecture/interface/data design sections, generate a gap report with remediation actions, perform SDD review-only gap analysis, or update an SDD after architecture changes.
license: MIT
metadata:
  author: RJTPP
  version: 0.1.0
---

# Software Design Doc

Create or review an SDD using a structure inspired by IEEE 1016-2009 concepts while staying pragmatic for the project context.

## Resources

- Use [references/sdd-completeness-checklist.md](references/sdd-completeness-checklist.md) for completeness gates and required content coverage.
- Use [references/sdd-template.md](references/sdd-template.md) as the default SDD structure.
- Use [references/sdd-template-implementation-deep.md](references/sdd-template-implementation-deep.md) when detail profile is `implementation-deep`.
- Use [references/viewpoint-mapping.md](references/viewpoint-mapping.md) to choose and justify design viewpoints.
- Use [references/copyright-safety.md](references/copyright-safety.md) for mandatory copyright guardrails.
- Use [scripts/check_sdd_structure.py](scripts/check_sdd_structure.py) to validate mode/file contract and required headings in generated outputs.

Mandatory preflight sequence:

1. Read necessary available context first (PRD/SDD/repo docs relevant to request).
2. Recommend mode, detail profile, and interaction option based on that context.
3. Ask for user confirmation before drafting.

Do not start drafting until preflight confirmation is received, unless user explicitly uses `/fast` or `/assume`.

## Copyright and Standards Safety (Mandatory)

- Treat IEEE 1016-2009 as a conceptual reference only.
- Treat this skill as unofficial and not IEEE-endorsed.
- Use original wording in all generated outputs.
- Do not reproduce or closely paraphrase any copyrighted standard text, tables, or figures.
- Do not provide clause text on request; provide section alignment guidance and ask the user to consult their licensed standard copy for normative wording.
- When referring to IEEE structure, cite section identifiers only (for example "Clause 4"), not normative text.

## Defaults

- Mode: `draft+review`.
- Completeness strictness: `pragmatic`.
- Detail profile: `ieee-pragmatic`.
- Codebase inspection: enabled if repository context is available.
- Output files:
  - `docs/SDD.md`
  - `docs/SDD-gap-report.md`

If the user specifies a different mode, follow the user preference.
If the user specifies a different output path, only accept a safe relative path within the project folder (see output path safety rules below).

Mode shortcuts accepted in user prompts:

- `/de` or `/draft+review` -> `draft+review`
- `/d` or `/draft-only` -> `draft-only`
- `/r` or `/review-only` -> `review-only`

Mode resolution precedence:

1. Explicit shortcut token in the prompt (`/de`, `/d`, `/r`, or long form)
2. Clear natural-language intent (for example "review only")
3. Default to `draft+review`

Interaction options:

- `/ask` (default behavior): confirm scope/mode/inputs before drafting and request missing critical info.
- `/fast`: proceed immediately with reasonable assumptions, then list assumptions in the output.
- `/assume`: proceed with assumptions even if inputs are incomplete, and clearly mark assumption-based sections.

Detail profile options:

- `ieee-pragmatic` (default): IEEE 1016 core structure + concise implementation guidance.
- `implementation-deep`: Keep all core template sections and add deeper implementation appendices.

If user asks for "detailed", "implementation handoff", "architecture deep dive", "ERD/data dictionary", or "full design package", use `implementation-deep`.

## Output Path Safety (Mandatory)

- Only write outputs within the repository root (project folder).
- Allow custom subpaths when they remain inside the repository (for example `docs/reviews/v2/SDD.md`).
- Reject absolute paths and any path containing parent traversal (`..`).
- Never write to sensitive paths (for example `.git/`, `.github/workflows/`, `/etc/`, home directories).
- Never build shell commands by interpolating user-provided paths.

## Input Contract

Expect at least one of:

- project requirements/PRD context, or
- an existing SDD to review/update.

If neither is available, stop and ask for missing inputs before drafting.
Do not invent project-specific architecture details.

Useful optional inputs:

- architecture constraints,
- technology stack constraints,
- required viewpoints,
- completeness strictness override,
- explicit output path inside the project folder.

Before drafting, perform an intake check:

1. Confirm mode, detail profile, and output path inside the project folder.
2. Confirm whether repository inspection should be used.
3. Identify missing critical inputs (PRD context, existing SDD, key constraints).

If critical inputs are missing, ask concise clarification questions first.
Only skip clarification when user explicitly uses `/fast` or `/assume`.

## Modes

### `draft+review` (default)

1. Draft or update `docs/SDD.md`.
2. Run completeness/gap analysis.
3. Write both SDD and gap report files.

### `draft-only`

1. Draft or update `docs/SDD.md`.
2. Skip gap report unless requested.

### `review-only`

1. Do not rewrite source SDD unless user asks.
2. Produce `docs/SDD-gap-report.md` with concrete remediation actions.

## Required Workflow

1. Discover context

- Inspect repository docs and key code structure by default.
- Identify available artifacts: PRD, existing SDD, architecture notes, APIs, schemas.

2. Identify stakeholders and concerns

- Extract explicit and implied design stakeholders.
- Convert requirements/risks/NFRs into design concerns.

3. Select viewpoints

- Choose only viewpoints that address identified concerns.
- Mark omitted viewpoints as `Not Applicable` with justification.

4. Draft or update SDD

- Follow the default structure from `references/sdd-template.md`.
- Use original wording; do not quote or mirror copyrighted standards text.
- Include rationale for major decisions and viewpoint selection.
- Include traceability mapping from requirement concerns to design sections.
- Preserve core template sections in all profiles; never replace the base structure with custom-only sections.
- Use Mermaid diagrams for architecture/flow/state representations when they improve clarity.
- If detail profile is `implementation-deep`, add the following sections as extensions:
  - `## System Overview` (deployment topology and runtime boundaries)
  - `## Data Design` (ERD summary, data dictionary, client-side cache/storage model)
  - `## Component Design` (subsystems, responsibilities, key interfaces/routes)
  - `## Human Interface Design` (screen/wireframe references where available)
  - `## Requirements Traceability Matrix`
  - `## Appendices` (sequence/state/config/cache/security/testing/risk)
  - `## Design Decisions (Locked)`
  - Include at least two Mermaid diagrams:
    - one system context/component diagram
    - one sequence or state diagram for a key operational flow

5. Run pragmatic completeness pass

- Check core SDD content coverage mapped to IEEE 1016-2009 Clause 4 themes (without reproducing standard text).
- Check concern-to-view coverage and missing decisions.
- Allow justified simplification for project scale.
- In `implementation-deep`, also check extension consistency:
  - product/system name is consistent across title, document control, and body
  - version references are consistent with source artifacts
  - references to PRD/PDD/source files are accurate and non-conflicting

6. Write outputs

- Ensure parent directory exists.
- Resolve output paths safely inside the repository root only. Reject and ask for a safe path if the requested path is absolute, contains `..`, or targets a sensitive path.
- For `draft+review` or `draft-only`, write `docs/SDD.md` by default (or another safe in-repo path if requested).
- For `draft+review` or `review-only`, write `docs/SDD-gap-report.md` by default (or another safe in-repo path if requested).
- In `review-only`, do not modify the source SDD unless explicitly requested.

7. Validate generated outputs

- Run `python3 scripts/check_sdd_structure.py --mode <draft+review|draft-only|review-only> --docs-dir <output-dir> --profile <ieee-pragmatic|implementation-deep>`.
- Section completeness is strict by default; use `--allow-soft-sections` only when section checks should be advisory.
- In `review-only`, use `--allow-input-sdd` if source SDD is colocated with generated gap report.
- Treat checker hard-fail results as blockers and revise outputs before finalizing.

## Gap Report Format

Use these headings in order:

1. `# SDD Gap Report`
2. `## Scope and Inputs`
3. `## Missing Required Content`
4. `## Weak or Implicit Rationale`
5. `## Traceability Gaps`
6. `## Recommended Fixes (Priority Ordered)`
7. `## Coverage Summary`

## Pragmatic Completeness Rules

- Treat mapped core content areas as required unless genuinely out of scope.
- If an item is omitted, provide a short `N/A rationale`.
- Favor correctness and implementability over ceremonial detail.
- Keep terminology consistent with the project domain.
- If the user asks for exact IEEE wording, decline and provide a non-verbatim summary instead.

## Output Quality Bar

- SDD sections are complete enough for implementation handoff.
- Viewpoint choices are explicit and concern-driven.
- Gap report recommendations are actionable and prioritized.
- No machine-specific assumptions or absolute local-only dependencies in the document content.
- Core template sections remain intact even when adding deep implementation sections.
- Names/versions/references are consistent across all sections.

## Example Requests That Should Trigger This Skill

- "Write an SDD with an IEEE 1016-inspired structure from this PRD and repo structure."
- "Review this SDD and list standards gaps with fixes."
- "Update our SDD after moving from monolith to microservices."
- "Map PRD requirements to design sections and identify missing architecture details."
