## 8. Design Rationale

### 8.1 Key Decisions
Asynchronous ingestion isolates OCR latency from operator interactions.

### 8.2 Alternatives Considered
A synchronous OCR path was rejected due to latency and vendor volatility.

### 8.3 Tradeoff Analysis
Queue-based processing adds operational complexity but improves resilience and throughput.
