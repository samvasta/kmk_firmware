from kmk.keys import KC, Key, Keyboard, make_argumented_key
from kmk.modules import Module
from kmk.modules.string_substitution import Character, Phrase, str_to_phrase
from kmk.scheduler import create_task
from kmk.utils import Debug
from micropython import const


debug = Debug(__name__)

def str_to_keys(string: str) -> list[Key]:
    keys: list[Key] = []
    for char in string:
        key_code = KC[char.upper()]
        if key_code == KC.NO:
            raise ValueError(f'Invalid character in dictionary: {char}')
        keys.append(key_code)
    return keys

class CharTree:
    _current: Character
    _children: dict[Character, 'CharTree']
    _result: list[Key]

    def __init__(self, current: Character, result: list[Key] = []):
        self._current = current
        self._children = {}
        self._result = result

    def append(self, str: str, result: list[Key] = []):
        self._append(str_to_phrase(str), result)

    def _append(self, str: list[Character], result: list[Key] = []):
        if len(str) == 0:
            if len(result) > 0:
                self._result = result
            return

        next = str[0]
        rest = str[1:]

        if next not in self._children:
            self._children[next] = CharTree(next, result if len(rest) == 0 else [])

        self._children[next]._append(rest, result)

    def match(self, str: list[Character]) -> tuple[int, list[Key]]:
        
        matches: dict[int, list[Key]] = {}

        if bool(self._result) and len(self._result) > 0:
            matches[0] = self._result

        if len(str) == 0:
            return [0, self._result]
        
        for child in self._children.values():
            if str[0] == child._current:
                rest = str[1:]
                child_match = child.match(rest)
                if bool(child_match):
                    matches[child_match[0] + 1] = child_match[1]

        if len(matches) == 0:
            return None

        return max(matches.items(), key=lambda kvp: kvp[0])


class Deque:
    def __init__(self, maxlen=10):
        self._maxlen = maxlen
        self._list = []

    def append(self, item):
        self._list.append(item)
        if len(self._list) > self._maxlen:
            del self._list[: len(self._list) - self._maxlen]

    def clear(self):
        del self._list[:]

    def list(self):
        return self._list

    def __str__(self):
        return str(self._list)

    def __len__(self):
        return len(self._list)


class Magic(Key):
    _match_tree: CharTree
    _default_key = KC.N

    def __init__(self, dictionary, default_key=KC.N, **kwargs):
        super().__init__(**kwargs)
        self._match_tree = CharTree(None)
        for key, value in dictionary.items():
            self._match_tree.append(key, value)
        self._default_key = default_key
        self._task = None


def MagicIter(keyboard, key_list):
    for key in key_list:
        key.on_press(keyboard)
        keyboard._send_hid()
        yield
        key.on_release(keyboard)
        yield


class State:
    LISTENING = const(0)

class SendState(State):
    def __init__(self, keys: list[Key]):
        super().__init__()
        self.index = 0
        self.keys = keys

    def step(self, keyboard):
        keyboard.tap_key(self.keys[self.index])
        self.index += 1

        return self.index >= len(self.keys)


class MagicKey(Module):

    def __init__(self, history_size=10, _make_key=True):
        self._prior_keys = Deque(history_size)
        self.state = State.LISTENING

        if _make_key:
            make_argumented_key(
                names=('MAGIC',),
                constructor=Magic,
                on_press=self.magic_pressed,
                on_release=self.magic_released,
            )

    def during_bootup(self, keyboard):
        pass

    def before_matrix_scan(self, keyboard):
        '''
        Return value will be injected as an extra matrix update
        '''
        pass

    def after_matrix_scan(self, keyboard):
        '''
        Return value will be replace matrix update if supplied
        '''
        pass

    def process_key(self, keyboard, key: Key, is_pressed, int_coord):
        if self.state != State.LISTENING:
            return key
        
        if key is not None and type(key) is not Magic and is_pressed:
            self._prior_keys.append(Character(key, False))

        return key

    def before_hid_send(self, keyboard):
        if type(self.state) == SendState:
            if self.state.step(keyboard):
                self.state = State.LISTENING

    def after_hid_send(self, keyboard):
        pass

    def on_powersave_enable(self, keyboard):
        pass

    def on_powersave_disable(self, keyboard):
        pass

    def deinit(self, keyboard):
        pass

    def magic_pressed(self, key, keyboard, *args, **kwargs):
        if type(key) is not Magic:
            return keyboard

        if len(self._prior_keys) == 0:
            debug("No prior keys")
            keyboard.tap_key(key._default_key)
            return keyboard

        debug(f"Processing magic key...prior keys: {self._prior_keys}")
        match = key._match_tree.match(self._prior_keys.list())
        debug(f"Match: {match}")
        if match is None:
            keyboard.tap_key(key._default_key)
            self.clear_prior_keys()
            return keyboard
        else:
            keys = match[1]
            self.state = SendState(keys)
            # self.process_magic_async(keyboard, key, MagicIter(keyboard, keys))

        self.clear_prior_keys()

        return keyboard

    def magic_released(self, key, keyboard, *args, **kwargs):
        return keyboard

    def clear_prior_keys(self):
        self._prior_keys.clear()