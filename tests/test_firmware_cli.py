"""Student-authored negative/state-integrity cases for the ESP32 UART CLI.

These five parametrized cases were executed locally in test_boundaries.py.
They are kept in a separate file here to make the homework submission clear.
"""

import pytest


@pytest.mark.parametrize("value", [-1, 101, 999])
def test_invalid_pwm_does_not_change_state(device, value):
    response = device.command("SET PWM 50")
    assert response["status"] == "OK"

    before = device.command("STATUS")

    response = device.command(f"SET PWM {value}")
    assert response["status"] == "ERROR"
    assert response["code"] == "INVALID_VALUE"

    after = device.command("STATUS")
    assert after["pwm"] == before["pwm"]


@pytest.mark.parametrize("value", ["abc", "50.5"])
def test_pwm_invalid_format_does_not_change_state(device, value):
    response = device.command("SET PWM 50")
    assert response["status"] == "OK"

    before = device.command("STATUS")

    response = device.command(f"SET PWM {value}")
    assert response["status"] == "ERROR"

    after = device.command("STATUS")
    assert after["pwm"] == before["pwm"]
