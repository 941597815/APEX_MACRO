from typing import Optional, Callable, List, Dict
from threading import Thread, Event, Lock
import ctypes
from ctypes import wintypes
from ._rawinput import RawInputListener
from ._types import KeyboardEvent, MouseEvent, Key, Button, DeviceInfo


_listener_lock = Lock()
_global_listener: Optional["UnifiedListener"] = None
_keyboard_callbacks: List[Callable] = []
_mouse_callbacks: List[Callable] = []


class UnifiedListener:
    def __init__(self):
        self._running = False
        self._listener: Optional[RawInputListener] = None
        self._stop_event = Event()

    def _on_keyboard(self, event: KeyboardEvent) -> Optional[bool]:
        for callback in _keyboard_callbacks[:]:
            try:
                result = callback(event)
                if result is False:
                    return False
            except Exception:
                pass
        return None

    def _on_mouse(self, event: MouseEvent) -> Optional[bool]:
        for callback in _mouse_callbacks[:]:
            try:
                result = callback(event)
                if result is False:
                    return False
            except Exception:
                pass
        return None

    def start(self):
        if self._running:
            return
        self._running = True
        self._stop_event.clear()
        self._listener = RawInputListener(
            on_keyboard=self._on_keyboard,
            on_mouse=self._on_mouse,
        )
        self._listener.start()

    def stop(self):
        if not self._running:
            return
        self._running = False
        self._stop_event.set()
        if self._listener:
            self._listener.stop()
            self._listener = None

    def join(self, timeout: Optional[float] = None):
        if self._listener:
            self._listener._thread.join(timeout=timeout)


def _ensure_listener():
    global _global_listener
    with _listener_lock:
        if _global_listener is None:
            _global_listener = UnifiedListener()
            _global_listener.start()
        return _global_listener


def register_keyboard_callback(callback: Callable[[KeyboardEvent], Optional[bool]]):
    _keyboard_callbacks.append(callback)
    return _ensure_listener()


def unregister_keyboard_callback(callback: Callable):
    if callback in _keyboard_callbacks:
        _keyboard_callbacks.remove(callback)


def register_mouse_callback(callback: Callable[[MouseEvent], Optional[bool]]):
    _mouse_callbacks.append(callback)
    return _ensure_listener()


def unregister_mouse_callback(callback: Callable):
    if callback in _mouse_callbacks:
        _mouse_callbacks.remove(callback)


class KeyboardListener:
    def __init__(
        self,
        on_press: Optional[Callable[[Key], Optional[bool]]] = None,
        on_release: Optional[Callable[[Key], Optional[bool]]] = None,
        vid: Optional[int] = None,
        pid: Optional[int] = None,
        suppress: bool = False,
        exclude_devices: Optional[List[Dict[str, int]]] = None,
        include_devices: Optional[List[Dict[str, int]]] = None,
    ):
        self.on_press = on_press
        self.on_release = on_release
        self.vid = vid
        self.pid = pid
        self.suppress = suppress
        self.exclude_devices = exclude_devices
        self.include_devices = include_devices
        self._running = False
        self._stop_event = Event()
        self._callback = None

    def _on_event(self, event: KeyboardEvent) -> Optional[bool]:
        if self._stop_event.is_set():
            return False

        if self.vid is not None and event.vid != self.vid:
            return None
        if self.pid is not None and event.pid != self.pid:
            return None

        if self.exclude_devices:
            for device in self.exclude_devices:
                vid_match = device.get("vid") is None or device.get("vid") == event.vid
                pid_match = device.get("pid") is None or device.get("pid") == event.pid
                if vid_match and pid_match:
                    return None

        if self.include_devices:
            found = False
            for device in self.include_devices:
                vid_match = device.get("vid") is None or device.get("vid") == event.vid
                pid_match = device.get("pid") is None or device.get("pid") == event.pid
                if vid_match and pid_match:
                    found = True
                    break
            if not found:
                return None

        try:
            if event.pressed and self.on_press:
                result = self.on_press(event.key)
                if result is False:
                    return False
                if self.suppress:
                    return True
            elif not event.pressed and self.on_release:
                result = self.on_release(event.key)
                if result is False:
                    return False
                if self.suppress:
                    return True
        except Exception:
            pass

        return None

    def start(self):
        if self._running:
            return
        self._running = True
        self._stop_event.clear()
        self._callback = self._on_event
        register_keyboard_callback(self._callback)

    def stop(self):
        if not self._running:
            return
        self._running = False
        self._stop_event.set()
        if self._callback:
            unregister_keyboard_callback(self._callback)
            self._callback = None

    def join(self, timeout: Optional[float] = None):
        _global_listener.join(timeout=timeout)

    def wait(self):
        self._stop_event.wait()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        return False


class MouseListener:
    def __init__(
        self,
        on_move: Optional[Callable[[int, int], Optional[bool]]] = None,
        on_click: Optional[Callable[[int, int, Button, bool], Optional[bool]]] = None,
        on_scroll: Optional[Callable[[int, int, int], Optional[bool]]] = None,
        vid: Optional[int] = None,
        pid: Optional[int] = None,
        suppress: bool = False,
        exclude_devices: Optional[List[Dict[str, int]]] = None,
        include_devices: Optional[List[Dict[str, int]]] = None,
    ):
        self.on_move = on_move
        self.on_click = on_click
        self.on_scroll = on_scroll
        self.vid = vid
        self.pid = pid
        self.suppress = suppress
        self.exclude_devices = exclude_devices
        self.include_devices = include_devices
        self._running = False
        self._stop_event = Event()
        self._callback = None

    def _get_cursor_pos(self) -> tuple:
        pt = wintypes.POINT()
        ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
        return (pt.x, pt.y)

    def _on_event(self, event: MouseEvent) -> Optional[bool]:
        if self._stop_event.is_set():
            return False

        if self.vid is not None and event.vid != self.vid:
            return None
        if self.pid is not None and event.pid != self.pid:
            return None

        if self.exclude_devices:
            for device in self.exclude_devices:
                vid_match = device.get("vid") is None or device.get("vid") == event.vid
                pid_match = device.get("pid") is None or device.get("pid") == event.pid
                if vid_match and pid_match:
                    return None

        if self.include_devices:
            found = False
            for device in self.include_devices:
                vid_match = device.get("vid") is None or device.get("vid") == event.vid
                pid_match = device.get("pid") is None or device.get("pid") == event.pid
                if vid_match and pid_match:
                    found = True
                    break
            if not found:
                return None

        try:
            x, y = self._get_cursor_pos()

            if event.dx != 0 or event.dy != 0:
                if self.on_move:
                    result = self.on_move(x, y)
                    if result is False:
                        return False
                    if self.suppress:
                        return True

            if event.button is not None and event.pressed is not None:
                if self.on_click:
                    result = self.on_click(x, y, event.button, event.pressed)
                    if result is False:
                        return False
                    if self.suppress:
                        return True

            if event.scroll != 0:
                if self.on_scroll:
                    result = self.on_scroll(x, y, event.scroll)
                    if result is False:
                        return False
                    if self.suppress:
                        return True
        except Exception:
            pass

        return None

    def start(self):
        if self._running:
            return
        self._running = True
        self._stop_event.clear()
        self._callback = self._on_event
        register_mouse_callback(self._callback)

    def stop(self):
        if not self._running:
            return
        self._running = False
        self._stop_event.set()
        if self._callback:
            unregister_mouse_callback(self._callback)
            self._callback = None

    def join(self, timeout: Optional[float] = None):
        _global_listener.join(timeout=timeout)

    def wait(self):
        self._stop_event.wait()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        return False
