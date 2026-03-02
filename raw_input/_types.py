from enum import IntEnum, IntFlag
from dataclasses import dataclass
from typing import Optional, Callable, Any


class KeyCode:
    A = 0x41
    B = 0x42
    C = 0x43
    D = 0x44
    E = 0x45
    F = 0x46
    G = 0x47
    H = 0x48
    I = 0x49
    J = 0x4A
    K = 0x4B
    L = 0x4C
    M = 0x4D
    N = 0x4E
    O = 0x4F
    P = 0x50
    Q = 0x51
    R = 0x52
    S = 0x53
    T = 0x54
    U = 0x55
    V = 0x56
    W = 0x57
    X = 0x58
    Y = 0x59
    Z = 0x5A
    DIGIT0 = 0x30
    DIGIT1 = 0x31
    DIGIT2 = 0x32
    DIGIT3 = 0x33
    DIGIT4 = 0x34
    DIGIT5 = 0x35
    DIGIT6 = 0x36
    DIGIT7 = 0x37
    DIGIT8 = 0x38
    DIGIT9 = 0x39
    ENTER = 0x0D
    ESCAPE = 0x1B
    BACKSPACE = 0x08
    TAB = 0x09
    SPACE = 0x20
    MINUS = 0xBD
    EQUAL = 0xBB
    LEFT_BRACKET = 0xDB
    RIGHT_BRACKET = 0xDD
    BACKSLASH = 0xDC
    SEMICOLON = 0xBA
    QUOTE = 0xDE
    GRAVE = 0xC0
    COMMA = 0xBC
    DOT = 0xBE
    SLASH = 0xBF
    CAPS_LOCK = 0x14
    F1 = 0x70
    F2 = 0x71
    F3 = 0x72
    F4 = 0x73
    F5 = 0x74
    F6 = 0x75
    F7 = 0x76
    F8 = 0x77
    F9 = 0x78
    F10 = 0x79
    F11 = 0x7A
    F12 = 0x7B
    PRINT_SCREEN = 0x2A
    SCROLL_LOCK = 0x91
    PAUSE = 0x13
    INSERT = 0x2D
    HOME = 0x24
    PAGE_UP = 0x21
    DELETE = 0x2E
    END = 0x23
    PAGE_DOWN = 0x22
    RIGHT_ARROW = 0x27
    LEFT_ARROW = 0x25
    DOWN_ARROW = 0x28
    UP_ARROW = 0x26
    NUM_LOCK = 0x90
    KP_DIVIDE = 0x6F
    KP_MULTIPLY = 0x6A
    KP_SUBTRACT = 0x6D
    KP_ADD = 0x6B
    KP_ENTER = 0x0D
    KP_1 = 0x61
    KP_2 = 0x62
    KP_3 = 0x63
    KP_4 = 0x64
    KP_5 = 0x65
    KP_6 = 0x66
    KP_7 = 0x67
    KP_8 = 0x68
    KP_9 = 0x69
    KP_0 = 0x60
    KP_DOT = 0x6E
    LEFT_CTRL = 0xA2
    LEFT_SHIFT = 0xA0
    LEFT_ALT = 0xA4
    LEFT_CMD = 0x5B
    RIGHT_CTRL = 0xA3
    RIGHT_SHIFT = 0xA1
    RIGHT_ALT = 0xA5
    RIGHT_CMD = 0x5C
    CTRL = 0x11
    SHIFT = 0x10
    ALT = 0x12

    _name_map = {
        0x41: "a",
        0x42: "b",
        0x43: "c",
        0x44: "d",
        0x45: "e",
        0x46: "f",
        0x47: "g",
        0x48: "h",
        0x49: "i",
        0x4A: "j",
        0x4B: "k",
        0x4C: "l",
        0x4D: "m",
        0x4E: "n",
        0x4F: "o",
        0x50: "p",
        0x51: "q",
        0x52: "r",
        0x53: "s",
        0x54: "t",
        0x55: "u",
        0x56: "v",
        0x57: "w",
        0x58: "x",
        0x59: "y",
        0x5A: "z",
        0x30: "0",
        0x31: "1",
        0x32: "2",
        0x33: "3",
        0x34: "4",
        0x35: "5",
        0x36: "6",
        0x37: "7",
        0x38: "8",
        0x39: "9",
        0x0D: "enter",
        0x1B: "esc",
        0x08: "backspace",
        0x09: "tab",
        0x20: "space",
        0xBD: "minus",
        0xBB: "equal",
        0xDB: "left_bracket",
        0xDD: "right_bracket",
        0xDC: "backslash",
        0xBA: "semicolon",
        0xDE: "quote",
        0xC0: "grave",
        0xBC: "comma",
        0xBE: "dot",
        0xBF: "slash",
        0x14: "caps_lock",
        0x70: "f1",
        0x71: "f2",
        0x72: "f3",
        0x73: "f4",
        0x74: "f5",
        0x75: "f6",
        0x76: "f7",
        0x77: "f8",
        0x78: "f9",
        0x79: "f10",
        0x7A: "f11",
        0x7B: "f12",
        0x2A: "print_screen",
        0x91: "scroll_lock",
        0x13: "pause",
        0x2D: "insert",
        0x24: "home",
        0x21: "page_up",
        0x2E: "delete",
        0x23: "end",
        0x22: "page_down",
        0x27: "right",
        0x25: "left",
        0x28: "down",
        0x26: "up",
        0x90: "num_lock",
        0x6F: "kp_divide",
        0x6A: "kp_multiply",
        0x6D: "kp_subtract",
        0x6B: "kp_add",
        0x61: "kp_1",
        0x62: "kp_2",
        0x63: "kp_3",
        0x64: "kp_4",
        0x65: "kp_5",
        0x66: "kp_6",
        0x67: "kp_7",
        0x68: "kp_8",
        0x69: "kp_9",
        0x60: "kp_0",
        0x6E: "kp_dot",
        0xA2: "lctrl",
        0xA0: "lshift",
        0xA4: "lalt",
        0x5B: "lcmd",
        0xA3: "rctrl",
        0xA1: "rshift",
        0xA5: "ralt",
        0x5C: "rcmd",
        0x11: "ctrl",
        0x10: "shift",
        0x12: "alt",
    }

    @classmethod
    def from_vk(cls, vk: int) -> Optional[str]:
        return cls._name_map.get(vk)


