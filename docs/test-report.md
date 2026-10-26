<!-- Snapshot of the Google Docs QA report. Update manually when the Google Doc changes. -->

> **Source (editable):** [Google Docs Test Report](https://docs.google.com/document/d/1nAbP0ulq0aC19MI5TuiUNGAtnZK4YVzIr5v7H86u_xE/edit)  
> **Note:** This Markdown file is a snapshot. Changes to Google Docs are not automatically synchronized with GitHub.

# EMBEDDED QA

## WEBINAR 6 — PYTHON / PYTEST AUTOMATION

ESP32 firmware · Wokwi · Serial / RFC2217 · Final Test Summary

Звіт за домашнім завданням  |  26 жовтня 2026

## EXECUTIVE SUMMARY

OVERALL RESULT — FAIL

Завершальний запуск: 19 тестів, із них 15 PASSED і 4 FAILED. Усі 5 доданих власних параметризованих сценаріїв пройшли. Повторно відтворено чотири відхилення: PWM=100, RESET safe state, GET TEMP JSON та PING timeout.

Цей результат означає, що тестова автоматизація функціонує, а тестована buggy firmware не проходить весь набір перевірок. Причину кожного FAIL потрібно відрізняти від власне повідомлення Pytest; не всі падіння за будь-яких умов автоматично є дефектами прошивки.

## 01  TEST SCOPE & ENVIRONMENT

System under test: навчальна прошивка ESP32 із папки homework_buggy; автоматизація з папки automation.

Platform: Windows; Python 3.14.7; pytest 9.1.1; PySerial 3.5; VS Code / PlatformIO; Wokwi Simulator.

Connection: DEVICE_PORT = rfc2217://localhost:4000, baudrate = 115200.

Execution: python -m pytest -v  |  29.42 секунди.

Requirements: webinar_6_python_automation/requirements/device_requirements.md (10 вимог до PING, STATUS, GET TEMP, LED, PWM, RESET, unknown commands, timeout та інтерпретації результатів).

Evidence: вивід Pytest з першого прогону (14 tests), повторні ізольовані прогони 4 FAIL, перевірка власних тестів (13 tests) і завершальний прогін (19 tests).

## 02  EXECUTION SCORECARD

19 COLLECTED  |  15 PASSED  |  4 FAILED  |  0 SKIPPED

Pass rate: 78.9%  |  Run time: 29.42 s  |  Warnings: 38.

38 warnings — DeprecationWarning у бібліотеці PySerial (setDaemon / setName), по два попередження для кожного з 19 тестів. Це не додаткові FAIL.

Наявні тести (14): 10 PASS, 4 FAIL.

Власні тести (5): 5 PASS, 0 FAIL.

FAILED: test_pwm_valid_boundaries[100]; test_reset_restores_safe_state; test_temperature_is_valid_json; test_ping.

Boundary-only rerun: 13 collected, 12 passed, 1 failed (PWM=100); з'єднання з Wokwi працювало.

## 03  CUSTOM PARAMETRIZED TESTS — 5 / 5

Test group A: test_invalid_pwm_does_not_change_state(value)

Вхідні значення: -1, 101, 999. Результат: 3/3 PASSED.

Test group B: test_pwm_invalid_format_does_not_change_state(value)

Вхідні значення: "abc", "50.5". Результат: 2/2 PASSED.

Обидві групи: SET PWM 50 → STATUS (before) → SET PWM invalid → перевірка status=ERROR → STATUS (after) → assert after['pwm'] == before['pwm']. Для групи A також перевіряється code=INVALID_VALUE.

Важлива відмінність: команда SET PWM 50 і STATUS можуть повертати PWM у різних шкалах; раніше STATUS показував 127 після SET PWM 50. Тому в цих тестах коректно порівнюються before/after, а не використовується жорстке припущення STATUS.pwm == 50.

Ці тести покривають boundary, negative input validation та state integrity. Нові форматні кейси очікують ERROR і незмінність стану; точний код помилки для тексту та десяткового дробу в requirements окремо не визначений.

## 04  BUG REPORTS — CONFIRMED OBSERVATIONS

### BUG-001  |  PWM 100 IS REJECTED

Severity: Medium  |  Test: test_pwm_valid_boundaries[100]  |  Reproducibility: 2/2.

Requirement: SET PWM N приймає всі цілі числа від 0 до 100 включно.

Steps to reproduce: 1) Запустити Wokwi; 2) Надіслати SET PWM 100 через PySerial/pytest; 3) Перевірити статус відповіді.

Expected: JSON status = OK; валідне значення 100 приймається.

Actual: response status = ERROR, тому assert 'ERROR' == 'OK' і тест FAILED.

Evidence: test_boundaries.py:6; повний прогін та ізольований запуск PWM[100].

Classification: Firmware behavior mismatch (сильна підстава); точну помилку порівняння в коді не підтверджували.

### BUG-002  |  RESET DOES NOT RESTORE SAFE PWM

Severity: High  |  Test: test_reset_restores_safe_state  |  Reproducibility: 2/2.

Requirement: RESET повертає безпечні виходи — LED OFF, PWM 0.

Steps to reproduce: 1) SET LED ON; 2) RESET; 3) STATUS; 4) Перевірити поле pwm.

Expected: pwm = 0, led = false.

Actual: pwm = 255; assert 255 == 0; перевірка led не була досягнута після FAIL за PWM.

Evidence: test_relay.py:9; повний та ізольований запуск.

