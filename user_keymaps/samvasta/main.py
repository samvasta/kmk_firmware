# from kmk.hid import HIDModes
from kmk.extensions.media_keys import MediaKeys
from kmk.keys import KC
from kb import Input
from kmk.modules.layers import Layers
from kmk.modules.magickey import MagicKey, str_to_keys
from kmk.modules.string_substitution import str_to_phrase
from kmk.utils import Debug

from kmk.modules.mode import Mode
from tft import AnimatedDisplay

# from tft import tft_display
DEBUG_ENABLE = True

debug = Debug(__name__)

keyboard = Input()
# fmt:off
combo_layers = {
    (1, 2): 5, # Media Layer
    (3, 4): 6  # System Layer
}
# fmt:on
keyboard.modules.append(Layers(combo_layers))
MODE_WIN_LIN = 0
MODE_MAC = 1
keyboard.modules.append(Mode(MODE_WIN_LIN))

keyboard.extensions.append(MediaKeys())
keyboard.modules.append(MagicKey())
# keyboard.extensions.append(AnimatedDisplay())


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

L1 = KC.MO(1)
L2 = KC.MO(2)
L3 = KC.MO(3)
L4 = KC.MO(4)


MAGIC = KC.MAGIC(
    {
        # Single letters
        "a": [KC.O],
        "b": str_to_keys("efore"),
        "c": str_to_keys("kly"),
        "d": [KC.Y],
        "e": [KC.U],
        # "f" same finger as magic, no use
        "g": [KC.Y],
        # "h" same finger as magic, no use
        "i": str_to_keys("on"),
        "j": str_to_keys("ust"),
        "k": [KC.S],
        "l": [KC.Y],
        "m": str_to_keys("ent"),
        "n": str_to_keys("ion"),
        "o": [KC.A],
        "p": [KC.Y],
        # "q" same finger as magic, no use
        "r": [KC.L],
        "s": [KC.K],
        "t": str_to_keys("ment"),
        "u": [KC.E],
        "v": str_to_keys("er"),
        "w": str_to_keys("hich"),
        "x": str_to_keys("es"),
        "y": str_to_keys("ou"),
        # "z" same finger as magic, no use
        # Word completions
        "con": str_to_keys("figuration"),
        "ob": str_to_keys("ject"),
        "play": str_to_keys("book"),
        "wor": str_to_keys("kflow"),
        "wo": str_to_keys("uld"),
        "be": str_to_keys("cause"),
    },
    KC.DOT,
)

REPEAT = KC.MAGIC(
    {
        "0": [KC.N0],
        "1": [KC.N1],
        "2": [KC.N2],
        "3": [KC.N3],
        "4": [KC.N4],
        "5": [KC.N5],
        "6": [KC.N6],
        "7": [KC.N7],
        "8": [KC.N8],
        "9": [KC.N9],
        "a": [KC.N, KC.D],  # and
        "b": [KC.B],
        "c": [KC.Y],  # y
        "d": [KC.D],
        "e": [KC.E],
        "f": [KC.O],  # fo
        "g": [KC.G],
        "h": [KC.H],
        "i": [KC.N, KC.G],  # ing
        "j": [KC.J],
        "k": [KC.K],
        "l": [KC.L],
        "m": [KC.M],
        "n": [KC.N],
        "o": [KC.F],  # of
        "p": [KC.P],
        "q": [KC.Q],
        "r": [KC.R],
        "s": [KC.S],
        "t": [KC.T],
        "u": [KC.U],
        "v": [KC.V],
        "w": [KC.W],
        "x": [KC.X],
        "y": [KC.Y],
        "z": [KC.Z],
    },
    KC.NO,
)


