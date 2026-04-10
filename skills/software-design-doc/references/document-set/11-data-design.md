## 11. Data Design
- What to include: persistent model, data contracts, retention, and access patterns.
- Minimum evidence: canonical entities and data boundaries identified.

### 11.1 ERD Summary
- What to include: core entities and relationships.
- Minimum evidence: primary keys and major foreign-key relationships.

### 11.2 Data Description
- What to include: store purpose, lifecycle states, and consistency expectations.
- Minimum evidence: read/write patterns and consistency assumptions.
- Future evolution note: include expected migration path when current storage is intentionally minimal/static.

### 11.3 Data Dictionary
- What to include: key fields, semantics, and validation constraints.
- Minimum evidence: critical fields for core workflows documented.

### 11.4 Client-side Cache/Storage Model
- What to include: cache layers, invalidation, TTL, and offline behavior.
- Minimum evidence: cache coherence and invalidation strategy documented.
