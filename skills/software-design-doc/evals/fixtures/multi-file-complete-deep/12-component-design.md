## 12. Component Design

### 12.1 Subsystem Responsibilities
Ingestion validates uploads, approval manages review workflows, and export packages ERP-ready batches.

### 12.2 Internal Interfaces
Internal commands and events define contracts between orchestration and domain services.

### 12.3 Public/Private API Surface
Public APIs are versioned REST endpoints. Internal events remain private to platform services.

### 12.4 Failure Handling and Retries
Retries are idempotent, bounded, and observable across OCR and export workflows.