Classification: High-priority firmware / state safety mismatch. Логічний PWM після RESET підтверджений, але фізичний duty cycle окремо не вимірювали.

### BUG-003  |  GET TEMP RETURNS INVALID JSON

Severity: Medium  |  Test: test_temperature_is_valid_json  |  Reproducibility: 2/2.

Requirement: GET TEMP повертає валідний JSON з температурою або явною sensor error.

Steps to reproduce: 1) Запустити ESP32; 2) GET TEMP; 3) Спробувати json.loads(response).

Expected: синтаксично валідний JSON; температура або структурована помилка датчика.

Actual raw response: {"status":"OK","temperature":24.5

Actual failure: JSONDecodeError → AssertionError: Invalid JSON from device.

Evidence: device.py:29–31; tests/test_sensor.py:2; повний та ізольований запуск.

Classification: Repeatable protocol-format mismatch; внутрішню причину (формування повідомлення чи передача) не встановлено.

### BUG-004  |  PING DOES NOT RESPOND

Severity: Medium (provisional)  |  Test: test_ping  |  Reproducibility: 2/2.

Requirement: PING → valid JSON with status=OK.

Steps to reproduce: 1) Запустити/перезапустити Wokwi; 2) Виконати isolated test_ping; 3) Дочекатися відповіді PySerial.

Expected: JSON з status=OK (тест також очікує command=PING).

Actual: TimeoutError: No response for command: PING; у межах timeout=1.0 s немає рядка відповіді.

Evidence: tests/test_status.py:2; device.py:23; повний та ізольований запуск.

Classification: Підозра на firmware command-handling defect; інші UART-команди працювали, але причину відсутності відповіді не встановлено, тому зв'язок/парсер окремо не виключено.

## 05  TIMEOUT, PRECONDITION & CLEANUP

TIMEOUT — VERIFIED: Device(port, timeout=1.0) задає скінченний таймаут serial.readline(). Після порожньої відповіді виникає TimeoutError. Готовий test_no_response_becomes_timeout для NO_RESPONSE пройшов у загальному наборі.

PRECONDITION — PARTIAL: поточний conftest.py створює Device і передає його тесту, але не надсилає RESET перед yield. Деякі тести самостійно встановлюють власний стан (наприклад, SET PWM 50), але контрольований baseline для кожного тесту через fixture ще не реалізований.

CLEANUP — IMPLEMENTED, RECOVERY NOT ROBUST: fixture після yield намагається dev.command('RESET') і завжди закриває порт у finally через dev.close(). Це коректне завершення з'єднання за наявності відповіді; коли Wokwi переставав відповідати, cleanup також викликав TimeoutError і породжував ERROR у teardown.

ENVIRONMENT INCIDENT: в одному прогоні 13 тестів дали TimeoutError на RESET/SET PWM через недоступний UART. Після Restart Wokwi тест PWM=50 став PASS, а всі 13 тестів дали змістовний результат (12 PASS / 1 FAIL). Цей інцидент класифіковано як temporary communication/environment issue, а не як 13 нових firmware defects.

Рекомендація до framework: додати контрольований RESET-before-yield (із явним перехопленням помилки підключення), ізолювати потік виконання teardown, а також окремо логувати raw serial response при protocol failures.

## 06  REQUIREMENT COVERAGE

REQ 1 — PING valid JSON: FAIL (TimeoutError).

REQ 2 — STATUS valid JSON + state/heap: PASS у готовому test_status.

REQ 3 — GET TEMP valid JSON or sensor error: FAIL (malformed JSON).

REQ 4 — SET LED ON/OFF: PASS у test_led_on_off; повний safe state після RESET — FAIL за PWM.

REQ 5 — PWM integers 0..100 inclusive: FAIL на 100; інші валідні перевірені значення пройшли.

REQ 6 — Out-of-range PWM → INVALID_VALUE: PASS на -1, 101, 999.

REQ 7 — RESET → safe LED OFF / PWM 0: FAIL на PWM=255.

REQ 8 — Unknown commands → UNKNOWN_COMMAND: окремого тесту з цією точною вимогою у наданих логах не виділено; NO_RESPONSE використовується для timeout.

REQ 9 — Finite communication timeout: PASS (Device timeout + timeout test).

REQ 10 — FAILED does not imply firmware defect: виконано в аналізі; 13 timeout-based failures одного прогону відокремлено як проблему зв'язку.

## 07  QA CONCLUSION & NEXT ACTIONS

OVERALL RESULT: FAIL — buggy firmware не проходить функціональні та safety requirements; Python/Pytest framework придатний для запуску тестів.

Повторно підтверджені дефекти: PWM=100 (Medium), RESET PWM=255 (High), GET TEMP malformed JSON (Medium), PING no response (Medium provisional).

Домашнє: підключення, готовий suite, класифікація FAIL, 5 власних parameterized cases, timeout та Test Summary — виконано. Пункт «додати контрольований precondition та cleanup» — частково: cleanup є у starter fixture; контрольований precondition перед кожним тестом не додано.

Пріоритети: виправити RESET safe state; приймання PWM 100; GET TEMP JSON; розібрати PING; доповнити fixture precondition; виконати повний regression rerun 19+ тестів і зберегти лог.

Evidence storage note: цей документ містить ключові уривки й точні назви тестів, але повний raw terminal log окремим вкладенням до Google Doc не доданий. Для здачі, якщо викладач вимагає, його варто прикріпити як окремий файл.

END OF REPORT