# fmt:off
keyboard.keymap = [
    [
#    ┌────────┬────────┬─────────┬────────┬────────┬────────┐                       ┌────────┬────────┬────────┬────────┬────────┬────────┐
#    │  ESC   │    Z   │   M     │   L    │   C    │   B    │                       │    F   │   H    │   O    │    U   │   J    │ BKSPC  │
#    ├────────┼────────┼─────────┼────────┼────────┼────────┤                       ├────────┼────────┼────────┼────────┼────────┼────────┤
#    │  TAB   │    S   │   T     │   R    │   D    │   Y    │                       │   ⭐   │   N    │   A    │    E   │   I    │ ENTER  │
#    ├────────┼────────┼─────────┼────────┼────────┼────────┤                       ├────────┼────────┼────────┼────────┼────────┼────────┤
#    │Ctrl/Cmd│    V   │   K     │   W    │   G    │   Q    │                       │    X   │   P    │   ;    │    ,   │   .    │Ctrl/Cmd│
#    └────────┴────────┴─────────┴────────┴────────┴────────┘                       └────────┴────────┴────────┴────────┴────────┴────────┘
       KC.ESC,   KC.Z,    KC.M,     KC.L,    KC.C,    KC.B,    KC.SPC,    KC.RSFT,     KC.F,     KC.H,  KC.O,    KC.U,    KC.J,    KC.BSPC,
       KC.TAB,   KC.S,    KC.T,     KC.R,    KC.D,    KC.Y,    L1,        L2,          MAGIC,    KC.N,  KC.A,    KC.E,    KC.I,    KC.ENT,
       CTRL_CMD, KC.V,    KC.K,     KC.W,    KC.G,    KC.Q,    L3,        L4,          KC.X,     KC.P,  KC.SCLN, KC.COMM, KC.DOT,  ALT_CTRL,
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
       KC.NO,  S(KC.GRV),  KC.BSPC, KC.UP,   KC.DEL,   CTRL_ALT_K,    KC.SPC,    KC.RSFT,    KC.NO, KC.HOME, UNDO,    REDO,     SCRNSHOT, KC.NO,
       KC.NO,  S(KC.TAB),  KC.LEFT, KC.DOWN, KC.RIGHT, CTRL_ALT_J,    L1,        L2,         KC.NO, KC.END,  ALT_CMD, CTRL_ALT, KC.LSFT,  KC.NO,
       KC.NO,  KC.NO,      CUT,     COPY,    PASTE,    KC.NO,         L3,        L4,         KC.NO, KC.NO,   KC.NO,   KC.NO,    KC.NO,    KC.NO,
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
       KC.NO,  KC.CIRC,  KC.BSLS,   KC.ASTR,  KC.COLN, KC.AMPR,    KC.SPC,    KC.RSFT,    KC.GRV,  KC.DLR,  KC.LBRC, KC.RBRC, KC.PERC, KC.NO,
       KC.NO,  KC.EXLM,  KC.MINUS,  KC.PLUS,  KC.EQL,  KC.PIPE,    L1,        L2,         KC.QUES, KC.LPRN, KC.LCBR, KC.RCBR, KC.RPRN, KC.NO,
       KC.NO,  KC.TILD,  KC.POUND,  KC.LABK,  KC.RABK, KC.AT,      L3,        L4,         KC.DOT,  KC.QUOT, KC.DQT,  KC.SLSH, KC.COMM, KC.NO,
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
       KC.NO,  KC.DLR, KC.N7,  KC.N8,  KC.N9,  KC.PLUS,   KC.SPC,    KC.RSFT,    KC.DLR, KC.N7,  KC.N8, KC.N9,  KC.PLUS,  KC.NO,
       KC.NO,  KC.DOT, KC.N4,  KC.N5,  KC.N6,  KC.EQL,    L1,        L2,         KC.DOT, KC.N4,  KC.N5, KC.N6,  KC.EQL,   KC.NO,
       KC.NO,  KC.N0,  KC.N1,  KC.N2,  KC.N3,  KC.MINUS,  L3,        L4,         KC.N0,  KC.N1,  KC.N2, KC.N3,  KC.MINUS, KC.NO,
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
       KC.NO,  KC.F1,  KC.F2,  KC.F3,  KC.F4,  KC.NO,    KC.SPC,    KC.RSFT,    KC.NO, KC.F1,  KC.F2,  KC.F3,  KC.F4,  KC.NO,
       KC.NO,  KC.F5,  KC.F6,  KC.F7,  KC.F8,  KC.NO,    L1,        L2,         KC.NO, KC.F5,  KC.F6,  KC.F7,  KC.F8,  KC.NO,
       KC.NO,  KC.F9,  KC.F10, KC.F11, KC.F12, KC.NO,    L3,        L4,         KC.NO, KC.F9,  KC.F10, KC.F11, KC.F12, KC.NO,
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
       KC.NO,  KC.NO,  KC.NO,  KC.NO, KC.VOLD, KC.VOLU,      KC.SPC,    KC.RSFT,    KC.VOLD, KC.VOLU,  KC.NO, KC.NO,  KC.NO,  KC.NO,
       KC.NO,  KC.NO,  KC.NO,  KC.NO, KC.MUTE, KC.MPLY,      L1,        L2,         KC.MUTE, KC.MPLY,  KC.NO, KC.NO,  KC.NO,  KC.NO,
       KC.NO,  KC.NO,  KC.NO,  KC.NO, KC.MPRV, KC.MNXT,      L3,        L4,         KC.MPRV, KC.MNXT,  KC.NO, KC.NO,  KC.NO,  KC.NO,
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
       KC.NO,  KC.NO,  KC.NO,  KC.NO, KC.NO, KC.NO,                          KC.SPC,    KC.RSFT,    KC.NO, KC.NO,  KC.NO, KC.NO,  KC.NO,  KC.NO,
       KC.NO,  KC.NO,  KC.NO,  KC.NO, KC.MODE_SET(MODE_WIN_LIN), KC.NO,      L1,        L2,         KC.NO, KC.MODE_SET(MODE_MAC),  KC.NO, KC.NO,  KC.NO,  KC.NO,
       KC.NO,  KC.NO,  KC.NO,  KC.NO, KC.NO, KC.NO,                          L3,        L4,         KC.NO, KC.NO,  KC.NO, KC.NO,  KC.NO,  KC.NO,
    ],
]
# fmt:on

if __name__ == "__main__":
    try:
        keyboard.go()
    except Exception as e:
        debug(e)
