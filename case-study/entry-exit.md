# 6 · Entry & Exit Criteria / Release Decision

These criteria are proposed QA quality gates for this case study, not claimed as verbatim device requirements.

## Entry criteria

| Condition | Observed state |
|---|---|
| R1–R8 testable requirements available | MET |
| Firmware builds and Wokwi simulator starts | MET |
| UART CLI accepts `STATUS` and fault-injection commands | MET |
| Baseline state/counters can be read | MET |
| Planned test cases and expected results identified | MET |
| Evidence collection available for state/counters/logs | MET |
| Timestamped retry timing + complete archived logs | PARTIAL |

**Entry assessment:** Sufficient for simulated functionality/reliability testing; evidence for exact retry timing incomplete.

## Exit criteria (positive release recommendation)

- R1–R8 tested and traceable to outcomes/evidence.
- No unresolved release-blocking reliability and data-integrity issues.
- Controlled retry/backoff under network loss and successful recovery.
- Buffer capacity 8 enforced with observable, correct DROP_OLDEST.
- Each message ID successfully published no more than once.
- Buffered telemetry flushed without corruption/duplicates outside specified drop policy.
- No systematic irreversible heap decline under repeated sending.
- Regression complete, deviations and residual risks approved by responsible stakeholders.

## Exit assessment

| Gate | Result |
|---|---|
| Basic states and diagnostics observable | MET |
| Network recovers to CONNECTED | MET |
| Retry storm absent | **NOT MET** |
| Buffer/drop contract honored | **NOT MET** |
| Duplicate-free buffered delivery | **NOT MET** |
| Memory stability | **NOT MET** |
| Timing/soak evidence fully complete | PARTIAL |

## Final recommendation: NO-GO

The **tested simulated firmware** does not satisfy core reliability/data-integrity requirements R2, R4, R6 and R7. Recovery and queueing alone are insufficient because published messages are duplicated and overflow semantics fail.

### Conditions for reassessment

1. Implement controlled backoff and record actual retry intervals with timestamps.
2. Correct buffer count and DROP_OLDEST data/counters.
3. Eliminate duplicate publish after reconnect and verify every retained ID.
4. Investigate the heap trend; extend soak testing and repeat independently.
5. Rerun the risk-based matrix in Wokwi, then conduct physical ESP32 + real Wi-Fi/MQTT verification before a production release.

This is a **training build quality decision**, not an industrial certification.

[Case Study](README.md)
