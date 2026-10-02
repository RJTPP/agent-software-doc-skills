# ADR 0007: Deliver Webhooks Synchronously

## Metadata

- ID: 0007
- Date: 2026-01-15
- Status: Accepted

## Context

The invoice platform sends a webhook after creating an invoice. The small initial
workload favored keeping delivery inside the API process. PostgreSQL stores invoices.

## Decision

Call the webhook provider synchronously during invoice creation. Report provider
failures to the caller so operators can retry manually.

## Alternatives Considered

An asynchronous worker was considered but deferred to avoid operating a queue
before the delivery volume justified it.

## Consequences

The API needs no worker service. Provider outages can delay or fail invoice
creation, and operators must resolve ambiguous delivery failures manually.

## Related Links

- [SDD webhook rationale](../sdd/07-08-traceability-and-rationale.md#81-key-decisions)
