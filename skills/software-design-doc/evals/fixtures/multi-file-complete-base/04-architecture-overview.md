## 4. Architecture Overview

### 4.1 Logical Architecture
The system is divided into web, API, workflow, ingestion, and reporting components.

### 4.2 Deployment and Runtime Topology
UI and API run in a primary region, workers consume jobs from a queue, and reporting runs on scheduled workers.

### 4.3 Critical Flow Summary
Invoice upload triggers OCR, extraction validation, approval workflow, and ERP export.
