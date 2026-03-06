# Quality Attribute Scenarios

Use this pattern when documenting quality-sensitive design concerns.

## Scenario Template

Use at least one scenario for each critical quality concern area (for example performance, reliability, security, accessibility):

- `Scenario:` short label
- `Stimulus:` event or trigger
- `Environment:` runtime context/conditions
- `Response:` expected system behavior
- `Measurement:` concrete threshold or verification metric

## Example: Smooth Animation

- `Scenario:` Smooth animation under user scroll
- `Stimulus:` user scrolls the page continuously
- `Environment:` modern desktop browser on standard hardware
- `Response:` animation pipeline remains responsive without visible stutter
- `Measurement:` rendered frame rate remains >= 60 FPS in performance tooling

## Example: Accessibility Compliance Gate

- `Scenario:` Keyboard-only navigation
- `Stimulus:` user navigates all interactive elements via keyboard
- `Environment:` production build in supported browsers
- `Response:` focus order and visible focus states remain correct
- `Measurement:` no blocking accessibility issues in automated audits and manual keyboard walkthrough

## Example: Database Failover Resilience

- `Scenario:` Primary database node failure
- `Stimulus:` primary DB instance becomes unavailable (crash or network partition)
- `Environment:` production environment with replica configured
- `Response:` system automatically promotes replica and resumes accepting reads and writes
- `Measurement:` total downtime does not exceed 30 seconds; no data loss for committed transactions

## Example: Authentication Security Gate

- `Scenario:` Brute-force login attempt
- `Stimulus:` an automated client sends more than 10 failed login requests for a single account within 60 seconds
- `Environment:` production API endpoint exposed to the internet
- `Response:` account is temporarily locked and subsequent attempts are rejected with a rate-limit error
- `Measurement:` lock triggered within the same 60-second window; legitimate user can recover via email reset within 5 minutes
