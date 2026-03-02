import ctypes
from ctypes import (
    wintypes,
    Structure,
    POINTER,
    byref,
    sizeof,
    cast,
    c_ushort,
    c_ulong,
    c_char,
    c_void_p,
    c_int,
    c_long,
    Union,
)
import threading
from typing import Optional, List, Callable, Dict, Tuple, Set
from ._types import KeyboardEvent, MouseEvent, Key, Button, DeviceInfo, KeyCode

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

user32.DefWindowProcW.restype = c_long
user32.DefWindowProcW.argtypes = [
    wintypes.HWND,
    wintypes.UINT,
    wintypes.WPARAM,
    wintypes.LPARAM,
]

RIDI_DEVICENAME = 0x20000007
RIDI_DEVICEINFO = 0x2000000B
RIDI_PREPARSEDDATA = 0x20000005

RIM_TYPEMOUSE = 0
RIM_TYPEKEYBOARD = 1
RIM_TYPEHID = 2

RIDEV_INPUTSINK = 0x00000100
RIDEV_REMOVE = 0x00000001

WM_INPUT = 0x00FF
WM_DESTROY = 0x0002

RID_INPUT = 0x10000003

RIDEV_NOLEGACY = 0x00000030

MOUSE_MOVE_RELATIVE = 0x00
MOUSE_MOVE_ABSOLUTE = 0x01
MOUSE_VIRTUAL_DESKTOP = 0x02
MOUSE_ATTRIBUTES_CHANGED = 0x04

RI_MOUSE_LEFT_BUTTON_DOWN = 0x0001
RI_MOUSE_LEFT_BUTTON_UP = 0x0002
RI_MOUSE_RIGHT_BUTTON_DOWN = 0x0004
RI_MOUSE_RIGHT_BUTTON_UP = 0x0008
RI_MOUSE_MIDDLE_BUTTON_DOWN = 0x0010
RI_MOUSE_MIDDLE_BUTTON_UP = 0x0020
RI_MOUSE_BUTTON_4_DOWN = 0x0040
RI_MOUSE_BUTTON_4_UP = 0x0080
RI_MOUSE_BUTTON_5_DOWN = 0x0100
RI_MOUSE_BUTTON_5_UP = 0x0200
RI_MOUSE_WHEEL = 0x0400

RI_KEY_MAKE = 0x00
RI_KEY_BREAK = 0x01
RI_KEY_E0 = 0x02
RI_KEY_E1 = 0x04

HWND_MESSAGE = wintypes.HWND(-3)

GWL_WNDPROC = -4

WNDPROC = ctypes.WINFUNCTYPE(
    c_long, wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM
)


class RAWINPUTDEVICELIST(Structure):
    _fields_ = [
        ("hDevice", wintypes.HANDLE),
        ("dwType", wintypes.DWORD),
    ]


class RAWINPUTDEVICE(Structure):
    _fields_ = [
        ("usUsagePage", c_ushort),
        ("usUsage", c_ushort),
        ("dwFlags", wintypes.DWORD),
        ("hwndTarget", wintypes.HWND),
    ]


class RAWINPUTHEADER(Structure):
    _fields_ = [
        ("dwType", wintypes.DWORD),
        ("dwSize", wintypes.DWORD),
        ("hDevice", wintypes.HANDLE),
        ("wParam", wintypes.WPARAM),
    ]


class _BUTTONDATA(Structure):
    _fields_ = [
        ("usButtonFlags", c_ushort),
        ("usButtonData", c_ushort),
    ]


class _BUTTONS(Union):
    _fields_ = [
        ("ulButtons", wintypes.ULONG),
        ("button", _BUTTONDATA),
    ]


class RAWMOUSE(Structure):
    _anonymous_ = ("buttons",)
    _fields_ = [
        ("usFlags", c_ushort),
        ("buttons", _BUTTONS),
        ("ulRawButtons", wintypes.ULONG),
        ("lLastX", wintypes.LONG),
        ("lLastY", wintypes.LONG),
        ("ulExtraInformation", wintypes.ULONG),
    ]


class RAWKEYBOARD(Structure):
    _fields_ = [
        ("MakeCode", c_ushort),
        ("Flags", c_ushort),
        ("Reserved", c_ushort),
        ("VKey", c_ushort),
        ("Message", wintypes.UINT),
        ("ExtraInformation", wintypes.ULONG),
    ]


