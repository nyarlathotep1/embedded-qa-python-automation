# Embedded QA — Observed Bug Reports

These are black-box observations against the training firmware in Wokwi. Severity is assessed for potential real-system impact; exact internal causes were not investigated.

## BUG-001 — Reconnect storm after network loss

**Requirement:** R2 · **Severity:** Major · **Repeatability:** observed in at least two separate loss/recovery runs (336 and 435 attempts).

- **Precondition:** CONNECTED, broker=true, baseline STATUS.
- **Steps:** `NET DOWN`; observe `[NET]` logs; `NET UP`; `STATUS`.
- **Expected:** Controlled backoff without reconnect storm; device remains responsive; reconnect when network returns.
- **Actual:** `retry=1 backoff_ms=500`, subsequently reported `backoff_ms=50` on many retries; counts of 336 and 435 observed; later `CONNECTED`.
- **Recovery:** Yes, after NET UP.
- **Evidence:**

```text
[NET] state=DISCONNECTED
[NET] state=BACKOFF
[NET] retry=1 backoff_ms=500
[NET] retry=2 backoff_ms=50
...
[NET] retry=336 backoff_ms=50
```

**Limitation:** Actual retry timing was not independently calculated from timestamped logs.

## BUG-002 — Duplicate publishing during offline buffer flush

**Requirement:** R6 · **Severity:** Major · **Repeatability:** observed with batches of 5, 9 and 12 queued messages.

- **Precondition:** NET DOWN with an offline telemetry queue.
- **Steps:** `SEND` five times; `BUFFER`; `NET UP`; read publish IDs and `STATUS`.
- **Expected:** One successful publish per ID, five total, duplicates=0.
- **Actual:** Each of IDs 1–5 appears twice; sent=10; duplicates=5; buffer cleared.
- **Recovery:** Network returned to CONNECTED but telemetry integrity failed.
- **Evidence:**

```text
[BUFFER] flush_start count=5
[MQTT] publish id=1 temp=24.5
[MQTT] publish id=1 temp=24.5
...
[BUFFER] flush_end count=0
{"net":"CONNECTED","sent":10,"duplicates":5,"buffer":0}
```

**Limitation:** Logs represent training protocol simulated publishing; not real MQTT network captures.

## BUG-003 — Buffer capacity 8 and DROP_OLDEST not enforced

**Requirement:** R4 · **Severity:** Major · **Repeatability:** overflow observed at 9 and 12 SEND scenarios (distinct boundary workloads).

- **Precondition:** NET DOWN, buffer empty, reset statistics.
- **Steps:** Offline SEND ×8, BUFFER; SEND a ninth message, BUFFER; in a fresh scenario offline SEND ×12, BUFFER; NET UP and inspect flush.
- **Expected:** Buffer occupancy max 8; nine inputs → dropped=1; twelve → dropped=4, retaining newest eight IDs.
- **Actual:** count=9/8 and 12/8; dropped=0. Published order is inconsistent and duplicates are present.
- **Recovery:** CONNECTED, flushed buffer; correctness failed.
- **Evidence:**

```text
[BUFFER] queued id=8 count=8/8
[BUFFER] overflow policy=DROP_OLDEST dropped_total=0
[BUFFER] queued id=9 count=9/8
[BUFFER] count=9 capacity=8 dropped=0
```

**Limitation:** Source-level root cause unknown; the `duplicates` counter in 12-message case did not account for all repeats under a per-ID first-publication definition.

## BUG-004 — Progressive free heap decline under telemetry stress

**Requirement:** R7 · **Severity:** Major (provisional) · **Repeatability:** observed across five consecutive stress batches in **one** continuous session; independent-run reproducibility not measured.

- **Precondition:** CONNECTED, RESET STATS, STATUS heap=349884.
- **Steps:** Five repetitions of `STRESS 100` then `STATUS`, without restarting; follow with idle STATUS.
- **Expected:** No systematic irreversible free-heap degradation.
- **Actual:** Baseline 349884 B → 309880 B after 500 publishes, net decline 40004 B (~80 B/message). Idle check remained at 309880 B.
- **Evidence:**

```text
[STRESS] start count=100 heap=341884
[STRESS] end heap=333884
{"net":"CONNECTED","sent":500,"heap":309880}
```

**Limitation:** No allocation profiling, no long soak test, and 300-message heap value missing from available excerpt. Exact root cause cannot be asserted.

[Case Study](README.md) · [Evidence](evidence.md)
