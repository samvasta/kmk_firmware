# from kmk.hid import HIDModes
from kmk.extensions.media_keys import MediaKeys
from kmk.keys import KC
from kb import Input
from kmk.modules.layers import Layers
from kmk.utils import Debug

from kmk.modules.mode import Mode
from tft import AnimatedDisplay

# from tft import tft_display
DEBUG_ENABLE = True

debug = Debug(__name__)

keyboard = Input()
keyboard.modules.append(Layers())
MODE_WIN_LIN = 0
MODE_MAC = 1
keyboard.modules.append(Mode(MODE_WIN_LIN))

keyboard.extensions.append(MediaKeys())
keyboard.extensions.append(AnimatedDisplay())

keyboard.debug_enabled = DEBUG_ENABLE

S = KC.LSFT
CTL = KC.LCTL
CMD = KC.LGUI
ALT = KC.LALT


CTRL_CMD = KC.MODE_DO(
    {
        MODE_WIN_LIN: KC.LCTL,
        MODE_MAC: KC.LGUI,
    },
    KC.LCTL,
)
ALT_CMD = KC.MODE_DO(
    {
        MODE_WIN_LIN: KC.LALT,
        MODE_MAC: KC.LGUI,
    },
    KC.LALT,
)
ALT_CTRL = KC.MODE_DO(
    {
        MODE_WIN_LIN: KC.LALT,
        MODE_MAC: KC.LCTL,
    },
    KC.LALT,
)
CTRL_ALT = KC.MODE_DO(
    {
        MODE_WIN_LIN: KC.LCTL,
        MODE_MAC: KC.LALT,
    },
    KC.LCTL,
)
CTRL_ALT_J = KC.MODE_DO(
    {
        MODE_WIN_LIN: CTL(KC.J),
        MODE_MAC: ALT(KC.J),
    },
    KC.NO,
)
CTRL_ALT_K = KC.MODE_DO(
    {
        MODE_WIN_LIN: CTL(KC.K),
        MODE_MAC: ALT(KC.K),
    },
    KC.NO,
)

CUT = KC.MODE_DO(
    {
        MODE_WIN_LIN: CTL(KC.X),
        MODE_MAC: CMD(KC.X),
    },
    KC.NO,
)
COPY = KC.MODE_DO(
    {
        MODE_WIN_LIN: CTL(KC.C),
        MODE_MAC: CMD(KC.C),
    },
    KC.NO,
)
PASTE = KC.MODE_DO(
    {
        MODE_WIN_LIN: CTL(KC.V),
        MODE_MAC: CMD(KC.V),
    },
    KC.NO,
)
UNDO = KC.MODE_DO(
    {
        MODE_WIN_LIN: CTL(KC.Z),
        MODE_MAC: CMD(KC.Z),
    },
    KC.NO,
)
REDO = KC.MODE_DO(
    {
        MODE_WIN_LIN: CTL(KC.Y),
        MODE_MAC: CMD(KC.Y),
    },
    KC.NO,
)
SCRNSHOT = KC.MODE_DO(
    {
        MODE_WIN_LIN: KC.PSCR,
        MODE_MAC: S(CTL(CMD(KC.N4))),
    },
    KC.NO,
)


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
combo_layers = {
    (1, 2): 5, # Media Layer
    (3, 4): 6  # System Layer
}
# fmt:on
keyboard.modules.append(Layers(combo_layers))

