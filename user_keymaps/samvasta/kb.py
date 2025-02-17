import board
import busio

from adafruit_mcp230xx.mcp23017 import MCP23017

# from kmk.hid import HIDModes
from kmk.keys import KC
from kmk.kmk_keyboard import KMKKeyboard as KMKKeyboard

from kmk.scanners import DiodeOrientation

from kmk.scanners.digitalio import MatrixScanner as DigitalIOMatrixScanner
import digitalio


FINGER_COLS = 6
ROWS = 3
THUMB_COLS = 3
THUMB_ROWS = 1

KEYS_PER_HAND = FINGER_COLS * ROWS + THUMB_COLS * THUMB_ROWS


MCP_COLS = [1, 2, 3, 4, 5, 6, 0]
MCP_ROWS = [8, 9, 10]


i2c = busio.I2C(scl=board.IO12, sda=board.IO13, frequency=100000)
mcp_r = MCP23017(i2c, address=0x20)
mcp_l = MCP23017(i2c, address=0x21)


class Input(KMKKeyboard):
    def __init__(self):
        super().__init__()
        # create and register the scanner
        self.matrix = [
            DigitalIOMatrixScanner(
                cols=[mcp_l.get_pin(col_pin) for col_pin in MCP_COLS],
                rows=[mcp_l.get_pin(row_pin) for row_pin in MCP_ROWS],
                diode_orientation=DiodeOrientation.COL2ROW,
                pull=digitalio.Pull.UP,
            ),
            DigitalIOMatrixScanner(
                cols=[mcp_r.get_pin(col_pin) for col_pin in MCP_COLS],
                rows=[mcp_r.get_pin(row_pin) for row_pin in MCP_ROWS],
                diode_orientation=DiodeOrientation.COL2ROW,
                pull=digitalio.Pull.UP,
                offset=KEYS_PER_HAND,
            ),
        ]

        # fmt: off
        self.coord_mapping = [
    #Cols:  5    4    3    2    1    0     6 (thumbs) 6     0,   1,   2,   3,   4,   5
            5,   4,   3,   2,   1,   0,    6,        27,   21,  22,  23,  24,  25,  26,
           12,  11,  10,   9,   8,   7,   13,        34,   28,  29,  30,  31,  32,  33,
           19,  18,  17,  16,  15,  14,   20,        41,   35,  36,  37,  38,  39,  40,
        ]
        # fmt: on
