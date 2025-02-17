from kmk.keys import KC
from kmk.modules import Module
import time


class PowerMode(Module):
    def __init__(
        self,
        window_sec: float = 10.0,
        ignore_keys: list[KC] = [],
        power_mode_min_wpm: float = 20.0,
        power_mode_min_duration_sec: float = 5.0,
    ):
        self.window_sec = window_sec
        self.ignore_keys = ignore_keys
        self.logs: list[int] = []
        self.wpm: float = 0.0
        self.power_mode_min_wpm = power_mode_min_wpm
        self.power_mode_min_duration_sec = power_mode_min_duration_sec

        self.power_mode_start_time = None
        self.power_mode_percent: float = 0.0

    def during_bootup(self, keyboard):
        return

    def matrix_detected_press(self, keyboard):
        return keyboard.matrix_update is None

    def before_matrix_scan(self, keyboard):
        return

    def process_key(self, keyboard, key, is_pressed, int_coord):
        if is_pressed and key not in self.ignore_keys:
            self.logs.append(int(round(time.time_ns())))

        return key

    def before_hid_send(self, keyboard):
        return

    def after_hid_send(self, keyboard):
        return

    def on_powersave_enable(self, keyboard):
        return

    def on_powersave_disable(self, keyboard):
        return

    def after_matrix_scan(self, keyboard):
        start_of_window = time.time_ns() - self.window_sec * 1_000_000_000
        self.logs = [log for log in self.logs if log >= start_of_window]
        self.wpm = len(self.logs) / 5.0

        if self.wpm > self.power_mode_min_wpm:
            if not self.power_mode_start_time:
                # Start the power mode timer
                self.power_mode_start_time = time.time_ns()
            elif (
                # Check if our wpm has been above the minimum for the min duration
                time.time_ns() - self.power_mode_start_time
                > self.power_mode_min_duration_sec * 1_000_000_000
            ):
                self.power_mode_percent = (
                    time.time_ns() - self.power_mode_start_time
                ) / (self.power_mode_min_duration_sec / 1_000_000_000)
        else:
            self.power_mode_start_time = None
            self.power_mode_percent = 0.0

        return
