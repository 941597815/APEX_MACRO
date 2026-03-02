from typing import Optional, Callable, List, Dict
from ._listener import KeyboardListener as _KeyboardListener
from ._types import Key, KeyCode, DeviceInfo


class Listener(_KeyboardListener):
    pass


def listen(
    on_press: Optional[Callable[[Key], Optional[bool]]] = None,
    on_release: Optional[Callable[[Key], Optional[bool]]] = None,
    vid: Optional[int] = None,
    pid: Optional[int] = None,
    suppress: bool = False,
    exclude_devices: Optional[List[Dict[str, int]]] = None,
    include_devices: Optional[List[Dict[str, int]]] = None,
) -> Listener:
    listener = Listener(
        on_press=on_press,
        on_release=on_release,
        vid=vid,
        pid=pid,
        suppress=suppress,
        exclude_devices=exclude_devices,
        include_devices=include_devices,
    )
    listener.start()
    return listener


class Controller:
    def __init__(self, vid: Optional[int] = None, pid: Optional[int] = None):
        self.vid = vid
        self.pid = pid

    def press(self, key: Key):
        import ctypes

        vk = self._key_to_vk(key)
        if vk:
            ctypes.windll.user32.keybd_event(vk, 0, 0, 0)

    def release(self, key: Key):
        import ctypes

        vk = self._key_to_vk(key)
        if vk:
            ctypes.windll.user32.keybd_event(vk, 0, 2, 0)

    def _key_to_vk(self, key: Key) -> int:
        vk_map = {
            KeyCode.A: 0x41,
            KeyCode.B: 0x42,
            KeyCode.C: 0x43,
            KeyCode.D: 0x44,
            KeyCode.E: 0x45,
            KeyCode.F: 0x46,
            KeyCode.G: 0x47,
            KeyCode.H: 0x48,
            KeyCode.I: 0x49,
            KeyCode.J: 0x4A,
            KeyCode.K: 0x4B,
            KeyCode.L: 0x4C,
            KeyCode.M: 0x4D,
            KeyCode.N: 0x4E,
            KeyCode.O: 0x4F,
            KeyCode.P: 0x50,
            KeyCode.Q: 0x51,
            KeyCode.R: 0x52,
            KeyCode.S: 0x53,
            KeyCode.T: 0x54,
            KeyCode.U: 0x55,
            KeyCode.V: 0x56,
            KeyCode.W: 0x57,
            KeyCode.X: 0x58,
            KeyCode.Y: 0x59,
            KeyCode.Z: 0x5A,
            KeyCode.DIGIT0: 0x30,
            KeyCode.DIGIT1: 0x31,
            KeyCode.DIGIT2: 0x32,
            KeyCode.DIGIT3: 0x33,
            KeyCode.DIGIT4: 0x34,
            KeyCode.DIGIT5: 0x35,
            KeyCode.DIGIT6: 0x36,
            KeyCode.DIGIT7: 0x37,
            KeyCode.DIGIT8: 0x38,
            KeyCode.DIGIT9: 0x39,
            KeyCode.ENTER: 0x0D,
            KeyCode.ESCAPE: 0x1B,
            KeyCode.BACKSPACE: 0x08,
            KeyCode.TAB: 0x09,
            KeyCode.SPACE: 0x20,
            KeyCode.LEFT_CTRL: 0xA2,
            KeyCode.RIGHT_CTRL: 0xA3,
            KeyCode.LEFT_ALT: 0xA4,
            KeyCode.RIGHT_ALT: 0xA5,
            KeyCode.LEFT_SHIFT: 0xA0,
            KeyCode.RIGHT_SHIFT: 0xA1,
            KeyCode.LEFT_ARROW: 0x25,
            KeyCode.UP_ARROW: 0x26,
            KeyCode.RIGHT_ARROW: 0x27,
            KeyCode.DOWN_ARROW: 0x28,
            KeyCode.F1: 0x70,
            KeyCode.F2: 0x71,
            KeyCode.F3: 0x72,
            KeyCode.F4: 0x73,
            KeyCode.F5: 0x74,
            KeyCode.F6: 0x75,
            KeyCode.F7: 0x76,
            KeyCode.F8: 0x77,
            KeyCode.F9: 0x78,
            KeyCode.F10: 0x79,
            KeyCode.F11: 0x7A,
            KeyCode.F12: 0x7B,
        }
        if isinstance(key, Key):
            return vk_map.get(key.vk, 0)
        return 0

    def type(self, text: str):
        import ctypes

        user32 = ctypes.windll.user32
        for char in text:
            vk = ord(char.upper())
            shift = char.isupper()
            if shift:
                user32.keybd_event(0x10, 0, 0, 0)
            user32.keybd_event(vk, 0, 0, 0)
            user32.keybd_event(vk, 0, 2, 0)
            if shift:
                user32.keybd_event(0x10, 0, 2, 0)


def list_keyboards() -> list:
    from ._rawinput import list_keyboards as _list_keyboards

    return _list_keyboards()
