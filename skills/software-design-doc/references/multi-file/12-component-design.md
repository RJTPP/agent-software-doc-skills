## 12. Component Design
- What to include: subsystem-level internal design for implementation handoff.
- Minimum evidence: major subsystems have clear responsibilities, internal interfaces, and failure behavior.

### 12.1 Subsystem Responsibilities
- What to include: owned responsibilities and boundaries for each subsystem.
- Minimum evidence: every subsystem has a distinct role and collaboration notes.

### 12.2 Internal Interfaces
- What to include: internal APIs, commands, events, and call contracts.
- Minimum evidence: signatures or schema summaries for critical internal interfaces.

### 12.3 Public/Private API Surface
- What to include: what is stable for consumers versus internal-only.
- Minimum evidence: compatibility expectations and ownership boundaries are explicit.

### 12.4 Failure Handling and Retries
- What to include: retry behavior, timeouts, fallbacks, and idempotency rules.
- Minimum evidence: failure mode handling is defined for critical interactions.
