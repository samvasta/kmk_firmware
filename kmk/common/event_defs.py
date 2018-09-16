from micropython import const

KEY_UP_EVENT = const(1)
KEY_DOWN_EVENT = const(2)
INIT_FIRMWARE_EVENT = const(3)


def init_firmware(keymap, row_pins, col_pins, diode_orientation):
    return {
        'type': INIT_FIRMWARE_EVENT,
        'keymap': keymap,
        'row_pins': row_pins,
        'col_pins': col_pins,
        'diode_orientation': diode_orientation,
    }


def key_up_event(keycode, row, col):
    return {
        'type': KEY_UP_EVENT,
        'keycode': keycode,
        'row': row,
        'col': col,
    }


def key_down_event(keycode, row, col):
    return {
        'type': KEY_DOWN_EVENT,
        'keycode': keycode,
        'row': row,
        'col': col,
    }