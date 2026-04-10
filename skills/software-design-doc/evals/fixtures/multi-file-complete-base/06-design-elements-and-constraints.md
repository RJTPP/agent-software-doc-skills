## 6. Design Elements and Constraints

### 6.1 Design Element Catalog (Formal Definitions)
Component: API Service
Responsibility: Serve tenant-scoped invoice operations and publish workflow events.
Inputs: Authenticated HTTP requests, admin configuration changes.
Outputs: JSON responses, queue messages, audit events.
Dependencies: Postgres, message queue, identity provider.
Public Functions: createInvoice, submitForApproval, exportBatch

### 6.2 Interfaces and Data Structures
Versioned REST resources and event payload schemas define compatibility boundaries.

### 6.3 Relationships
The API owns workflow initiation while workers own asynchronous processing and retries.

### 6.4 Constraints and Assumptions
All persisted records must remain tenant-scoped and auditable.

### 6.5 Runtime State and Data Notes (Recommended)
Persistent data lives in Postgres. Runtime state lives in queue and worker memory.
