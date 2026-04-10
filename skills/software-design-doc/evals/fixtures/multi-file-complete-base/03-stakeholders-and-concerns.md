## 3. Stakeholders and Design Concerns

### 3.1 Stakeholder List
- Finance operators
- Tenant admins
- Platform engineering
- Support and compliance

### 3.2 Concern Catalog
- Accurate extraction under variable document quality
- Reliable approval workflows
- Operational visibility for stuck jobs

### 3.3 Non-Functional Targets (Recommended)
Stimulus: nightly report generation starts at 01:00 UTC.
Environment: 10,000 invoices processed during month-end load.
Response: reports complete without data loss and retries remain bounded.
Measurement: 95 percent complete within 30 minutes with zero cross-tenant leakage.
