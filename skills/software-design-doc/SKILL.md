---
name: software-design-doc
description: Draft, review, and update Software Design Descriptions using an IEEE 1016-2009-inspired structure with explicit architecture/views/elements formalization and output structure validation. Use this whenever a user asks to write an SDD, assess SDD quality/completeness, align design docs to IEEE 1016 concepts, map PRD requirements to design, produce architecture/interface/data design sections, generate a gap report with remediation actions, perform SDD review-only gap analysis, or update an SDD after architecture changes.
license: MIT
metadata:
  author: RJTPP
  version: 0.4.0-dev
---

# Software Design Description

Create or review an SDD using an IEEE 1016-inspired structure while staying pragmatic for project context.

## Resources

- Use [references/sdd-completeness-checklist.md](references/sdd-completeness-checklist.md) for completeness gates and required content coverage.
- Use the templates under [references/multi-file/](references/multi-file/) as the canonical SDD document-set structure.
- Use [references/viewpoint-mapping.md](references/viewpoint-mapping.md) to choose viewpoints and map them to concrete views.
- Use [references/copyright-safety.md](references/copyright-safety.md) for copyright/standards guardrails.
- Use [references/quality-attribute-scenarios.md](references/quality-attribute-scenarios.md) for quality-attribute scenario patterns.
- Use [scripts/check_sdd_structure.py](scripts/check_sdd_structure.py) to validate required files, headings, links, and core formalization sections across the generated document set.
- Use [scripts/count_text_size.py](scripts/count_text_size.py) to inspect file size quickly (`chars`, `words`, `lines`) and optional Markdown heading breakdown (`--by-heading`).

Mandatory preflight sequence:

1. Read available context first (PRD/SDD/repo docs relevant to the request).
2. Optionally run a size check for large doc sets: `python3 scripts/count_text_size.py --glob "<sdd-root>/**/*.md" --by-heading`.
3. Recommend mode, detail profile, and output root from that context.
4. Ask for user confirmation before drafting.

Do not start drafting until preflight confirmation is received, unless user explicitly uses `/fast` or `/assume`.

## Copyright and Standards Safety (Mandatory)

- Treat IEEE 1016-2009 as a conceptual reference only.
- Use original wording in all generated outputs.
- Do not reproduce or closely paraphrase any copyrighted standard text, tables, or figures.
- Do not provide clause text on request; provide section-alignment guidance and ask the user to consult their licensed standard copy for normative wording.
- When referring to IEEE structure, cite section identifiers only (for example `Clause 4`), not normative text.
- If a disclaimer is needed, include one concise line only (for example, `IEEE 1016-inspired internal guidance, unofficial.`).

## Defaults

- Mode: `draft+review`.
- Completeness strictness: `pragmatic`.
- Detail profile: `ieee-pragmatic`.
- Codebase inspection: enabled when repository context is available.
- Output root: `docs/sdd/`
- Output files:
  - `docs/sdd/index.md`
  - `docs/sdd/01-introduction.md`
  - `docs/sdd/02-system-overview.md`
  - `docs/sdd/03-stakeholders-and-concerns.md`
  - `docs/sdd/04-architecture-overview.md`
  - `docs/sdd/05-viewpoints-and-views.md`
  - `docs/sdd/06-design-elements-and-constraints.md`
  - `docs/sdd/07-traceability.md`
  - `docs/sdd/08-design-rationale.md`
  - `docs/sdd/09-risks-and-mitigations.md`
  - `docs/sdd/10-summary.md`
  - `docs/sdd/gap-report.md`

If the user specifies a different mode, follow the user preference.
If the user specifies a different output root, only accept a safe relative directory inside the project folder.

Mode shortcuts accepted in user prompts:

- `/de` or `/draft+review` -> `draft+review`
- `/d` or `/draft-only` -> `draft-only`
- `/r` or `/review-only` -> `review-only`

Mode resolution precedence:

