## 11. Data Design

### 11.1 ERD Summary
Core entities are Invoice, ApprovalTask, ExportRecord, and ReportSnapshot with tenant-scoped keys.

### 11.2 Data Description
Relational storage is authoritative, and append-only audit records capture approval and export history.

### 11.3 Data Dictionary
Critical fields include invoice_status, tenant_id, export_batch_id, and review_deadline.

### 11.4 Client-side Cache/Storage Model
The UI caches filter state and short-lived task lists with explicit invalidation after approvals.
