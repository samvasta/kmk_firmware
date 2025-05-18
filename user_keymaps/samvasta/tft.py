import board
import busio
import displayio
import terminalio
from kmk.scheduler import create_task
from kmk.utils import Debug, clamp
from kmk.keys import make_key
from supervisor import ticks_ms
from kmk.kmktime import PeriodicTimer, ticks_diff

from adafruit_bitmap_font import bitmap_font
from displayio import Bitmap


from kmk.extensions import Extension

from kmk.extensions.display.ili9341 import ILI9341
from api import AuthTokenProvider
from spotify import SpotifyProvider
from weather import AirQuality, Weather

from adafruit_display_text import label
from adafruit_display_shapes import rect

debug = Debug(__name__)

displayio.release_displays()

font_bold = bitmap_font.load_font("fonts/luBS14.bdf", Bitmap)
font_reg = bitmap_font.load_font("fonts/luRS14.bdf", Bitmap)
font_icon = bitmap_font.load_font("fonts/custom_icons_24.bdf", Bitmap)

spi = busio.SPI(clock=board.IO6, MOSI=board.IO4, MISO=board.IO5)

tft_cs = board.IO3
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


class AnimatedDisplay(Extension):
    update_count = 0
    frame_count = 0

    def __init__(
        self,
        width=320,
        height=240,
        flip: bool = True,
        flip_left: bool = False,
        flip_right: bool = False,
        brightness=0.8,
        brightness_step=0.1,
        dim_time=20,
        dim_target=0.1,
        off_time=60,
        powersave_dim_time=10,
        powersave_dim_target=0.1,
        powersave_off_time=30,
        refresh_rate=5,
    ):
        self.driver = driver
        self.flip = flip
        self.flip_left = flip_left
        self.flip_right = flip_right
        self.width = width
        self.height = height
        self.prev_layer = None
        self.brightness = brightness
        self.brightness_step = brightness_step
        self.timer_start = ticks_ms()
        self.powersave = False
        self.dim_time_ms = dim_time * 1000
        self.dim_target = dim_target
        self.off_time_ms = off_time * 1000
        self.powersavedim_time_ms = powersave_dim_time * 1000
        self.powersave_dim_target = powersave_dim_target
        self.powersave_off_time_ms = powersave_off_time * 1000
        self.dim_period = PeriodicTimer(50)
        self.split_side = None

        self.allow_dim = False

        make_key(names=('DIS_BRI',), on_press=self.display_brightness_increase)
        make_key(names=('DIS_BRD',), on_press=self.display_brightness_decrease)

        self.refresh_rate = refresh_rate

        token_provider = AuthTokenProvider()
        self.weather = Weather(token_provider)
        self.air_quality = AirQuality(token_provider)
        self.spotify = SpotifyProvider(token_provider)

    def on_runtime_enable(self, sandbox):
        return

    def on_runtime_disable(self, sandbox):
        return

    def during_bootup(self, keyboard):
        self.driver.during_bootup(self.width, self.height, 180 if self.flip else 0)

        if self.allow_dim:
            self.driver.brightness = self.brightness

        self.splash = displayio.Group()
        self.driver.display.root_group = self.splash
        self._task = create_task(self.animate, period_ms=(1000 * self.refresh_rate))
        self.weather.create_task()
        self.air_quality.create_task()
        self.spotify.create_task()

    def before_matrix_scan(self, sandbox):
        '''override default rendering hook so it doesn't call super().render()'''
        if self.dim_period.tick():
            self.dim()
        self.update_count = self.update_count + 1
        self.sandbox = sandbox

    def after_matrix_scan(self, sandbox):
        if sandbox.matrix_update or sandbox.secondary_matrix_update:
            self.timer_start = ticks_ms()

    def before_hid_send(self, sandbox):
        return

    def after_hid_send(self, sandbox):
        return

    def on_powersave_enable(self, sandbox):
        self.powersave = True

    def on_powersave_disable(self, sandbox):
        self.powersave = False

    def deinit(self, sandbox):
        displayio.release_displays()
        self.driver.deinit()

    def display_brightness_increase(self, *args):
        if self.allow_dim:
            self.driver.brightness = clamp(
                self.driver.brightness + self.brightness_step, 0, 1
            )
            self.brightness = self.driver.brightness  # Save current brightness

    def display_brightness_decrease(self, *args):
        if self.allow_dim:
            self.driver.brightness = clamp(
                self.driver.brightness - self.brightness_step, 0, 1
            )
            self.brightness = self.driver.brightness  # Save current brightness

    def dim(self):
        if not self.allow_dim:
            return
        if self.powersave:
            if (
                self.powersave_off_time_ms
                and ticks_diff(ticks_ms(), self.timer_start)
                > self.powersave_off_time_ms
            ):
                self.driver.sleep()

            elif (
                self.powersave_dim_time_ms
                and ticks_diff(ticks_ms(), self.timer_start)
                > self.powersave_dim_time_ms
            ):
                self.driver.brightness = self.powersave_dim_target

            else:
                self.driver.brightness = self.brightness
                self.driver.wake()

        elif (
            self.off_time_ms
            and ticks_diff(ticks_ms(), self.timer_start) > self.off_time_ms
        ):
            self.driver.sleep()

        elif (
            self.dim_time_ms
            and ticks_diff(ticks_ms(), self.timer_start) > self.dim_time_ms
        ):
            self.driver.brightness = self.dim_target

        else:
            self.driver.brightness = self.brightness
            self.driver.wake()

    def animate(self):
        self.frame_count = self.frame_count + 1

        self.splash = displayio.Group()
        self.splash.append(
            rect.Rect(x=0, y=0, width=self.width, height=self.height, fill=0xFFFFFF)
        )

        self.splash.append(
            label.Label(
                font_reg,
                text=f"frame: {self.frame_count}",
                color=0x000000,
                background_color=0xFFFFFF,
                y=15,
            )
        )

        self.splash.append(
            label.Label(
                font_bold,
                text=self.weather.describe_weather(),
                color=0x333333,
                background_color=0xFFFFFF,
                y=50,
                x=32,
            )
        )

        self.splash.append(
            label.Label(
                font_icon,
                text=IconFont['SUN'],
                color=0xBB9911,
                background_color=0xFFFFFF,
                y=50,
                x=8,
            )
        )

        self.splash.append(
            label.Label(
                font_icon,
                text=IconFont['AQ'],
                color=0x2244BB,
                background_color=0xFFFFFF,
                y=135,
                x=8,
            )
        )

        self.splash.append(
            label.Label(
                font_bold,
                text=self.air_quality.aqi(),
                color=0x333333,
                background_color=0xFFFFFF,
                y=135,
                x=32,
            )
        )

        self.splash.append(
            label.Label(
                font_icon,
                text=IconFont['TEMP_2'],
                color=0xBB2244,
                background_color=0xFFFFFF,
                y=100,
                x=8,
            )
        )

        self.splash.append(
            label.Label(
                font_bold,
                text=self.weather.temperature(),
                color=0x333333,
                background_color=0xFFFFFF,
                y=100,
                x=32,
            )
        )

        self.driver.display.root_group = self.splash
