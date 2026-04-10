## 6. Design Elements and Constraints

### 6.1 Design Element Catalog (Formal Definitions)
Component: Approval Service
Responsibility: Evaluate policy, manage approval tasks, and emit audit-safe approval events.
Inputs: Workflow commands, operator actions, policy snapshots.
Outputs: Approval decisions, audit records, export readiness events.
Dependencies: Postgres, queue, policy engine.
Public Functions: assignReviewer, approveInvoice, rejectInvoice

### 6.2 Interfaces and Data Structures
Approval commands and invoice aggregates are versioned to preserve workflow compatibility.

### 6.3 Relationships
Approval depends on ingestion outputs and informs export readiness through explicit events.

### 6.4 Constraints and Assumptions
No component may bypass tenant authorization or audit emission.

### 6.5 Runtime State and Data Notes (Recommended)
Persistent state is relational, transient workflow state is queued, and cached policy snapshots expire within five minutes.
