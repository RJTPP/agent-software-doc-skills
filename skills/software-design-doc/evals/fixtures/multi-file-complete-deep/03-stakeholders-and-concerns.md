## 3. Stakeholders and Design Concerns

### 3.1 Stakeholder List
- Finance operators
- Tenant admins
- Compliance reviewers
- SRE

### 3.2 Concern Catalog
- Data residency compliance
- Retry safety under vendor outages
- UX consistency during approval exceptions

### 3.3 Non-Functional Targets (Recommended)
Stimulus: OCR provider intermittently fails for 15 minutes.
Environment: month-end load with high approval volume.
Response: ingestion retries safely while operator UI remains responsive.
Measurement: 99 percent of accepted uploads are recoverable without manual database repair.
