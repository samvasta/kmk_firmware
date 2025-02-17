# from kmk.hid import HIDModes
from kmk.keys import KC
from kb import Input
from kmk.modules.layers import Layers
from kmk.utils import Debug

# from tft import tft_display


DEBUG_ENABLE = True

debug = Debug(__name__)

keyboard = Input()
keyboard.modules.append(Layers())

keyboard.debug_enabled = DEBUG_ENABLE


# rgb = RGB(
#     pixel_pin=board.GP14,
#     num_pixels=8,
#     val_limit=100,
#     hue_default=0,
#     sat_default=100,
#     val_default=100,
#     hue_step=5,
#     sat_step=5,
#     val_step=5,
#     animation_speed=1,
#     breathe_center=1,  # 1.0-2.7
#     knight_effect_length=3,
#     animation_mode=AnimationModes.STATIC,
#     reverse_animation=False,
#     refresh_rate=60,
# )
# keyboard.extensions.append(rgb)

# keyboard.extensions.append(tft_display)

L1 = KC.MO(1)
L2 = KC.MO(2)
L3 = KC.MO(3)
L4 = KC.MO(4)

# fmt:off
keyboard.keymap = [
     [
#Cols:  5    4    3    2    1    0     6 (thumbs) 6     0,   1,   2,   3,   4,   5
       KC.ESC,  KC.Q,  KC.W,  KC.E,  KC.R,  KC.T,    KC.SPC,    KC.RSFT,  KC.Y, KC.U,  KC.I,    KC.O,    KC.P,    KC.BSPC,
       KC.TAB,  KC.A,  KC.S,  KC.D,  KC.F,  KC.G,    L1,        L2,       KC.H, KC.J,  KC.K,    KC.L,    KC.SCLN, KC.ENT,
       KC.LCTL, KC.Z,  KC.X,  KC.C,  KC.V,  KC.B,    L3,        L4,       KC.N, KC.M,  KC.COMM, KC.DOT,  KC.SLSH, KC.RALT,
    ]
]
# fmt:on

if __name__ == "__main__":
    try:
        keyboard.go()
    except Exception as e:
        debug(e)