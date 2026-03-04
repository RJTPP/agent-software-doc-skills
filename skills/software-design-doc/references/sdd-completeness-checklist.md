# SDD Completeness Checklist

## Provenance

This checklist is an independently authored practical reference inspired by the public structure and terminology of IEEE 1016-2009 for implementation use.

It is intentionally non-verbatim and not a substitute for the official IEEE standard text.

Use this file for practical SDD drafting/review. It maps internal completeness checks to Clause 4 themes, Clause 5 viewpoint terminology, and Annex C-style structure guidance without reproducing IEEE text.

## Core SDD Content Coverage (Mapped to Clause 4 Themes)

For each item, provide content or mark `N/A` with a reason.

1. SDD identification

- Date of issue and status
- Scope
- Issuing organization
- Authorship
- References
- Context
- Declared design languages by viewpoint
- Body
- Summary
- Glossary
- Change history

2. Stakeholders and concerns

- Identified stakeholders
- Identified concerns per stakeholder
- Evidence that each concern is addressed

3. Views and viewpoints

- One or more design views
- Exactly one governing viewpoint per view
- Rationale for each selected viewpoint

4. Design elements quality

- Named and typed entities/relationships/constraints
- Consistent naming and typing conventions

5. Overlays and rationale

- Overlays marked and linked to a base view if used
- Design rationale documented for major decisions/tradeoffs

6. Design languages

- Chosen notations have defined syntax/semantics
- Standard or clearly defined notation references

## Viewpoint Catalog (Mapped to Clause 5 Terminology, Use When Applicable)

- Context
- Composition
- Logical
- Dependency
- Information
- Patterns Use
- Interface
- Structure
- Interaction
- State Dynamics
- Algorithm
- Resources

A viewpoint should be selected when it directly addresses identified design concerns. If not selected, provide `N/A` justification in the SDD.

## Pragmatic Completeness Gate

An SDD is acceptable when:

1. Every critical concern maps to at least one view.
2. Major architecture/interface/data decisions are explicit.
3. Missing optional depth is acknowledged with rationale.
4. The document is implementation-usable, not only descriptive.

## Annex C-Inspired Document Shape (Informal Mapping)

1. Front matter and identification
2. Introduction (purpose/scope/context/references/glossary)
3. Stakeholders and concerns
4. Viewpoint declarations and design views
5. Design rationale
6. Summary and change history