1. Explicit shortcut token in the prompt (`/de`, `/d`, `/r`, or long form)
2. Clear natural-language intent (for example `review only`)
3. Default to `draft+review`

Interaction options:

- `/ask` (default): confirm scope/mode/inputs before drafting and request missing critical info.
- `/fast`: proceed immediately with reasonable assumptions, then list assumptions in the output.
- `/assume`: proceed with assumptions even if inputs are incomplete, and clearly mark assumption-based sections.

Detail profile options:

- `ieee-pragmatic` (default): strict base structure with concise implementation guidance.
- `implementation-deep`: keep all base sections and add deeper implementation files.

If user asks for `detailed`, `implementation handoff`, `architecture deep dive`, `ERD/data dictionary`, or `full design package`, use `implementation-deep`.

## Output Root Safety (Mandatory)

- Only write outputs within the repository root (project folder).
- Allow custom subdirectories when they remain inside the repository (for example `docs/reviews/v2/sdd/`).
- Reject absolute paths and any path containing parent traversal (`..`).
- Never write to sensitive paths (for example `.git/`, `.github/workflows/`, `/etc/`, home directories).
- Never build shell commands by interpolating user-provided paths.

## Input Contract

Expect at least one of:

- project requirements/PRD context, or
- an existing multi-file SDD root or `index.md` to review/update, or
- a legacy single-file SDD to convert into the canonical multi-file set.

If neither is available, stop and ask for missing inputs before drafting.
Do not invent project-specific architecture details.

Useful optional inputs:

- architecture constraints,
- technology stack constraints,
- required viewpoints,
- completeness strictness override,
- explicit output root inside the project folder.

Before drafting, perform an intake check:

1. Confirm mode, detail profile, and output root.
2. Confirm whether repository inspection should be used.
3. Identify missing critical inputs (PRD context, existing SDD input, key constraints).

If critical inputs are missing, ask concise clarification questions first.
Only skip clarification when user explicitly uses `/fast` or `/assume`.

## Modes

### `draft+review` (default)

1. Draft or update the canonical document set under `docs/sdd/`.
2. Run completeness/gap analysis.
3. Write both the SDD files and `gap-report.md`.

### `draft-only`

1. Draft or update the canonical document set under `docs/sdd/`.
2. Skip gap report unless requested.

### `review-only`

1. Accept an existing multi-file SDD root or `index.md` as input.
2. Do not rewrite source files unless user asks.
3. Produce `gap-report.md` with concrete remediation actions for the document set.

## Required Workflow

1. Discover context

- Inspect repository docs and key code structure by default.
- Identify available artifacts: PRD, existing multi-file SDD files, legacy single-file SDDs, architecture notes, APIs, schemas.

2. Identify stakeholders and concerns

- Extract explicit and implied design stakeholders.
- Convert requirements/risks/NFRs into design concerns.

3. Select viewpoints

- Choose only viewpoints that address identified concerns.
- Mark omitted viewpoints as `Not Applicable` with justification.

4. Draft or update the SDD document set

- Use `references/multi-file/` as the canonical template library.
- When the source is a legacy single-file SDD, redistribute its validated content into the canonical multi-file file set instead of preserving the old layout.
- `index.md` is the document entrypoint and must contain document control metadata plus links to every generated section file in canonical order.
- Use original wording; do not quote or mirror copyrighted standards text.
- Preserve required section ownership by file.
- Keep core architecture sections at the architectural abstraction level (layers/components/responsibilities), not file-by-file implementation listings.
- Put concrete file/module paths in implementation-oriented files or appendices when needed.
- Include Mermaid diagrams when they improve clarity.
- Always include the core-3 formal artifacts:
  - `## 4. Architecture Overview` in `04-architecture-overview.md`
  - `### 5.1 Viewpoint-to-View Mapping` in `05-viewpoints-and-views.md`
  - `### 6.1 Design Element Catalog (Formal Definitions)` in `06-design-elements-and-constraints.md` with fields: `Component`, `Responsibility`, `Inputs`, `Outputs`, `Dependencies`, `Public Functions`
