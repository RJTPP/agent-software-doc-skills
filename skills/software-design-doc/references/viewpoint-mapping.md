# Concern-to-Viewpoint Mapping Guide

Use this guide to justify viewpoint selection and ensure concern coverage.
This guide is independently authored; keep outputs non-verbatim and avoid reproducing standards text.

## Required Mapping Rule

Always include `### 5.1 Viewpoint-to-View Mapping` in the SDD.
Each selected viewpoint must map to at least one concrete view section.

## Mapping Table

| Concern Type | Recommended Viewpoint(s) | Expected SDD Section(s) | Typical Evidence |
| --- | --- | --- | --- |
| System boundary and external actors | Context | 5.2 Context View | Use cases, external interfaces, boundary definition |
| Decomposition into modules/services | Composition | 5.3 Composition View | Components, ownership, assembly model |
| Type model and static structure | Logical | 5.4 Logical View | Class/type models, static relationships |
| Build/runtime coupling impact | Dependency | 5.5 Dependency View | Dependency graph, integration constraints |
| Persistent data and semantics | Information | 5.6 Information View | Data entities, stores, access rules |
| API/service contracts | Interface | 5.7 Interface View | Endpoints/interfaces, schemas, error contracts |
| Collaboration behavior and flows | Interaction | 5.8 Interaction / State / Algorithm Views | Sequence or message flow descriptions |
| Modes, transitions, reactive behavior | State Dynamics | 5.8 Interaction / State / Algorithm Views | State models and transition rules |
| Procedural logic and computation | Algorithm | 5.8 Interaction / State / Algorithm Views | Key algorithms and decision flow |
| Performance/capacity/limits | Resources | 5.9 Resource View | Resource budgets, quotas, scaling constraints |

Use template section names as canonical labels. Internal aliases are fine only when explicitly mapped.

## Selection Procedure

1. List stakeholders and concerns from section 3.
2. Map each concern to one or more viewpoints.
3. Prefer the minimal viewpoint set that still covers all critical concerns.
4. Record omitted viewpoints with `N/A` rationale.
5. Ensure each selected viewpoint has evidence in section 5.

## Quick Completeness Check

- Every high-priority concern maps to at least one view.
- No selected viewpoint exists without corresponding section content.
- `5.1 Viewpoint-to-View Mapping` is explicit and complete.
- `4. Architecture Overview` and `6.1 Design Element Catalog` are present and consistent with mapped views.

## Implementation-Deep Extensions

Use this section when detail profile is `implementation-deep`.
These sections extend the base template views; they do not replace base sections.

| Concern Type | Deep Section(s) | Typical Evidence |
| --- | --- | --- |
| Deployment topology and runtime boundaries | 4.2 Deployment and Runtime Topology | Environment diagram, runtime boundary notes |
| Data contracts and storage behavior | 11. Data Design | ERD summary, data dictionary, cache/storage model |
| Service boundaries and implementation handoff | 12. Component Design | Component responsibilities, API route matrix, failure handling |
| User interaction specifics and UX constraints | 13. Human Interface Design | Screen/wireframe references, key flows, interaction rules |
| Requirement-to-design accountability | 14. Requirements Traceability Matrix | Requirement mapping table with coverage status |
| Operational concerns and implementation details | 15. Appendices | Sequence/state models, config matrix, cache/security/testing/risk notes |
| Architecture decision continuity | 16. Design Decisions (Locked) | ADR-style decisions, rationale, deferred decisions |
