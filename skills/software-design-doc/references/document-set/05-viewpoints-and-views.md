## 5. Viewpoints and Views
- What to include: selected viewpoints and the concrete views produced from each.
- Minimum evidence: every high-priority concern is covered by one or more views.

### 5.1 Viewpoint-to-View Mapping
- What to include: explicit mapping table from viewpoint to concrete view sections.
- Minimum evidence: each selected viewpoint maps to at least one named view.

### 5.2 Context View
- What to include: system boundary, actors, external systems, and trust boundaries.
- Minimum evidence: boundary diagram or equivalent structured description.

### 5.3 Composition View
- What to include: major subsystems/components, layers, and ownership boundaries at architectural level.
- Minimum evidence: decomposition with responsibilities per component (avoid raw file-by-file listings in this section).
- Optional detail: map components to concrete file/module paths in implementation sections or appendices.

### 5.4 Logical View
- What to include: domain model/types and key invariants.
- Minimum evidence: principal entities/types and their relationships listed.

### 5.5 Dependency View
- What to include: compile/runtime dependencies and coupling constraints.
- Minimum evidence: critical dependency paths and impact notes.

### 5.6 Information View
- What to include: data entities, stores, lifecycle, and access boundaries.
- Minimum evidence: key data flows and data ownership documented.

### 5.7 Interface View
- What to include: API contracts, events, protocols, and error semantics.
- Minimum evidence: interface contract examples with request/response or event schema.

### 5.8 Interaction / State / Algorithm Views (as applicable)
- What to include: behavior over time, state transitions, and key algorithms.
- Minimum evidence: at least one critical runtime flow represented.

### 5.9 Resource View (as applicable)
- What to include: performance, scaling limits, quotas, and capacity assumptions.
- Minimum evidence: resource budgets or SLO-linked constraints documented.
