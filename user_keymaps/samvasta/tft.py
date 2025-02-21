import board
import busio
import displayio
from kmk.scheduler import create_task

from kmk.extensions.display import Display

from kmk.extensions.display.ili9341 import ILI9341
from api import AuthTokenProvider
from spotify import SpotifyProvider
from weather import AirQuality, Weather

from adafruit_display_text import label

displayio.release_displays()

spi = busio.SPI(clock=board.IO6, MOSI=board.IO4, MISO=board.IO8)

tft_cs = board.IO2
tft_dc = board.IO1
tft_reset = board.IO16

# Replace command, chip_select, and reset according to your hardware configuration.
driver = ILI9341(
    # Mandatory:
    spi=spi,
    command=tft_dc,  # DC
    chip_select=tft_cs,  # CS_LCD
    reset=tft_reset,
)


IconFont = {
    "CHEVRON_DOWN": '0',
    "CHEVRON_LEFT": '1',
    "CHEVRON_RIGHT": '2',
    "CHEVRON_UP": '3',
    "CHECK": '4',
    "CLOSE": '5',
    "TOGGLE_OFF": '6',
    "TOGGLE_ON": '7',
    "WARNING": '8',
    "WIFI": 'A',
    "WIFI_OFF": 'B',
    "HOME": 'C',
    "CALCULATOR": 'D',
    "DICTIONARY": 'E',
    "CLOCK": 'F',
    "CHART": 'G',
    "KEYBOARD": 'H',
    "LAYERS": 'I',
    "SHIFT": 'J',
    "SHIFT_LOCK": 'K',
    "APPLE": 'L',
    "TUX": 'M',
    "CIRCLE": 'N',
    "CIRCLE_CHECK": 'O',
    "SPOTIFY": 'Q',
    "SONG_NAME": 'R',
    "SONG_ARTIST": 'S',
    "SONG_ALBUM": 'T',
    "LIGHTBULB": 'U',
    "COMMAND": 'W',
    "ALT_OPTION": 'X',
    "CONTROL": 'Y',
    "AQ": 'Z',
    "SUN": 'a',
    "PART_CLOUDY": 'b',
    "MOON": 'c',
    "MOON_PART_CLOUDY": 'd',
    "CLOUD": 'e',
    "DRIZZLE": 'f',
    "RAIN": 'g',
    "RAIN_HEAVY": 'h',
    "FOGGY": 'i',
    "HAIL": 'j',
    "SNOW": 'k',
    "LIGHTNING": 'l',
    "SUN_SHOWER": 'm',
    "SNOWFLAKE": 'n',
    "TORNADO": 'o',
    "TEMP_0": 'p',
    "TEMP_1": 'q',
    "TEMP_2": 'r',
    "TEMP_3": 's',
    "TEMP_4": 't',
    "DROP": 'u',
    "DROP_PERCENT": 'v',
    "WIND": 'w',
    "WAVES": 'x',
    "SUNRISE": 'y',
    "SUNSET": 'z',
}


class AnimatedDisplay(Display):
    update_count = 0
    frame_count = 0

    def __init__(self, display=None, refresh_rate=5):
        super().__init__(
            display=display,
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
        self.refresh_rate = refresh_rate

        token_provider = AuthTokenProvider()
        self.weather = Weather(token_provider)
        self.air_quality = AirQuality(token_provider)
        self.spotify = SpotifyProvider(token_provider)

    def during_bootup(self, width, height, rotation):
        super().during_bootup(width, height, rotation)
        self.splash = displayio.Group()
        self.display.root_group = self.splash
        self._task = create_task(self.animate, period_ms=(1000 // self.refresh_rate))
        self.weather.create_task()
        self.air_quality.create_task()
        self.spotify.create_task()

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
