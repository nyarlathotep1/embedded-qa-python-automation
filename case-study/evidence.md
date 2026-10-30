# 5 · Evidence Register

## Primary evidence — selected IoT node (Wokwi)

| Evidence ID | Requirement | Observed result | Source/trace |
|---|---|---|---|
| EV-01 Baseline | R1,R8 | CONNECTED, broker=true, buffer=0/8, counters=0, heap=350868 | Initial STATUS |
| EV-02 Reconnect | R2 | First reported 500 ms backoff, later 50 ms repeatedly; 336 and 435 attempts observed in separate recovery runs | NET DOWN/UP logs |
| EV-03 Offline queue | R3 | Queued IDs 1–5, BUFFER count=5/8, dropped=0 | SEND ×5 offline |
| EV-04 Overflow | R4 | At 9 messages: 9/8 dropped=0; at 12: 12/8 dropped=0 | BUFFER logs |
| EV-05 Duplicates | R6 | Five unique IDs produced ten publish entries; sent=10 duplicates=5 | Flush of five |
| EV-06 Heap | R7 | 349884 → 341884 → 333884 → [300 not captured] → 317880 → 309880 B, idle 309880 | Five STRESS 100 + STATUS |

**Detailed source:** [Homework 7 — IoT Network Testing QA Report](https://docs.google.com/document/d/126fvFYXzWC-jdOEz_RiQoUFtV60L0TmRSE6S5HuL3Rg/edit). The extracted UART logs were supplied during the exercise; complete original raw logs are **not** included in this GitHub repo. Log excerpts and observed/expected contrasts are in [Bug Reports](bug-reports.md).

### Memory stability evidence

| Iteration | Messages total | Free heap (bytes) | Remark |
|---|---:|---:|---|
| 0 | 0 | 349884 | Separate stress-phase baseline |
| 1 | 100 | 341884 | −8000 |
| 2 | 200 | 333884 | −8000 |
| 3 | 300 | — | Not captured in provided excerpt |
| 4 | 400 | 317880 | −16004 vs 200 |
| 5 | 500 | 309880 | −8000 |
| Idle STATUS | 500 | 309880 | No recovery during short observed pause |

The initial boot heap (350868 B) **must not** be substituted for the later 349884 B stress baseline.

## Supporting evidence — separate training systems

These **demonstrate Embedded QA skills** and must not be interpreted as test results of this IoT node.

| Practice | Evidence | Competency |
|---|---|---|
| [Smart Gate Controller](https://docs.google.com/document/d/1IrJTdb2rrrvoSeZq159T8Tr7AOMy53QUqzHHVdlLJjk/edit) | 24 cases: 20 PASS, 3 FAIL, 1 BLOCKED | GPIO / state machine / safety / timeout |
| [Interrupt & Debounce](https://docs.google.com/document/d/1MCIdlbveIsD0F-fhKlCAuPbpfpC5ets7KCEth7hxwQ8/edit) | Noise accepted as logical press; short-noise scenario reproduced 5/5 | ISR, bounce, logic analyzer |
| [UART/Python Automation](https://docs.google.com/document/d/1nAbP0ulq0aC19MI5TuiUNGAtnZK4YVzIr5v7H86u_xE/edit) | 19 test cases: 15 PASS, 4 FAIL; five custom parameterized scenarios passed | Pytest, UART, BVA, negative/state testing |
| [WDT / Sleep / NVS](https://docs.google.com/document/d/15COrL-vUTrdvnlFhEyEcGxBkvmDZotUFSGCyLE40-kg/edit) | Fault-injection logs and report | Recovery, persistence, safe-state validation |

I²C SDA/SCL and ACK/NACK decoding was practiced separately; this does not demonstrate the selected IoT node's MQTT implementation.

## Evidence limitations

- No timestamp-derived retry interval measurements; `backoff_ms` is firmware-reported.
- No broker capture/ACK trace; `[MQTT] publish` is simulated UART evidence.
- The heap observation is one continuous five-batch run with a short idle check, not a repeated long-duration soak test.
- Simulation only; no physical ESP32 RF or power measurements.
- External Google Docs permissions may need to be set for reviewer access.

[Case Study](README.md)
