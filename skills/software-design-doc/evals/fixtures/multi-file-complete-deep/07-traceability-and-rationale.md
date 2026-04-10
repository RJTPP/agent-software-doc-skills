## 7. Traceability

### 7.1 Requirement/Concern to Design Mapping
Compliance requirements map to 2.3, 4.2, 5.6, 6.4, and 15.5.

### 7.2 Coverage and Gaps
Offline operator workflows remain intentionally deferred.

## 8. Design Rationale

### 8.1 Key Decisions
Bounded services and explicit async orchestration reduce coupling around OCR and export vendors.

### 8.2 Alternatives Considered
A single workflow monolith was rejected due to scaling and ownership pressure.

### 8.3 Tradeoff Analysis
The chosen design increases integration overhead but improves resilience, operability, and team autonomy.