class Key:
    def __init__(self, vk: int):
        self.vk = vk
        self.name = KeyCode.from_vk(vk) or f"unknown_{vk:02x}"

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Key({self.name})"

    def __eq__(self, other):
        if isinstance(other, Key):
            return self.vk == other.vk
        if isinstance(other, str):
            return self.name == other
        return False

    def __hash__(self):
        return hash(self.vk)


class Button:
    LEFT = "left"
    RIGHT = "right"
    MIDDLE = "middle"
    X1 = "x1"
    X2 = "x2"

    def __init__(self, button: str):
        self.name = button

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Button({self.name})"

    def __eq__(self, other):
        if isinstance(other, Button):
            return self.name == other.name
        if isinstance(other, str):
            return self.name == other
        return False

    def __hash__(self):
        return hash(self.name)


@dataclass
class KeyboardEvent:
    key: Key
    pressed: bool
    device_handle: Optional[int] = None
    vid: Optional[int] = None
    pid: Optional[int] = None


@dataclass
class MouseEvent:
    x: int
    y: int
    button: Optional[Button] = None
    pressed: Optional[bool] = None
    dx: int = 0
    dy: int = 0
    scroll: int = 0
    device_handle: Optional[int] = None
    vid: Optional[int] = None
    pid: Optional[int] = None


class DeviceInfo:
    def __init__(self, handle: int, vid: int, pid: int, name: str = ""):
        self.handle = handle
        self.vid = vid
        self.pid = pid
        self.name = name

    def __repr__(self):
        return f"DeviceInfo(handle=0x{self.handle:X}, vid=0x{self.vid:04X}, pid=0x{self.pid:04X}, name='{self.name}')"


KeyboardListenerCallback = Callable[[KeyboardEvent], Optional[bool]]
MouseListenerCallback = Callable[[MouseEvent], Optional[bool]]
