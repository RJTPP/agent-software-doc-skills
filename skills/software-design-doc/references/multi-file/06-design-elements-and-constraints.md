## 6. Design Elements and Constraints
- What to include: formally defined design elements, interfaces, relationships, and constraints.
- Minimum evidence: entities and constraints are reviewable and testable.

### 6.1 Design Element Catalog (Formal Definitions)
- What to include: each key component in a formal field-based definition.
- Minimum evidence: each entry includes `Component`, `Responsibility`, `Inputs`, `Outputs`, `Dependencies`, `Public Functions`.
- Example fields:
  - `Component:`
  - `Responsibility:`
  - `Inputs:`
  - `Outputs:`
  - `Dependencies:`
  - `Public Functions:`

### 6.2 Interfaces and Data Structures
- What to include: interface boundaries and key structures/schemas.
- Minimum evidence: versioning/error/compatibility expectations are explicit.

### 6.3 Relationships
- What to include: dependencies, associations, ownership, and communication paths.
- Minimum evidence: relationship direction and cardinality/strength where relevant.

### 6.4 Constraints and Assumptions
- What to include: technology, compliance, runtime, organizational, and schedule constraints.
- Minimum evidence: assumptions are explicit with risk if invalid.

### 6.5 Runtime State and Data Notes (Recommended)
- What to include: persistent data vs runtime state vs configuration boundaries.
- Minimum evidence: each category explicitly marked (or `None` with rationale).
- Future evolution note: if persistent data is currently `None`, include one short note describing a likely future data evolution path.
