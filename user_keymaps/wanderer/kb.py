import board
import busio

from adafruit_mcp230xx.mcp23017 import MCP23017

# from kmk.hid import HIDModes
from kmk.keys import KC
from kmk.kmk_keyboard import KMKKeyboard as KMKKeyboard

from kmk.scanners import DiodeOrientation

from kmk.scanners.digitalio import MatrixScanner as DigitalIOMatrixScanner
import digitalio


i2c = busio.I2C(scl=board.GP13, sda=board.GP12, frequency=100000)
mcp_r = MCP23017(i2c, address=0x20)


MCP_COLS = [5, 4, 3, 2, 1, 0] # pinky -> index
MCP_ROWS = [7, 8, 9, 10] # top -> thumbs


class Input(KMKKeyboard):
    def __init__(self):
        super().__init__()
        # create and register the scanner
        self.matrix = [
            DigitalIOMatrixScanner(
                cols=[
                    board.GP14,  # pinky 1
                    board.GP15,  # pinky 2
                    board.GP26,  # ring
                    board.GP27,  # middle
                    board.GP28,  # index
                    board.GP29,  # index
                ],
                rows=[
                    board.GP9,  # top
                    board.GP10, # middle
                    board.GP11, # bottom
                    board.GP8   # thumbs
                ],
                diode_orientation=DiodeOrientation.ROW2COL,
                pull=digitalio.Pull.UP,
            ),
            DigitalIOMatrixScanner(
                cols=[mcp_r.get_pin(col_pin) for col_pin in MCP_COLS],
                rows=[mcp_r.get_pin(row_pin) for row_pin in MCP_ROWS],
                diode_orientation=DiodeOrientation.ROW2COL,
                pull=digitalio.Pull.UP,
                offset=22,
            ),
        ]

        # fmt: off
        self.coord_mapping = [
             0,  1,  2,  3,  4,  5,             27, 26, 25, 24, 23, 22,
             6,  7,  8,  9, 10, 11,             33, 32, 31, 30, 29, 28,
            12, 13, 14, 15, 16, 17,             39, 38, 37, 36, 35, 34,
                    18, 19, 20, 21,             43, 42, 41, 40 
        ]
        # fmt: on
