# SDD Completeness Checklist

## Provenance

This checklist is an independently authored practical reference inspired by IEEE 1016-2009 structure and terminology.
It is non-verbatim and not a substitute for the official IEEE standard text.
It is unofficial internal guidance.

Use this file for practical SDD drafting/review and internal completeness checks.

## Required Base Structure

An acceptable base SDD includes these headings (template order is the default recommendation):

1. `## Document Control`
2. `## 1. Introduction`
3. `## 2. System Overview`
4. `## 3. Stakeholders and Design Concerns`
5. `## 4. Architecture Overview`
6. `## 5. Viewpoints and Views`
7. `## 6. Design Elements and Constraints`
8. `## 7. Traceability`
9. `## 8. Design Rationale`
10. `## 9. Risks and Mitigations`
11. `## 10. Summary`

## Core Formalization Checks (Required)

1. Architecture overview present
- Evidence: `## 4. Architecture Overview` includes logical + deployment/runtime depiction.

2. Viewpoint-to-view mapping explicit
- Evidence: `### 5.1 Viewpoint-to-View Mapping` maps each selected viewpoint to at least one view.

3. Formal design element definitions present
- Evidence: `### 6.1 Design Element Catalog (Formal Definitions)` includes fields: `Component`, `Responsibility`, `Inputs`, `Outputs`, `Dependencies`, `Public Functions`.

## Content Coverage (Mapped to IEEE-Inspired Themes)

For each item, provide content or mark `N/A` with rationale.

1. SDD identification and governance
- Date of issue and status
- Scope and purpose
- Issuing organization and authorship
- References and glossary
- Change history

2. Stakeholders and concerns
- Identified stakeholders
- Identified concerns per stakeholder
- Evidence each critical concern is addressed

3. Views and viewpoints
- One or more design views
- Explicit viewpoint-to-view mapping
- Rationale for selected and omitted viewpoints
- View descriptions use architectural/component language (file-level mappings deferred to implementation sections/appendices)

4. Design elements quality
- Named and typed entities/relationships/constraints
- Formal element definitions for critical components

5. Traceability and rationale
- Concern/requirement to design mapping
- Rationale documented for major decisions/tradeoffs

6. Risk treatment
- Major risks with likelihood/impact/mitigation/owner

## Recommended Enhancements

- Non-functional targets table in section `3.3`.
- Quality-attribute scenario for critical concerns using `Stimulus`, `Environment`, `Response`, `Measurement`.
- Runtime state vs persistent data vs configuration clarity in section `6.5`.
- Short future-evolution note when persistent data is currently absent/static.
- At least one architecture diagram and one runtime interaction/state diagram.

## Implementation-Deep Extensions

When `implementation-deep` profile is selected, also include:

- `## 11. Data Design`
- `## 12. Component Design`
- `## 13. Human Interface Design`
- `## 14. Requirements Traceability Matrix`
- `## 15. Appendices`
- `## 16. Design Decisions (Locked)`

A deep-profile SDD is acceptable when base requirements pass and deep extensions are complete enough for handoff.
