from typing import Optional, Callable, List, Dict
import ctypes
from ctypes import wintypes
from ._listener import MouseListener as _MouseListener
from ._types import Button, DeviceInfo


class Listener(_MouseListener):
    pass


def listen(
    on_move: Optional[Callable[[int, int], Optional[bool]]] = None,
    on_click: Optional[Callable[[int, int, Button, bool], Optional[bool]]] = None,
    on_scroll: Optional[Callable[[int, int, int], Optional[bool]]] = None,
    vid: Optional[int] = None,
    pid: Optional[int] = None,
    suppress: bool = False,
    exclude_devices: Optional[List[Dict[str, int]]] = None,
    include_devices: Optional[List[Dict[str, int]]] = None,
) -> Listener:
    listener = Listener(
        on_move=on_move,
        on_click=on_click,
        on_scroll=on_scroll,
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

    def move(self, dx: int, dy: int):
        ctypes.windll.user32.mouse_event(0x0001, dx, dy, 0, 0)

    def move_to(self, x: int, y: int):
        ctypes.windll.user32.SetCursorPos(x, y)

    def press(self, button: str = Button.LEFT):
        dwFlags = self._button_to_down_flag(button)
        ctypes.windll.user32.mouse_event(dwFlags, 0, 0, 0, 0)

    def release(self, button: str = Button.LEFT):
        dwFlags = self._button_to_up_flag(button)
        ctypes.windll.user32.mouse_event(dwFlags, 0, 0, 0, 0)

    def click(self, button: str = Button.LEFT, count: int = 1):
        for _ in range(count):
            self.press(button)
            self.release(button)

    def scroll(self, dx: int = 0, dy: int = 0):
        if dy != 0:
            ctypes.windll.user32.mouse_event(0x0800, 0, 0, dy * 120, 0)
        if dx != 0:
            ctypes.windll.user32.mouse_event(0x1000, 0, 0, dx * 120, 0)

    def _button_to_down_flag(self, button: str) -> int:
        flags = {
            Button.LEFT: 0x0002,
            Button.RIGHT: 0x0008,
            Button.MIDDLE: 0x0020,
            Button.X1: 0x0080,
            Button.X2: 0x0080,
        }
        return flags.get(button, 0x0002)

    def _button_to_up_flag(self, button: str) -> int:
        flags = {
            Button.LEFT: 0x0004,
            Button.RIGHT: 0x0010,
            Button.MIDDLE: 0x0040,
            Button.X1: 0x0100,
            Button.X2: 0x0100,
        }
        return flags.get(button, 0x0004)

    @property
    def position(self) -> tuple:
        pt = wintypes.POINT()
        ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
        return (pt.x, pt.y)


def list_mice() -> list:
    from ._rawinput import list_mice as _list_mice

    return _list_mice()