- Optional enhancements:
  - Include quality-attribute scenarios using `Stimulus`, `Environment`, `Response`, `Measurement` when quality concerns are material.
  - Include a short future-evolution note in `06-design-elements-and-constraints.md` and/or `11-data-design.md` when persistent data is currently absent/static.
  - If optional enhancements are omitted, add a concise `N/A rationale`.
- If detail profile is `implementation-deep`, include extension files:
  - `11-data-design.md`
  - `12-component-design.md`
  - `13-human-interface-design.md`
  - `14-requirements-traceability-matrix.md`
  - `15-appendices.md`
  - `16-design-decisions-locked.md`

5. Run pragmatic completeness pass

- Check coverage against core IEEE-inspired structure themes without reproducing standard text.
- Check concern-to-view coverage and missing decisions.
- Ensure architecture/viewpoint/element formalization is explicit and reviewable across files.
- Check consistency of terminology, component names, version references, and cited artifacts across the document set.
- Check that `index.md` links to every generated section file.
- Allow justified simplification for project scale.

6. Write outputs

- Ensure parent directory exists.
- Resolve output root safely inside repository root only.
- For `draft+review` or `draft-only`, write the canonical section files under the output root.
- For `draft+review` or `review-only`, write `gap-report.md` under the output root.
- In `review-only`, do not modify source SDD files unless explicitly requested.

7. Validate generated outputs

- Run `python3 scripts/check_sdd_structure.py --mode <draft+review|draft-only|review-only> --docs-dir <output-root> --profile <ieee-pragmatic|implementation-deep>`.
- For evals/CI strictness, run with `--require-all-subsections`.
- Section completeness is strict by default; use `--allow-soft-sections` only when section checks should be advisory.
- In `review-only`, use `--allow-input-index` if source `index.md` and generated `gap-report.md` are colocated.
- In `review-only`, add `--strict-review-input` when CI/evals should fail on missing canonical input files, missing document-map links, or missing required headings in the reviewed SDD set.
- Treat checker hard-fail results as blockers and revise outputs before finalizing.

## Canonical Base File Set

Use these files as the default document sequence:

1. `index.md`
2. `01-introduction.md`
3. `02-system-overview.md`
4. `03-stakeholders-and-concerns.md`
5. `04-architecture-overview.md`
6. `05-viewpoints-and-views.md`
7. `06-design-elements-and-constraints.md`
8. `07-traceability.md`
9. `08-design-rationale.md`
10. `09-risks-and-mitigations.md`
11. `10-summary.md`

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
- Treat core architecture/view/element formalization (`04`, `5.1`, `6.1` with formal fields) as required.
- Treat quality scenarios and future-evolution notes as recommended enhancements; allow omission with concise `N/A rationale`.
- If an item is omitted, provide a short `N/A rationale`.
- Favor correctness and implementability over ceremonial detail.
- Keep terminology consistent with the project domain.
- Prefer `UX consistency` / `visual design constraints` over vague labels such as `aesthetics`.
- Prefer `single consolidated stylesheet` over `monolithic stylesheet`.
- If the user asks for exact IEEE wording, decline and provide a non-verbatim summary.

## Output Quality Bar

- SDD sections are complete enough for implementation handoff.
- `index.md` provides stable navigation and document control.
- Architecture overview is explicit and includes logical plus deployment/runtime depiction.
- Viewpoint choices are explicit with viewpoint-to-view mapping.
- Design elements are formally defined with component fields.
- Terminology, component names, and version/references are internally consistent across files.
- Gap report recommendations are actionable and prioritized.
- No machine-specific assumptions or absolute local-only dependencies in document content.

## Example Requests That Should Trigger This Skill

- "Write an SDD document set with an IEEE 1016-inspired structure from this PRD and repo structure."
- "Review this multi-file SDD and list standards gaps with fixes."
- "Update our SDD docs after moving from monolith to microservices."
- "Map PRD requirements to design sections and identify missing architecture details."
