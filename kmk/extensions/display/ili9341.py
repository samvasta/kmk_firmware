import busio

import adafruit_ili9341  # Display-specific library
import displayio

from . import DisplayBase

# Required to initialize this display
displayio.release_displays()


class ILI9341(DisplayBase):
    def __init__(
        self,
        spi=None,
        sck=None,
        mosi=None,
        command=None,
        chip_select=None,
        reset=None,
        baudrate=1000000,
    ):
        self.command = command
        self.chip_select = chip_select
        self.reset = reset
        self.baudrate = baudrate
        # spi initialization
        self.spi = spi
        if self.spi is None:
            self.spi = busio.SPI(sck, mosi)

    def during_bootup(self, width, height, rotation):
        self.display = adafruit_ili9341.ILI9341(
            displayio.FourWire(
                self.spi,
                command=self.command,
                chip_select=self.chip_select,
                reset=self.reset,
                baudrate=self.baudrate,
            ),
            width=width,
            height=height,
            rotation=rotation,
        )

        return self.display

    def deinit(self):
        self.spi.deinit()