class RAWHID(Structure):
    _pack_ = 2
    _fields_ = [
        ("dwSizeHid", wintypes.DWORD),
        ("dwCount", wintypes.DWORD),
        ("bRawData", c_char * 1),
    ]


class _RAWDATA(Union):
    _pack_ = 2
    _fields_ = [
        ("mouse", RAWMOUSE),
        ("keyboard", RAWKEYBOARD),
        ("hid", RAWHID),
    ]


class RAWINPUT(Structure):
    _pack_ = 8
    _fields_ = [
        ("header", RAWINPUTHEADER),
        ("data", _RAWDATA),
    ]


class WNDCLASSEX(Structure):
    _fields_ = [
        ("cbSize", wintypes.UINT),
        ("style", wintypes.UINT),
        ("lpfnWndProc", WNDPROC),
        ("cbClsExtra", c_ushort),
        ("cbWndExtra", c_ushort),
        ("hInstance", wintypes.HINSTANCE),
        ("hIcon", wintypes.HANDLE),
        ("hCursor", wintypes.HANDLE),
        ("hbrBackground", wintypes.HANDLE),
        ("lpszMenuName", wintypes.LPCWSTR),
        ("lpszClassName", wintypes.LPCWSTR),
        ("hIconSm", wintypes.HANDLE),
    ]


def get_raw_input_devices() -> List[Tuple[int, int]]:
    num_devices = wintypes.UINT()
    user32.GetRawInputDeviceList(None, byref(num_devices), sizeof(RAWINPUTDEVICELIST))

    if num_devices.value == 0:
        return []

    devices = (RAWINPUTDEVICELIST * num_devices.value)()
    user32.GetRawInputDeviceList(
        devices, byref(num_devices), sizeof(RAWINPUTDEVICELIST)
    )

    result = []
    for device in devices:
        result.append((device.hDevice, device.dwType))

    return result


def get_device_info(hDevice: int) -> Optional[DeviceInfo]:
    size = wintypes.UINT()
    user32.GetRawInputDeviceInfoW(hDevice, RIDI_DEVICENAME, None, byref(size))

    if size.value == 0:
        return None

    name_buffer = (wintypes.WCHAR * (size.value + 1))()
    user32.GetRawInputDeviceInfoW(hDevice, RIDI_DEVICENAME, name_buffer, byref(size))
    device_name = "".join(name_buffer).rstrip("\x00")

    vid = 0
    pid = 0

    if "VID_" in device_name and "PID_" in device_name:
        try:
            vid_start = device_name.index("VID_") + 4
            vid = int(device_name[vid_start : vid_start + 4], 16)
            pid_start = device_name.index("PID_") + 4
            pid = int(device_name[pid_start : pid_start + 4], 16)
        except (ValueError, IndexError):
            pass

    return DeviceInfo(hDevice, vid, pid, device_name)


def get_all_devices_with_vid_pid() -> Dict[int, DeviceInfo]:
    devices = get_raw_input_devices()
    result = {}
    for hDevice, dwType in devices:
        info = get_device_info(hDevice)
        if info:
            result[hDevice] = info
    return result


