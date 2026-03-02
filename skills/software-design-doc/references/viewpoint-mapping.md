# Concern-to-Viewpoint Mapping Guide

Use this guide to justify viewpoint selection and ensure concern coverage.
This guide is independently authored; keep outputs non-verbatim and avoid reproducing standards text.

## Mapping Table

| Concern Type | Recommended Viewpoint(s) | Expected SDD Section(s) | Typical Evidence |
| --- | --- | --- | --- |
| System boundary and external actors | Context | 4.1 Context View | Use cases, external interfaces, boundary definition |
| Decomposition into modules/services | Composition, Structure | 4.2, 4.8 | Components, ownership, assembly model |
| Type model and static structure | Logical | 4.3 | Class/type models, static relationships |
| Build/runtime coupling impact | Dependency | 4.4 | Dependency graph, integration constraints |
| Persistent data and semantics | Information | 4.5 | Data entities, stores, access rules |
| API/service contracts | Interface | 4.6 | Endpoints/interfaces, schemas, error contracts |
| Collaboration behavior and flows | Interaction | 4.7 | Sequence or message flow descriptions |
| Modes, transitions, reactive behavior | State Dynamics | 4.7 | State models and transition rules |
| Procedural logic and computation | Algorithm | 4.7 | Key algorithms and decision flow |
| Performance/capacity/limits | Resources | 4.9 | Resource budgets, quotas, scaling constraints |
| Reusable architectural patterns | Patterns Use | 4.7 or 7 | Pattern choice and adaptation rationale |

Use the template section names as canonical labels. Internal aliases are fine, but map them explicitly to these headings.

## Selection Procedure

1. List stakeholders and concerns.
2. Map each concern to one or more viewpoints.
3. Prefer the minimal set that still covers all critical concerns.
4. Record omitted viewpoints as `N/A` with rationale.
5. Ensure each selected viewpoint has clear evidence in the SDD.

## Quick Completeness Check

- Each high-priority concern maps to at least one view.
- No selected viewpoint exists without corresponding section content.
- Interface and rationale are explicit, not implied.
- Traceability section links concerns/requirements to concrete design content.

## Implementation-Deep Extensions

Use this section when the detail profile is `implementation-deep`.
These sections extend the base template views; they do not replace them.

| Concern Type | Deep Section(s) | Typical Evidence |
| --- | --- | --- |
| Deployment topology and runtime boundaries | System Overview | Environment diagram, runtime boundary notes, service ownership |
| Data contracts and storage behavior | Data Design | ERD summary, data dictionary, cache/storage model |
| Service boundaries and implementation handoff | Component Design | Component responsibilities, API route matrix, failure handling |
| User interaction specifics and UX constraints | Human Interface Design | Screen/wireframe references, key flows, interaction rules |
| Requirement-to-design accountability | Requirements Traceability Matrix | Requirement mapping table with coverage status |
| Operational concerns and implementation details | Appendices | Sequence/state models, config matrix, cache/security/testing/risk notes |
| Architecture decision continuity | Design Decisions (Locked) | ADR-style decisions, rationale, deferred decisions |
