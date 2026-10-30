# 4 · Risk-Based Test Matrix

| ID | Risk / requirement | Objective & procedure | Type / level | Priority | Expected | Observed |
|---|---|---|---|---|---|---|
| TM-01 | QR-07 / R1,R8 | Boot → STATUS: inspect fields and initial state | Functional / System | P1 | CONNECTED; all fields | PASS |
| TM-02 | QR-01 / R1 | NET DOWN: follow DISCONNECTED/BACKOFF/CONNECTING | State / System | P1 | Observable state transitions | PASS for observed states |
| TM-03 | QR-01 / R2 | Monitor reconnect retries during NET DOWN | Reliability / System | P1 | Controlled backoff, no storm | FAIL: reported 50 ms and hundreds of attempts |
| TM-04 | QR-06 / R5 | NET UP → STATUS | Recovery / System | P1 | CONNECTED, broker true | PASS |
| TM-05 | QR-02 / R3 | NET DOWN → 5 × SEND → BUFFER | Integration / Functional | P1 | count=5, dropped=0 | PASS |
| TM-06 | QR-02,QR-06 / R5 | NET UP after 5 queued messages | Recovery / Integration | P1 | Buffer flushed, messages available | PARTIAL: flush occurred, but duplicate publish |
| TM-07 | QR-03 / R4 | Offline SEND ×8 | BVA / Integration | P1 | count=8, dropped=0 | PASS (occupancy only) |
| TM-08 | QR-03 / R4 | Offline SEND ×9 | BVA / Integration | P1 | count=8, dropped=1 | FAIL: count=9, dropped=0 |
| TM-09 | QR-03 / R4 | Offline SEND ×12 | Negative / Integration | P1 | count=8, dropped=4 | FAIL: count=12, dropped=0 |
| TM-10 | QR-04 / R6 | Count publish occurrences by ID after flush | Data integrity / Integration | P1 | One publish per eligible ID | FAIL |
| TM-11 | QR-05 / R7 | Five consecutive STRESS 100, idle STATUS | Stress / System | P1 | No sustained irreversible decline | FAIL: −40,004 B |
| TM-12 | QR-07 / R8 | Check STATUS fields, counters and consistency | Observability / System | P2 | Required fields plus accurate counts | PARTIAL: fields present, dropped inconsistent |

### Levels and priorities

**Integration** exercises interactions between node, buffer and publish logic through CLI. **System** verifies device-wide behavior in simulation. P1 is release-significant, P2 supports diagnostics. This is a retrospective matrix mapped to executed tests, not claims of executed unit/hardware tests.

### Traceability

R1 TM-01/02; R2 TM-03; R3 TM-05; R4 TM-07/08/09; R5 TM-04/06; R6 TM-10; R7 TM-11; R8 TM-01/12.

[Evidence](evidence.md) · [Case Study](README.md)