class RawInputListener:
    _class_counter = 0

    def __init__(
        self,
        vid: Optional[int] = None,
        pid: Optional[int] = None,
        on_keyboard: Optional[Callable[[KeyboardEvent], Optional[bool]]] = None,
        on_mouse: Optional[Callable[[MouseEvent], Optional[bool]]] = None,
        exclude_devices: Optional[List[Dict[str, int]]] = None,
        include_devices: Optional[List[Dict[str, int]]] = None,
    ):
        self.vid = vid
        self.pid = pid
        self.on_keyboard = on_keyboard
        self.on_mouse = on_mouse
        self.exclude_devices = exclude_devices or []
        self.include_devices = include_devices or []
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._hwnd: Optional[int] = None
        self._device_cache: Dict[int, DeviceInfo] = {}
        self._allowed_handles: Set[int] = set()
        self._suppress = False
        self._wnd_proc_ref = None
        self._class_name = f"RawInputListener_{id(self)}"

    def _is_device_allowed(self, hDevice: int) -> bool:
        if hDevice not in self._device_cache:
            info = get_device_info(hDevice)
            if info:
                self._device_cache[hDevice] = info

        info = self._device_cache.get(hDevice)
        if info is None:
            return False

        if self.include_devices:
            for device in self.include_devices:
                vid_match = device.get("vid") is None or device.get("vid") == info.vid
                pid_match = device.get("pid") is None or device.get("pid") == info.pid
                if vid_match and pid_match:
                    return True
            return False

        for device in self.exclude_devices:
            vid_match = device.get("vid") is None or device.get("vid") == info.vid
            pid_match = device.get("pid") is None or device.get("pid") == info.pid
            if vid_match and pid_match:
                return False

        if self.vid is not None and info.vid != self.vid:
            return False
        if self.pid is not None and info.pid != self.pid:
            return False

        return True

    def _get_device_vid_pid(self, hDevice: int) -> Tuple[Optional[int], Optional[int]]:
        if hDevice not in self._device_cache:
            info = get_device_info(hDevice)
            if info:
                self._device_cache[hDevice] = info

        info = self._device_cache.get(hDevice)
        if info:
            return info.vid, info.pid
        return None, None

    def _process_keyboard(self, raw: RAWINPUT) -> Optional[bool]:
        hDevice = raw.header.hDevice

        if not self._is_device_allowed(hDevice):
            return None

        keyboard = raw.data.keyboard
        make_code = keyboard.MakeCode
        flags = keyboard.Flags

        pressed = not (flags & RI_KEY_BREAK)

        is_extended = bool(flags & RI_KEY_E0)

        if make_code == 0x1D:
            if is_extended:
                vk = 0xA3
            else:
                vk = 0xA2
        elif make_code == 0x2A:
            vk = 0xA0
        elif make_code == 0x36:
            vk = 0xA1
        elif make_code == 0x38:
            if is_extended:
                vk = 0xA5
            else:
                vk = 0xA4
        elif make_code == 0x5B:
            if is_extended:
                vk = 0x5C
            else:
                vk = 0x5B
        else:
            vk = keyboard.VKey

        vid, pid = self._get_device_vid_pid(hDevice)

        event = KeyboardEvent(
            key=Key(vk),
            pressed=pressed,
            device_handle=hDevice,
            vid=vid,
            pid=pid,
        )

        if self.on_keyboard:
            return self.on_keyboard(event)
        return None

    def _process_mouse(self, raw: RAWINPUT) -> Optional[bool]:
        hDevice = raw.header.hDevice

        if not self._is_device_allowed(hDevice):
            return None

        mouse = raw.data.mouse
        button_flags = mouse.buttons.button.usButtonFlags

        button = None
        pressed = None

        if button_flags & (RI_MOUSE_LEFT_BUTTON_DOWN | RI_MOUSE_LEFT_BUTTON_UP):
            button = Button.LEFT
            pressed = bool(button_flags & RI_MOUSE_LEFT_BUTTON_DOWN)
        elif button_flags & (RI_MOUSE_RIGHT_BUTTON_DOWN | RI_MOUSE_RIGHT_BUTTON_UP):
            button = Button.RIGHT
            pressed = bool(button_flags & RI_MOUSE_RIGHT_BUTTON_DOWN)
        elif button_flags & (RI_MOUSE_MIDDLE_BUTTON_DOWN | RI_MOUSE_MIDDLE_BUTTON_UP):
            button = Button.MIDDLE
            pressed = bool(button_flags & RI_MOUSE_MIDDLE_BUTTON_DOWN)
        elif button_flags & (RI_MOUSE_BUTTON_4_DOWN | RI_MOUSE_BUTTON_4_UP):
            button = Button.X1
            pressed = bool(button_flags & RI_MOUSE_BUTTON_4_DOWN)
        elif button_flags & (RI_MOUSE_BUTTON_5_DOWN | RI_MOUSE_BUTTON_5_UP):
            button = Button.X2
            pressed = bool(button_flags & RI_MOUSE_BUTTON_5_DOWN)

        scroll = 0
        if button_flags & RI_MOUSE_WHEEL:
            scroll_val = ctypes.c_short(mouse.buttons.button.usButtonData).value
            scroll = scroll_val // 120

        vid, pid = self._get_device_vid_pid(hDevice)

        event = MouseEvent(
            x=0,
            y=0,
            button=button,
            pressed=pressed,
            dx=mouse.lLastX,
            dy=mouse.lLastY,
            scroll=scroll,
            device_handle=hDevice,
            vid=vid,
            pid=pid,
        )

        if self.on_mouse:
            return self.on_mouse(event)
        return None

    def _wnd_proc(self, hwnd, msg, wParam, lParam):
        if msg == WM_INPUT:
            size = wintypes.UINT()
            user32.GetRawInputData(
                lParam, RID_INPUT, None, byref(size), sizeof(RAWINPUTHEADER)
            )

            if size.value > 0:
                buffer = (ctypes.c_byte * size.value)()
                raw = cast(buffer, POINTER(RAWINPUT)).contents

                user32.GetRawInputData(
                    lParam, RID_INPUT, byref(raw), byref(size), sizeof(RAWINPUTHEADER)
                )

                if raw.header.dwType == RIM_TYPEKEYBOARD:
                    result = self._process_keyboard(raw)
                    if result is True:
                        return 0
                elif raw.header.dwType == RIM_TYPEMOUSE:
                    result = self._process_mouse(raw)
                    if result is True:
                        return 0

        elif msg == WM_DESTROY:
            self._running = False
            user32.PostQuitMessage(0)
            return 0

        return user32.DefWindowProcW(hwnd, msg, wParam, lParam)

    def _message_loop(self):
        wnd_proc = WNDPROC(self._wnd_proc)
        self._wnd_proc_ref = wnd_proc

        hInstance = kernel32.GetModuleHandleW(None)

        wc = WNDCLASSEX()
        wc.cbSize = sizeof(WNDCLASSEX)
        wc.style = 0
        wc.lpfnWndProc = wnd_proc
        wc.cbClsExtra = 0
        wc.cbWndExtra = 0
        wc.hInstance = hInstance
        wc.hIcon = None
        wc.hCursor = None
        wc.hbrBackground = None
        wc.lpszMenuName = None
        wc.lpszClassName = self._class_name
        wc.hIconSm = None

        atom = user32.RegisterClassExW(byref(wc))
        if atom == 0:
            error = kernel32.GetLastError()
            raise RuntimeError(f"Failed to register window class, error: {error}")

        self._hwnd = user32.CreateWindowExW(
            0,
            self._class_name,
            "RawInputListener",
            0,
            0,
            0,
            0,
            0,
            HWND_MESSAGE,
            None,
            hInstance,
            None,
        )

        if not self._hwnd:
            error = kernel32.GetLastError()
            raise RuntimeError(f"Failed to create window, error: {error}")

        rid = (RAWINPUTDEVICE * 2)()

        rid[0].usUsagePage = 0x01
        rid[0].usUsage = 0x06
        rid[0].dwFlags = RIDEV_INPUTSINK
        rid[0].hwndTarget = self._hwnd

        rid[1].usUsagePage = 0x01
        rid[1].usUsage = 0x02
        rid[1].dwFlags = RIDEV_INPUTSINK
        rid[1].hwndTarget = self._hwnd

        if not user32.RegisterRawInputDevices(rid, 2, sizeof(RAWINPUTDEVICE)):
            error = kernel32.GetLastError()
            raise RuntimeError(f"Failed to register raw input devices, error: {error}")

        msg = wintypes.MSG()
        while self._running:
            result = user32.GetMessageW(byref(msg), None, 0, 0)
            if result == 0:
                break
            user32.TranslateMessage(byref(msg))
            user32.DispatchMessageW(byref(msg))

        if self._hwnd:
            user32.DestroyWindow(self._hwnd)
        user32.UnregisterClassW(self._class_name, hInstance)

    def start(self):
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._message_loop, daemon=True)
        self._thread.start()

    def stop(self):
        if not self._running:
            return
        self._running = False
        if self._hwnd:
            user32.PostMessageW(self._hwnd, WM_DESTROY, 0, 0)
        if self._thread:
            self._thread.join(timeout=2.0)
            self._thread = None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        return False


def list_devices() -> List[DeviceInfo]:
    devices = get_all_devices_with_vid_pid()
    return list(devices.values())


def list_keyboards() -> List[DeviceInfo]:
    devices = get_raw_input_devices()
    result = []
    for hDevice, dwType in devices:
        if dwType == RIM_TYPEKEYBOARD:
            info = get_device_info(hDevice)
            if info:
                result.append(info)
    return result


def list_mice() -> List[DeviceInfo]:
    devices = get_raw_input_devices()
    result = []
    for hDevice, dwType in devices:
        if dwType == RIM_TYPEMOUSE:
            info = get_device_info(hDevice)
            if info:
                result.append(info)
    return result
