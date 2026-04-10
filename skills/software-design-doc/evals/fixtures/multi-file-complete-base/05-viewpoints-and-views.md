## 5. Viewpoints and Views

### 5.1 Viewpoint-to-View Mapping
Context viewpoint maps to 5.2. Information and interface concerns map to 5.6 and 5.7.

### 5.2 Context View
Actors include finance operators, tenant admins, OCR service, and ERP systems.

### 5.3 Composition View
Subsystems are UI, API, ingestion worker, workflow engine, reporting worker, and persistence.

### 5.4 Logical View
Core entities are Invoice, ExtractionResult, ApprovalStep, and ExportBatch.

### 5.5 Dependency View
The API depends on persistence and async job publication; workers depend on queue and OCR provider.

### 5.6 Information View
Invoice data is tenant-scoped and flows from upload through approval to export archives.

### 5.7 Interface View
REST APIs serve operator actions and events coordinate ingestion and reporting.

### 5.8 Interaction / State / Algorithm Views (as applicable)
Approval states transition from draft to review, approved, rejected, and exported.

### 5.9 Resource View (as applicable)
Queue throughput and OCR concurrency are the dominant scaling controls.
