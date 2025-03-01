from micropython import const

from kmk.keys import KC
from kmk.keys import Key, make_argumented_key
from kmk.modules import Module
from kmk.utils import Debug

debug = Debug(__name__)


class ModeKey(Key):
    def __init__(self, modes={0: KC.NO}, fallback_key: Key = KC.NO, **kwargs):
        super().__init__(**kwargs)
        self.modes = modes
        self.fallback_key = fallback_key


class SetModeKey(Key):
    def __init__(self, mode: int, **kwargs):
        super().__init__(**kwargs)
        self.mode = mode


class Mode(Module):
    mode = 0

    def __init__(self, initial_mode=0):
        self.mode = initial_mode

        make_argumented_key(
            names=('MODE_DO',),
            constructor=ModeKey,
            on_press=self.mk_pressed,
            on_release=self.mk_released,
        )

        make_argumented_key(
            names=('MODE_SET',),
            constructor=SetModeKey,
            on_press=self.sm_pressed,
            on_release=self.sm_released,
        )

    def during_bootup(self, keyboard):
        return

    def before_matrix_scan(self, keyboard):
        return

    def after_matrix_scan(self, keyboard):
        return

    def process_key(self, keyboard, key, is_pressed, int_coord):
        return key

    def before_hid_send(self, keyboard):
        return

    def after_hid_send(self, keyboard):
        return

    def on_powersave_enable(self, keyboard):
        return

    def on_powersave_disable(self, keyboard):
        return

    def mk_pressed(self, key: ModeKey, keyboard, *args, **kwargs):
        cur_key: Key = key.modes.get(self.mode, key.fallback_key)
        if cur_key is not None:
            return cur_key.on_press(keyboard, args[1])
        return keyboard

    def mk_released(self, key: ModeKey, keyboard, *args, **kwargs):
        cur_key: Key = key.modes.get(self.mode, key.fallback_key)
        if cur_key is not None:
            return cur_key.on_release(keyboard, args[1])
        return keyboard

    def sm_pressed(self, key: SetModeKey, keyboard, *args):
        self.mode = key.mode
        return keyboard

    def sm_released(self, key, keyboard, *args):
        return keyboard
