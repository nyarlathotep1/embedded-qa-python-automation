import json
import time

import serial


class Device:
    def __init__(self, port, baudrate=115200, timeout=1.0):
        # serial_for_url accepts physical COM ports and Wokwi RFC2217 URLs.
        self.ser = serial.serial_for_url(port, baudrate=baudrate, timeout=timeout)
        time.sleep(0.2)
        self.ser.reset_input_buffer()

    def close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()

    def command_raw(self, command):
        self.ser.reset_input_buffer()
        self.ser.write((command + "\n").encode())
        self.ser.flush()
        line = self.ser.readline().decode(errors="replace").strip()
        if not line:
            raise TimeoutError(f"No response for command: {command}")
        return line

    def command(self, command):
        raw = self.command_raw(command)
        try:
            return json.loads(raw)
        except json.JSONDecodeError as e:
            raise AssertionError(f"Invalid JSON from device: {raw!r}") from e