# fmt:off
keyboard.keymap = [
    [
#    ┌────────┬────────┬─────────┬────────┬────────┬────────┐             ┌────────┬────────┬────────┬────────┬────────┬────────┐
#    │  ESC   │    Z   │   M     │   L    │   C    │   B    │             │    F   │   H    │   O    │    U   │   J    │ BKSPC  │
#    ├────────┼────────┼─────────┼────────┼────────┼────────┤             ├────────┼────────┼────────┼────────┼────────┼────────┤
#    │  TAB   │    S   │   T     │   R    │   D    │   Y    │             │    .   │   N    │   A    │    E   │   I    │ ENTER  │
#    ├────────┼────────┼─────────┼────────┼────────┼────────┤             ├────────┼────────┼────────┼────────┼────────┼────────┤
#    │Ctrl/Cmd│    V   │   K     │   W    │   G    │   Q    │             │    X   │   P    │   ;    │   '    │   ,    │Ctrl/Cmd│
#    └────────┴────────┴─────────┴────────┴────────┴────────┘             └────────┴────────┴────────┴────────┴────────┴────────┘
       KC.ESC,   KC.Z,  KC.M,  KC.L,  KC.C,  KC.B,    KC.SPC,    KC.RSFT,  KC.F,   KC.H,  KC.O,    KC.U,    KC.J,    KC.BSPC,
       KC.TAB,   KC.S,  KC.T,  KC.R,  KC.D,  KC.Y,    L1,        L2,       KC.DOT, KC.N,  KC.A,    KC.E,    KC.I,    KC.ENT,
       CTRL_CMD, KC.V,  KC.K,  KC.W,  KC.G,  KC.Q,    L3,        L4,       KC.X,   KC.P,  KC.SCLN, KC.QUOT, KC.COMM, ALT_CTRL,
    ],
    [
#    Navigation
#    ┌────────┬─────────┬─────────┬─────────┬─────────┬─────────┐                         ┌────────┬─────────┬─────────┬─────────┬─────────┬────────┐
#    │        │ shift+` │backspace│   UP    │   DEL   │ctl/alt+K│                         │        │   HOME  │   undo  │   redo  │scrnshot │        │
#    ├────────┼─────────┼─────────┼─────────┼─────────┼─────────┤                         ├────────┼─────────┼─────────┼─────────┼─────────┼────────┤
#    │        |shift+tab│   left  │  down   │  right  │ctl/alt+J│                         │        │   END   │ alt/cmd │ctrl/alt │  shift  │        │
#    ├────────┼─────────┼─────────┼─────────┼─────────┼─────────┤                         ├────────┼─────────┼─────────┼─────────┼─────────┼────────┤
#    │        │         │   CUT   │  COPY   │  PASTE  │         │                         │        │         │         │         │         │        │
#    └────────┴─────────┴─────────┴─────────┴─────────┴─────────┘                         └────────┴─────────┴─────────┴─────────┴─────────┴────────┘
       KC.NO,  S(KC.GRV),  KC.BSPC, KC.UP,   KC.DEL,   CTRL_ALT_K,    KC.NO,     KC.NO,    KC.NO, KC.HOME, UNDO,    REDO,     SCRNSHOT, KC.NO,
       KC.NO,  S(KC.TAB),  KC.LEFT, KC.DOWN, KC.RIGHT, CTRL_ALT_J,    KC.NO,     KC.NO,    KC.NO, KC.END,  ALT_CMD, CTRL_ALT, KC.LSFT,  KC.NO,
       KC.NO,  KC.NO,      CUT,     COPY,    PASTE,    KC.NO,         KC.NO,     KC.NO,    KC.NO, KC.NO,   KC.NO,   KC.NO,    KC.NO,    KC.NO,
    ],
    [
#    Symbols
#    ┌────────┬────────┬─────────┬────────┬────────┬────────┐                           ┌────────┬────────┬────────┬────────┬────────┬────────┐
#    │        │    ^   │   \     │   *    │   :    │   &    │                           │    `   │   $    │   [    │    ]   │   %    │        │
#    ├────────┼────────┼─────────┼────────┼────────┼────────┤                           ├────────┼────────┼────────┼────────┼────────┼────────┤
#    │        │    !   │   -     │   +    │   =    │   |    │                           │    ?   │   (    │   {    │    }   │   )    │        │
#    ├────────┼────────┼─────────┼────────┼────────┼────────┤                           ├────────┼────────┼────────┼────────┼────────┼────────┤
#    │        │    ~   │   #     │   <    │   >    │   @    │                           │    .   │   '    │   "    │    /   │   ,    │        │
#    └────────┴────────┴─────────┴────────┴────────┴────────┘                           └────────┴────────┴────────┴────────┴────────┴────────┘
       KC.NO,  KC.CIRC,  KC.BSLS,   KC.ASTR,  KC.COLN, KC.AMPR,    KC.NO,     KC.NO,    KC.GRV,  KC.DLR,  KC.LBRC, KC.RBRC, KC.PERC, KC.NO,
       KC.NO,  KC.EXLM,  KC.MINUS,  KC.PLUS,  KC.EQL,  KC.PIPE,    KC.NO,     KC.NO,    KC.QUES, KC.LPRN, KC.LCBR, KC.RCBR, KC.RPRN, KC.NO,
       KC.NO,  KC.TILD,  KC.POUND,  KC.LABK,  KC.RABK, KC.AT,      KC.NO,     KC.NO,    KC.DOT,  KC.QUOT, KC.DQT,  KC.SLSH, KC.COMM, KC.NO,
    ],
    [
#    Numbers
#    ┌────────┬────────┬─────────┬────────┬────────┬────────┐                ┌────────┬────────┬────────┬────────┬────────┬────────┐
#    │        │    $   │    7    │   8    │    9   │   +    │                │   $    │   7    │   8    │   9    │   +    │        │
#    ├────────┼────────┼─────────┼────────┼────────┼────────┤                ├────────┼────────┼────────┼────────┼────────┤────────┤
#    │        │    .   │    4    │   5    │    6   │   =    │                │   .    │   4    │   5    │   6    │   =    │        │
#    ├────────┼────────┼─────────┼────────┼────────┼────────┤                ├────────┼────────┼────────┼────────┼────────┤────────┤
#    │        │    0   │    1    │   2    │    3   │   -    │                │   0    │   1    │   2    │   3    │   -    │        │
#    └────────┴────────┴─────────┴────────┴────────┴────────┘                └────────┴────────┴────────┴────────┴────────┴────────┘
       KC.NO,  KC.DLR, KC.N7,  KC.N8,  KC.N9,  KC.PLUS,   KC.NO,     KC.NO,    KC.DLR, KC.N7,  KC.N8, KC.N9,  KC.PLUS,  KC.NO,
       KC.NO,  KC.DOT, KC.N4,  KC.N5,  KC.N6,  KC.EQL,    KC.NO,     KC.NO,    KC.DOT, KC.N4,  KC.N5, KC.N6,  KC.EQL,   KC.NO,
       KC.NO,  KC.N0,  KC.N1,  KC.N2,  KC.N3,  KC.MINUS,  KC.NO,     KC.NO,    KC.N0,  KC.N1,  KC.N2, KC.N3,  KC.MINUS, KC.NO,
    ],
    [
#    Function Keys
#    ┌────────┬────────┬────────┬────────┬────────┬────────┐                 ┌────────┬────────┬────────┬────────┬────────┬────────┐
#    │        │   F1   │   F2   │   F3   │   F4   │ XXXXXX │                 │ XXXXXX │   F1   │   F2   │   F3   │   F4   │        │
#    ├────────┼────────┼────────┼────────┼────────┼────────┤                 ├────────┼────────┼────────┼────────┼────────┼────────┤
#    │        │   F5   │   F6   │   F7   │   F8   │ XXXXXX │                 │ XXXXXX │   F5   │   F6   │   F7   │   F8   │        │
#    ├────────┼────────┼────────┼────────┼────────┼────────┤                 ├────────┼────────┼────────┼────────┼────────┼────────┤
#    │        │   F9   │   F10  │   F11  │   F12  │ XXXXXX │                 │ XXXXXX │   F9   │   F10  │   F11  │   F12  │        │
#    └────────┴────────┴────────┴────────┴────────┴────────┘                 └────────┴────────┴────────┴────────┴────────┴────────┘
       KC.NO,  KC.F1,  KC.F2,  KC.F3,  KC.F4,  KC.NO,    KC.NO,     KC.NO,    KC.NO, KC.F1,  KC.F2,  KC.F3,  KC.F4,  KC.NO,
       KC.NO,  KC.F5,  KC.F6,  KC.F7,  KC.F8,  KC.NO,    KC.NO,     KC.NO,    KC.NO, KC.F5,  KC.F6,  KC.F7,  KC.F8,  KC.NO,
       KC.NO,  KC.F9,  KC.F10, KC.F11, KC.F12, KC.NO,    KC.NO,     KC.NO,    KC.NO, KC.F9,  KC.F10, KC.F11, KC.F12, KC.NO,
    ],
    [
#    Media
#    ┌────────┬────────┬─────────┬────────┬────────┬────────┐                     ┌────────┬────────┬────────┬────────┬────────┬────────┐
#    │ XXXXXX │ XXXXXX │ XXXXXXX │ XXXXXX │  VOL-  │  VOL+  │                     │  VOL-  │  VOL+  │ XXXXXX │ XXXXXX │ XXXXXX │ XXXXXX │
#    ├────────┼────────┼─────────┼────────┼────────┼────────┤                     ├────────┼────────┼────────┼────────┼────────┼────────┤
#    │ XXXXXX │ XXXXXX │ XXXXXXX │ XXXXXX │  MUTE  │  > ||  │                     │  MUTE  │  > ||  │ XXXXXX │ XXXXXX │ XXXXXX │ XXXXXX │
#    ├────────┼────────┼─────────┼────────┼────────┼────────┤                     ├────────┼────────┼────────┼────────┼────────┼────────┤
#    │ XXXXXX │ XXXXXX │ XXXXXXX │ XXXXXX │   <<   │   >>   │                     │   <<   │   >>   │ XXXXXX │ XXXXXX │ XXXXXX │ XXXXXX │
#    └────────┴────────┴─────────┴────────┴────────┴────────┘                     └────────┴────────┴────────┴────────┴────────┴────────┘
       KC.NO,  KC.NO,  KC.NO,  KC.NO, KC.VOLD, KC.VOLU,      KC.NO,     KC.NO,    KC.VOLD, KC.VOLU,  KC.NO, KC.NO,  KC.NO,  KC.NO,
       KC.NO,  KC.NO,  KC.NO,  KC.NO, KC.MUTE, KC.MPLY,      KC.NO,     KC.NO,    KC.MUTE, KC.MPLY,  KC.NO, KC.NO,  KC.NO,  KC.NO,
       KC.NO,  KC.NO,  KC.NO,  KC.NO, KC.MPRV, KC.MNXT,      KC.NO,     KC.NO,    KC.MPRV, KC.MNXT,  KC.NO, KC.NO,  KC.NO,  KC.NO,
    ],
    [
#    System
#    ┌────────┬────────┬─────────┬────────┬────────┬────────┐                     ┌────────┬────────┬────────┬────────┬────────┬────────┐
#    │        │        │       X │        │        │        │                     │        │        │        │        │        │        │
#    ├────────┼────────┼─────────┼────────┼────────┼────────┤                     ├────────┼────────┼────────┼────────┼────────┼────────┤
#    │        │        │       X │        │        │        │                     │        │        │        │        │        │        │
#    ├────────┼────────┼─────────┼────────┼────────┼────────┤                     ├────────┼────────┼────────┼────────┼────────┼────────┤
#    │        │        │       X │        │        │        │                     │        │        │        │        │        │        │
#    └────────┴────────┴─────────┴────────┴────────┴────────┘                     └────────┴────────┴────────┴────────┴────────┴────────┘
       KC.NO,  KC.NO,  KC.NO,  KC.NO, KC.NO, KC.NO,      KC.NO,     KC.NO,    KC.NO, KC.NO,  KC.NO, KC.NO,  KC.NO,  KC.NO,
       KC.NO,  KC.NO,  KC.NO,  KC.NO, KC.NO, KC.NO,      KC.NO,     KC.NO,    KC.NO, KC.NO,  KC.NO, KC.NO,  KC.NO,  KC.NO,
       KC.NO,  KC.NO,  KC.NO,  KC.NO, KC.NO, KC.NO,      KC.NO,     KC.NO,    KC.NO, KC.NO,  KC.NO, KC.NO,  KC.NO,  KC.NO,
    ],
]
# fmt:on

if __name__ == "__main__":
    try:
        keyboard.go()
    except Exception as e:
        debug(e)
