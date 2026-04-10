## 5. Viewpoints and Views

### 5.1 Viewpoint-to-View Mapping
Operational concerns map to deployment, resource, and failure-handling views. Data concerns map to information and data-design files.

### 5.2 Context View
The platform sits between operators, OCR, ERP, and email systems with strict tenant boundaries.

### 5.3 Composition View
Subsystems include operator UI, API gateway, ingestion orchestrator, approval service, export service, and reporting service.

### 5.4 Logical View
Domain entities include Invoice, ApprovalTask, ExportRecord, and ReportSnapshot.

### 5.5 Dependency View
Adapters isolate third-party OCR and ERP providers from domain services.

### 5.6 Information View
Tenant-scoped records and audit trails share a relational store with bounded caches.

### 5.7 Interface View
REST APIs, internal commands, and integration events define interaction boundaries.

### 5.8 Interaction / State / Algorithm Views (as applicable)
The approval state machine coordinates manual review and retry-safe export.

### 5.9 Resource View (as applicable)
Worker concurrency, queue depth, and report generation capacity are budgeted per tenant tier.
