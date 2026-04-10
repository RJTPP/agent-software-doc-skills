## 4. Architecture Overview

### 4.1 Logical Architecture
The architecture separates operator experience, orchestration, domain services, and external adapters.

### 4.2 Deployment and Runtime Topology
API and UI run in-region, workers scale independently, and background jobs share the queue and persistence layer.

### 4.3 Critical Flow Summary
Invoice submission flows through validation, OCR, exception handling, approval, and export.
