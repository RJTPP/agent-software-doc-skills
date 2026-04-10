## 8. Design Rationale

### 8.1 Key Decisions
Bounded services and explicit async orchestration reduce coupling around OCR and export vendors.

### 8.2 Alternatives Considered
A single workflow monolith was rejected due to scaling and ownership pressure.

### 8.3 Tradeoff Analysis
The chosen design increases integration overhead but improves resilience, operability, and team autonomy.
