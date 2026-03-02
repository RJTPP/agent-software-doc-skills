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

## 2. Stakeholders and Concerns
- Product: rapid feature delivery
- Operations: low operational overhead
- Security: strict auditability

## 3. Viewpoint Strategy
- Selected: Context, Logical, Information, Interface
- Omitted: Resources (not documented), Interaction (partial)

## 4. Design Views
### 4.1 Context View
The monolith integrates with payment gateway, tax provider, and email service.

### 4.3 Logical View
Modules: Catalog, Orders, Billing, Notifications.

### 4.5 Information View
Single relational schema with shared transactional tables.

### 4.6 Interface View
REST endpoints exposed from one application service.

## 5. Design Elements and Constraints
- One shared database
- Synchronous intra-module calls
- Shared deployment lifecycle

## 6. Traceability
- Checkout latency concerns map to Billing and Orders modules.
- Security concerns map to Billing and audit logging.

## 7. Design Rationale
- Monolith was selected to reduce initial delivery complexity.

## 8. Risks and Mitigations
- Tight coupling across modules may slow independent scaling.

## 9. Summary
Current design is stable but scaling constraints are increasing.
