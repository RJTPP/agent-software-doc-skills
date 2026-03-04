# Commerce Core SDD (Monolith Baseline)

## Document Control
- Version: 1.7
- Status: Approved
- Date of Issue: 2025-10-10

## 1. Introduction
### 1.1 Purpose
Describe the software design for the commerce core platform.

### 1.2 Scope
Single deployable application for catalog, checkout, billing, and notifications.

## 2. System Overview
### 2.1 Product and Runtime Context
One monolithic service handles business domains and background jobs.

### 2.2 External Systems and Integrations
Integrates with payment gateway, tax provider, and email service.

## 3. Stakeholders and Design Concerns
### 3.1 Stakeholder List
- Product: rapid feature delivery
- Operations: low operational overhead
- Security: strict auditability

### 3.2 Concern Catalog
- Checkout latency
- Release risk from shared deployable
- Data consistency across modules

## 4. Architecture Overview
### 4.1 Logical Architecture
Modules: Catalog, Orders, Billing, Notifications.

### 4.2 Deployment and Runtime Topology
Single application deployment backed by one relational database.

## 5. Viewpoints and Views
### 5.1 Viewpoint-to-View Mapping
| Viewpoint | View |
| --- | --- |
| Context | 5.2 Context View |
| Logical | 5.4 Logical View |
| Information | 5.6 Information View |
| Interface | 5.7 Interface View |

### 5.2 Context View
The monolith interfaces with payment, tax, and email providers.

### 5.4 Logical View
Modules are tightly coupled inside one runtime.

### 5.6 Information View
Single shared schema with transactional tables.

### 5.7 Interface View
REST endpoints are exposed from one application service.

## 6. Design Elements and Constraints
### 6.1 Design Element Catalog (Formal Definitions)
Component: Orders Module
Responsibility: Handle order lifecycle and orchestration.
Inputs: REST create/update order requests.
Outputs: Order state changes and domain events.
Dependencies: Catalog, Billing, shared database.

Component: Billing Module
Responsibility: Charge payment methods and issue invoices.
Inputs: Order settlement requests.
Outputs: Payment confirmations and billing records.
Dependencies: Payment gateway, shared database.

### 6.4 Constraints and Assumptions
Shared deployment lifecycle and schema coupling limit independent scaling.

## 7. Traceability
Checkout latency concern maps to Orders/Billing module boundaries.
Security concern maps to billing controls and audit logging.

## 8. Design Rationale
Monolith was selected initially to reduce delivery complexity.

## 9. Risks and Mitigations
Tight coupling increases blast radius for runtime and release failures.

## 10. Summary
Current design is stable but scaling constraints are increasing.
