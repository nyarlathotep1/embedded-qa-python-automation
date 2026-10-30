# 3 · Quality Risk Register

Risk priority below is **a planning assessment**, not a measured production failure probability. We use P1 for risks that may prevent reliable telemetry or device operation and P2 for observability gaps. `Observed` relates only to the training firmware and executed scenarios.

| ID | Quality risk | Requirement | Potential impact | Planned detection | Priority | Observed evidence |
| --- | --- | --- | --- | --- | --- | --- |
| QR-01 | Reconnect storm under network loss | R2 | CPU, broker and network overload; elevated power draw | NET DOWN, log retry/backoff, recover with NET UP | P1 | FAIL: repeated reported 50 ms backoff |
| QR-02 | Offline telemetry silently lost | R3, R5 | Missing time series, misleading monitoring | NET DOWN, 5 SEND, track each ID during flush | P1 | Offline queue PASS, delivery integrity deficient |
| QR-03 | Buffer overflow policy fails | R4 | Message loss, reordering, or incorrect stored data | Boundary 8, 9, 12; verify dropped/IDs | P1 | FAIL: count exceeded 8, dropped=0 |
| QR-04 | Duplicate publish after reconnect | R6 | Double-counted events or incorrect downstream actions | Count `publish id=` per distinct ID | P1 | FAIL: 5 IDs produced 10 publishes |
| QR-05 | Progressive memory retention/leak | R7 | Eventual allocation failure, reboot or stall | 5 × STRESS 100; idle STATUS | P1 | FAIL: −40,004 B after 500 messages |
| QR-06 | Reconnect never returns to connected | R1, R5 | Long outage even after service restoration | NET UP, STATUS + state transitions | P1 | PASS in tested simulated recovery |
| QR-07 | Diagnostics hide faults / wrong counters | R8, R4, R6 | Unreliable monitoring, delayed diagnosis | Verify field presence and reconcile counters with logs | P2 | PARTIAL: fields present; dropped count wrong |
 
## Prioritization rationale

Data integrity and loss of device function dominate the risk model. A `P1` test must run for each relevant firmware revision, even if other tests pass. Reconnect and recovery can be functional while end-to-end telemetry correctness is still broken.

## Assumptions and limits

- Impact is a *possible* consequence; no real broker, actuator or customer data was harmed in the simulation.
- A tested PASS is scoped to the exact scenario, not a blanket claim that the risk cannot materialize.
- Exact reconnect frequency was not measured from timestamps; only firmware-reported backoff values and attempt counters were observed.

[Back to Case Study](README.md)
