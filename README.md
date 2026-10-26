# Embedded QA — Python/Pytest Automation (Webinar 6)

Student homework: **ESP32 UART CLI testing** using Python, Pytest and PySerial, with Wokwi as the simulated device.

## What's included

- `tests/test_firmware_cli.py` — **5 custom parametrized negative / state-integrity cases**: PWM values `-1`, `101`, `999`, `abc`, `50.5`.
- `device.py` — UART/RFC2217 client with JSON parsing and a finite response timeout.
- `conftest.py` — Pytest device fixture and RESET cleanup.
- `requirements.txt`, `pytest.ini` — test dependencies and configuration.

The Wokwi firmware is provided separately in the course materials and is **not included** in this repository. Start the `homework_buggy` simulation before running tests.

## Run on Windows (PowerShell)

From the repository root:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:DEVICE_PORT="rfc2217://localhost:4000"
python -m pytest -v
```

Wokwi must expose the UART on `rfc2217://localhost:4000` and stay running. For a physical ESP32, set `DEVICE_PORT` to its COM port.

## Recorded homework result

The **complete local course suite**, including the 14 original tests plus the 5 custom scenarios, was executed in the user's course workspace:

- **19 collected · 15 passed · 4 failed**
- All **5 custom scenarios passed**.
- Known failures in the course suite: PWM=100 rejected; RESET returns PWM=255; GET TEMP invalid JSON; PING timeout.

**Important:** This GitHub repository intentionally contains **only the five custom scenarios**, not the 14 original course cases. Running `python -m pytest -v` here collects five tests, not nineteen. The numbers above are historical local results, not GitHub CI results. They may vary based on the running firmware and environment.

The fixture attempts RESET on teardown but does not yet establish a RESET precondition before each test; connection failures can affect cleanup.
