---
name: architecture-decision-record
description: Draft, review, and supersede Architecture Decision Records (ADRs) with explicit context, alternatives, consequences, and preserved decision history. Use for requests to document architectural decisions, review ADRs, replace an accepted decision, or assess whether a major design change, technology adoption/deprecation, or tradeoff merits an ADR.
license: MIT
metadata:
  author: RJTPP
  version: 0.1.0
---

# Architecture Decision Record

Record one consequential decision per ADR. Keep evidence, unresolved questions, and decision status explicit.

## Resources

- Read [references/adr-template.md](references/adr-template.md) when drafting or superseding a record.
- Read [references/gap-report-template.md](references/gap-report-template.md) when writing review findings.
- Use [scripts/check_doc_artifacts.py](scripts/check_doc_artifacts.py) to check saved gap-report history.

Resolve scripts from this skill's installation directory, not the project working directory. Script arguments refer to the project being documented.

## When To Write

- An explicit request to create, update, review, or supersede an ADR authorizes the corresponding outputs.
- For a major design change without an ADR request, briefly suggest recording it and wait for the user's agreement before creating files. Loading this skill alone does not authorize an ADR.
- Exploratory discussion is not an accepted decision. Explain what could be recorded without treating a recommendation as approval.
- If no decision context or existing ADR is supplied or discoverable, ask for the minimum context needed. Otherwise proceed with documented assumptions; do not invent project facts, alternatives considered, or reasons for rejection.

## Defaults And Modes

- Mode: `draft+review`.
- Canonical root: `docs/adr/`, with one `NNNN-short-title.md` per record and an `index.md`.
- Artifact parent root: `.agent-doc-skills/`; gap reports go under `adr/gaps/YYYY-MM-DD.md`.
- New record status: `Proposed`, unless the user explicitly confirms acceptance or supplied context clearly records an accepted decision.
- Dates: use the actual current date in `YYYY-MM-DD` format for new records and reports. Preserve a historical record's original date.

Resolve explicit mode keywords first, then natural-language intent, then the default:

| Mode | Outputs |
| --- | --- |
| `draft+review` | Create/update an ADR and index, then write a gap report. |
| `draft-only` | Create/update an ADR and index; omit the gap report unless requested. |
| `review-only` | Review existing records and index; write a gap report without changing canonical files. |
| `supersede` | Create a replacement; complete reciprocal links and status updates once explicitly accepted, then write a gap report. |

Custom canonical and artifact roots must be relative directories inside the project repository. Reject absolute paths, parent traversal, symlinks escaping the project, and sensitive locations such as `.git/`. Read available conventions before choosing paths; preserve established ADR locations and formats unless the user requests migration.

## Record And Index Contract

For a new collection, use the ADR template with body metadata: `ID`, `Date`, `Status`, and optional `Supersedes` / `Superseded By` links. Do not introduce YAML document metadata or Git drift anchors.

Require these sections in order: Context, Decision, Alternatives Considered, Consequences, Related Links. Alternatives must distinguish evidence of actual consideration from options suggested during review. Use a brief explanation when no alternatives were documented. Consequences should include benefits, costs/risks, and follow-up work when known.

Use `# ADR NNNN: Title` and a lowercase kebab-case filename for new records. Inspect the full collection, choose one greater than the highest allocated numeric ID (start at `0001`, at least four digits), and never reuse a retired ID or overwrite an existing record. For established collections, preserve their numbering and filenames. If IDs conflict or the next ID is ambiguous, ask rather than renumbering history.

Maintain an index table in numeric order with `ID | Title | Status | Date | Links`. Link the title to the record and include supersession links when applicable. Keep its metadata consistent with the records. Preserve an existing index's useful content and conventions. In review-only mode, report missing/stale index content instead of repairing it.

## Draft And Review

1. Read the supplied decision, relevant repository context, existing ADRs/index, and any directly related SDD sections. Confirm which choice is proposed or accepted from evidence.
2. Allocate an ID for a new record or identify the existing record to update. Draft concise context, decision, evidenced alternatives, consequences, and relative links. Mark unknowns explicitly.
3. Update the index for authorized canonical changes. Preserve accepted decision text during lifecycle changes; a changed accepted decision needs a new ADR rather than silently rewriting its rationale. Explicit editorial corrections can update wording without changing the decision.
4. Check required sections, status evidence, ID uniqueness, index accuracy, relative link targets, rationale, consequences, and active supersession relationships. These are review checks, not a claim of standards compliance.
5. For draft+review or review-only, save findings using the gap-report workflow below, including a clear coverage summary when no gaps were found.

`review-only` may inspect one record or a collection. Review only the supplied scope and directly related records needed to check links; preserve source ADRs and the index byte-for-byte.

## Decision Lifecycle

Supported statuses are `Proposed`, `Accepted`, `Rejected`, and `Superseded`. Record acceptance or rejection only when the user or supplied decision evidence supports it. Do not infer acceptance from implementation alone.

For `supersede`:

1. Identify an existing Accepted record and the replacement decision. If the target is ambiguous, absent, or not Accepted, report the mismatch and ask for the intended target.
2. Allocate a new ID and draft the replacement. Acceptance of the old decision does not imply acceptance of the replacement.
3. If the replacement is still Proposed, leave the old record Accepted, do not add active supersession metadata, and identify the intended predecessor in Related Links. Update the index for the proposed record and explain what acceptance would change. A gap report is optional for this pending branch unless requested.
4. Once the user explicitly accepts the replacement, set it Accepted with `Supersedes` linking to the old record. Change only the old record's Status to Superseded and add `Superseded By` linking to the new record; preserve its ID, date, and decision text.
5. Reuse an already-created proposed replacement when completing acceptance instead of creating another record. Preserve older links in a supersession chain, avoid self-links/cycles, and verify both records and the index agree before reporting completion.
6. Write a gap report for completed supersession. Report any unresolved history or rationale problems clearly.

## SDD Relationships

ADRs work without an SDD. When one exists, link relevant rationale or locked-decision sections using valid relative paths and Markdown heading anchors. Recommend SDD updates in findings or the final response. Do not edit SDD files unless separately requested; an ADR request alone does not authorize an SDD update.

## Gap Reports And Validation

- Write `.agent-doc-skills/adr/gaps/YYYY-MM-DD.md` (or the custom artifact parent root) using the gap-report template. Keep canonical ADRs separate from review artifacts.
- Each review entry contains Scope and Inputs, Findings, Recommended Fixes, and Coverage Summary. Identify the reviewed ADRs, status/lifecycle evidence, prioritized fixes, and any unverified assumptions. Report missing evidence as a gap rather than filling it with invented history.
- On repeat runs the same day, append a new review entry with a current timestamp and timezone. If a timestamp repeats, add an entry number. Preserve prior entries and reports on other dates.
- Confirm the current run's dated file and new entry exist, then invoke the bundled checker from its real installation path:

```bash
python3 <skill-dir>/scripts/check_doc_artifacts.py --artifact-root .agent-doc-skills --doc-kind adr --artifact-kind gaps
```

Use the actual artifact parent root for custom locations. The checker verifies artifact existence, dated filenames, and readability; it does not validate ADR content or ensure the current run wrote a report. Review content and confirm the new entry separately. Treat a missing expected report as a failure even if older reports let the checker pass.

Finish with record/report paths, the resulting status, unresolved questions, and any suggested SDD updates. This version has no ADR drift mode or dedicated structure validator.
