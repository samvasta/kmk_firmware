import board
import busio
import displayio
from kmk.scheduler import create_task
from enum import Enum

from kmk.extensions.display import Display

from kmk.extensions.display.ili9341 import ILI9341
from user_keymaps.samvasta.weather import AirQuality, Weather

from adafruit_display_text import label

displayio.release_displays()

spi = busio.SPI(clock=board.GP2, MOSI=board.GP3, MISO=board.GP0)

tft_cs = board.GP1
tft_dc = board.GP8
tft_reset = board.GP7

# Replace command, chip_select, and reset according to your hardware configuration.
driver = ILI9341(
    # Mandatory:
    spi=spi,
    command=tft_dc,  # DC
    chip_select=tft_cs,  # CS_LCD
    reset=tft_reset,
)


class Icon(Enum):
    CHEVRON_DOWN = '0'
    CHEVRON_LEFT = '1'
    CHEVRON_RIGHT = '2'
    CHEVRON_UP = '3'
    ARROW_DOWN = '4'
    ARROW_LEFT = '5'
    ARROW_RIGHT = '6'
    ARROW_UP = '7'
    CHECK = '8'
    CLOSE = '9'

    WIFI = 'A'
    WIFI_OFF = 'B'
    HOME = 'C'
    CALCULATOR = 'D'
    DICTIONARY = 'E'
    CLOCK = 'F'
    CHART = 'G'
    KEYBOARD = 'H'
    LAYERS = 'I'
    SHIFT_LOCK = 'J'
    SHIFT_LOCK_OFF = 'K'
    APPLE_ON = 'L'
    APPLE_OFF = 'M'
    RECORD = 'N'

    SPOTIFY = 'Q'
    SONG_NAME = 'R'
    SONG_ARTIST = 'S'
    SONG_ALBUM = 'T'

    COMMAND = 'W'
    SHIFT = 'X'
    ALT_OPTION = 'Y'
    CONTROL = 'Z'

    SUN = 'a'
    PART_CLOUDY = 'b'
    MOON = 'c'
    MOON_PART_CLOUDY = 'd'
    CLOUD = 'e'
    RAIN = 'f'
    THUNDERSTORM = 'g'
    FOG = 'h'
    SNOW = 'i'
    HAIL = 'j'
    MIX_STORM = 'k'
    SNOWFLAKE = 'l'
    TEMP_0 = 'm'
    TEMP_1 = 'n'
    TEMP_2 = 'o'
    TEMP_3 = 'p'
    TEMP_4 = 'q'
    WIND = 'r'
    AIR_QUALITY = 's'
    AIR = 't'
    HUMIDITY_PERCENT = 'u'


class AnimatedDisplay(Display):
    update_count = 0
    frame_count = 0

    def __init__(
        self, display=None, sleep_command=None, wake_command=None, refresh_rate=5
    ):
        super().__init__(
            display=display, sleep_command=sleep_command, wake_command=wake_command
        )
        self.refresh_rate = refresh_rate
        self.weather = Weather()
        self.air_quality = AirQuality()

    def during_bootup(self, width, height, rotation):
        super().during_bootup(width, height, rotation)
        self.splash = displayio.Group()
        self.display.root_group = self.splash
        self._task = create_task(self.animate, period_ms=(1000 // self.refresh_rate))
        self.weather.create_task()
        self.air_quality.create_task()

    def before_matrix_scan(self, sandbox):
        '''override default rendering hook so it doesn't call super().render()'''
        if self.dim_period.tick():
            self.dim()
        self.update_count = self.update_count + 1
        self.sandbox = sandbox

    def animate(self, sandbox):
        self.frame_count = self.frame_count + 1

        self.splash = displayio.Group()

        self.splash.append(
            label.Label(
                terminalio.FONT,
                text=f"AQI: {self.air_quality.aqi()}",
                color=0xFFFFFF,
                background_color=0x000000,
                anchored_position=(0, 0),
            )
        )

        self.splash.append(
            label.Label(
                terminalio.FONT,
                text=f"Weather: {self.weather.describe_weather()}",
                color=0xFFFFFF,
                background_color=0x000000,
                anchored_position=(0, 32),
            )
        )

        self.display.root_group = self.splash

        # for entry in self.entries:
        #     if entry.layer != layer and entry.layer is not None:
        #         continue
        #     if isinstance(entry, TextEntry):
        #         splash.append(
        #             label.Label(
        #                 terminalio.FONT,
        #                 text=entry.text,
        #                 color=entry.color,
        #                 background_color=entry.background_color,
        #                 anchor_point=entry.anchor_point,
        #                 anchored_position=entry.anchored_position,
        #                 label_direction=entry.direction,
        #                 line_spacing=entry.line_spacing,
        #                 padding_left=1,
        #             )
        #         )
        #     elif isinstance(entry, ImageEntry):
        #         splash.append(
        #             displayio.TileGrid(
        #                 entry.image,
        #                 pixel_shader=entry.image.pixel_shader,
        #                 x=entry.x,
        #                 y=entry.y,
        #             )
        #         )


tft_display = AnimatedDisplay(
    # Mandatory:
    display=driver,
    # Optional:
    width=320,  # screen size
    height=240,  # screen size
    flip=False,  # flips your display content
    flip_left=False,  # flips your display content on left side split
    flip_right=False,  # flips your display content on right side split
    brightness=0.8,  # initial screen brightness level
    brightness_step=0.1,  # used for brightness increase/decrease keycodes
    dim_time=20,  # time in seconds to reduce screen brightness
    dim_target=0.1,  # set level for brightness decrease
    off_time=60,  # time in seconds to turn off screen
    powersave_dim_time=10,  # time in seconds to reduce screen brightness
    powersave_dim_target=0.1,  # set level for brightness decrease
    powersave_off_time=30,  # time in seconds to turn off screen
)
