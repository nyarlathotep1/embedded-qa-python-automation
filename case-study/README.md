# ESP32 IoT Environmental Monitoring Node
### Embedded QA Case Study · Risk-Based Testing · Wokwi Simulation

**System under test:** ESP32-based environmental telemetry node (DHT22 / simulated network / MQTT-like publish behavior).  
**Approach:** Black-box, requirements-driven, risk-based Embedded QA.  
**Test environment:** VS Code + PlatformIO + Wokwi UART CLI.  
**Decision:** **NO-GO** for the tested training firmware against requirements R1–R8.

> **Scope:** This case study documents a simulated training firmware build. The results are **not** validation of a physical ESP32, Wi-Fi deployment, production MQTT broker, or cloud service.

## Executive summary

The node resumed the `CONNECTED` state after simulated network loss and buffered five offline messages. However, four reliability/data-integrity issues were observed:

| Finding | Requirement | Evidence | Assessment |
| --- | --- | --- | --- |
| Reconnect attempts are excessively frequent | R2 | Reported backoff changes from 500 ms to 50 ms; hundreds of retries | FAIL |
| Buffer capacity / DROP_OLDEST violated | R4 | Capacity 8; observed `9/8` and `12/8`, `dropped=0` | FAIL |
| Duplicate telemetry on buffer flush | R6 | Five unique IDs yield ten publish log entries | FAIL |
| Progressive free heap decline | R7 | 349,884 B → 309,880 B after 500 messages, not recovered in short idle check | FAIL |

Recovery of network connectivity itself worked; **delivery correctness did not**. No root-cause claims were made without source inspection or packet-level evidence.

## 7-part assignment coverage

| Deliverable | File |
| --- | --- |
| 1. Device selection | This README + [System Overview](system-overview.md) |
| 2. Architecture, system scope and exclusions | [System Overview & Scope](system-overview.md) |
| 3. At least five quality risks | [Quality Risk Register](quality-risks.md) |
| 4. Risk/requirement-based test matrix | [Test Matrix](test-matrix.md) |
| 5. Evidence from previous embedded practices | [Evidence Register](evidence.md) |
| 6. Entry / Exit Criteria and release decision | [Entry / Exit & NO-GO](entry-exit.md) |
| 7. Published GitHub / Markdown case study | This folder, including [Bug Reports](bug-reports.md) |

## Traceability at a glance

| Requirement | Description | Observed assessment |
| --- | --- | --- |
| R1 | DISCONNECTED, CONNECTING, CONNECTED, BACKOFF states | PASS for observed states |
| R2 | Controlled auto-reconnect/backoff | **FAIL** |
| R3 | Offline telemetry buffering | PASS (five queued messages) |
| R4 | Capacity = 8, DROP_OLDEST, observable drop | **FAIL** |
| R5 | Reconnect and buffered-message flush | PARTIAL: connected/flush, but integrity failure |
| R6 | No duplicate successful publish per message ID | **FAIL** |
| R7 | No sustained irreversible heap decline under SEND/STRESS | **FAIL** in tested stress run |
| R8 | STATUS observability | PASS for required fields; timing evidence incomplete |

**Quality decision: NO-GO.** The simulated firmware does not meet the full reliability and data-integrity contract. A remediation and regression cycle is necessary.

## Evidence and reproducibility

The principal evidence is from the [Homework 7 IoT Network Testing QA Report](https://docs.google.com/document/d/126fvFYXzWC-jdOEz_RiQoUFtV60L0TmRSE6S5HuL3Rg/edit). Supporting skills are documented from other exercises, clearly marked as **separate systems** in the [Evidence Register](evidence.md). Full raw serial logs were captured in the course conversation; they are not mirrored here. Short extracts are included in [Bug Reports](bug-reports.md).

**Important limitations:** Retry intervals were not independently measured using timestamps. Simulated `[MQTT] publish` logs are not network packet captures. Only a short idle follow-up was recorded for heap recovery. Access to linked Google Docs may require sharing permissions.

## Recommended next validation

Verify reconnect timing with device timestamps; enforce buffer limit/drop counters; prove each ID is published once at flush; investigate memory retention; run timed soak/regression tests; validate on a physical ESP32 with real Wi-Fi and MQTT.

---
*Prepared from observed course executions. No physical-hardware or real-broker outcomes are claimed.*
