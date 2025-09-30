"""
HIDDevice 顶层静态类
用法：
    from Arduino_dll import HIDDevice
    HIDDevice.open()          # 自动使用默认 VID/PID
    HIDDevice.mouse.move(100, 50)
    HIDDevice.keyboard.type("Hello")
    HIDDevice.close()
"""

import ctypes
import os
import time

# ------------------ DLL 加载 ------------------
_dll = ctypes.CDLL(os.path.join(os.path.dirname(__file__), "./arduino.dll"))

# ------------------ 原型声明 ------------------
_dll.HID_Open.argtypes = [ctypes.c_ushort, ctypes.c_ushort]
_dll.HID_Open.restype = ctypes.c_bool
_dll.HID_Close.restype = None
_dll.ReleaseAll.restype = ctypes.c_bool

_dll.Mouse_Move.argtypes = [ctypes.c_int, ctypes.c_int]
_dll.Mouse_Move.restype = ctypes.c_bool
_dll.Mouse_Wheel.argtypes = [ctypes.c_int]
_dll.Mouse_Wheel.restype = ctypes.c_bool
_dll.Mouse_Press.argtypes = [ctypes.c_char_p]
_dll.Mouse_Press.restype = ctypes.c_bool
_dll.Mouse_Release.argtypes = [ctypes.c_char_p]
_dll.Mouse_Release.restype = ctypes.c_bool
_dll.Mouse_Click.argtypes = [ctypes.c_char_p]
_dll.Mouse_Click.restype = ctypes.c_bool
_dll.Mouse_Drag.argtypes = [
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_char_p,
    ctypes.c_int,
    ctypes.c_int,
]
_dll.Mouse_Drag.restype = ctypes.c_bool

_dll.Key_Press.argtypes = [ctypes.c_char_p]
_dll.Key_Press.restype = ctypes.c_bool
_dll.Key_Release.argtypes = [ctypes.c_char_p]
_dll.Key_Release.restype = ctypes.c_bool
_dll.Key_Click.argtypes = [ctypes.c_char_p]
_dll.Key_Click.restype = ctypes.c_bool
_dll.Key_Type.argtypes = [ctypes.c_char_p]
_dll.Key_Type.restype = ctypes.c_bool
_dll.Key_Hotkey.argtypes = [ctypes.POINTER(ctypes.c_char_p), ctypes.c_int, ctypes.c_int]
_dll.Key_Hotkey.restype = ctypes.c_bool

# ------------------ 静态常量 ------------------
_DEFAULT_VID_PID = (0x046D, 0xC08F)  # 默认示例


# ------------------ 顶层类 ------------------
class HIDDevice:
    """HIDDevice 顶层静态类（全局单例）"""

    vid_pid = None

    # ---------- 设备管理 ----------
    @staticmethod
    def open(vid_pid=None):
        vid, pid = vid_pid or _DEFAULT_VID_PID
        ok = _dll.HID_Open(vid, pid)
        if not ok:
            raise RuntimeError("Unable to open HID device")
        HIDDevice.vid_pid = (vid, pid)

    @staticmethod
    def close():
        _dll.ReleaseAll()
        _dll.HID_Close()

    # ---------- 静态鼠标 ----------
    class mouse:
        LEFT = b"LEFT"
        RIGHT = b"RIGHT"
        MIDDLE = b"MIDDLE"

        @staticmethod
        def move(x: int, y: int) -> bool:
            return _dll.Mouse_Move(x, y)

        @staticmethod
        def wheel(a: int) -> bool:
            return _dll.Mouse_Wheel(a)

        @staticmethod
        def press(button=LEFT) -> bool:
            return _dll.Mouse_Press(button)

        @staticmethod
        def release(button=LEFT) -> bool:
            return _dll.Mouse_Release(button)

        @staticmethod
        def click(button=LEFT) -> bool:
            return _dll.Mouse_Click(button)

        @staticmethod
        def drag(
            start_x, start_y, end_x, end_y, button=LEFT, steps=10, delay_ms=10
        ) -> bool:
            return _dll.Mouse_Drag(
                start_x, start_y, end_x, end_y, button, steps, delay_ms
            )

    # ---------- 静态键盘 ----------
    class keyboard:
        # 字母
        A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z = [
            bytes([c]) for c in range(ord("A"), ord("Z") + 1)
        ]
        # 数字
        KEY_0, KEY_1, KEY_2, KEY_3, KEY_4, KEY_5, KEY_6, KEY_7, KEY_8, KEY_9 = [
            bytes([c]) for c in range(ord("0"), ord("9") + 1)
        ]
        # 功能键
        ENTER, ESC, BACKSPACE, TAB, SPACE = (
            b"ENTER",
            b"ESC",
            b"BACKSPACE",
            b"TAB",
            b"SPACE",
        )
        F1, F2, F3, F4, F5, F6, F7, F8, F9, F10, F11, F12 = (
            b"F1",
            b"F2",
            b"F3",
            b"F4",
            b"F5",
            b"F6",
            b"F7",
            b"F8",
            b"F9",
            b"F10",
            b"F11",
            b"F12",
        )
        # 修饰键
        LCTRL, LSHIFT, LALT, LGUI, RCTRL, RSHIFT, RALT, RGUI = (
            b"LCTRL",
            b"LSHIFT",
            b"LALT",
            b"LGUI",
            b"RCTRL",
            b"RSHIFT",
            b"RALT",
            b"RGUI",
        )

        @staticmethod
        def press(key) -> bool:
            return _dll.Key_Press(key if isinstance(key, bytes) else key.encode())

        @staticmethod
        def release(key) -> bool:
            return _dll.Key_Release(key if isinstance(key, bytes) else key.encode())

        @staticmethod
        def click(key) -> bool:
            return _dll.Key_Click(key if isinstance(key, bytes) else key.encode())

        @staticmethod
        def type(text: str) -> bool:
            return _dll.Key_Type(text.encode())

        @staticmethod
        def hotkey(*keys, delay_ms=50) -> bool:
            keys_bytes = [k if isinstance(k, bytes) else k.encode() for k in keys]
            key_arr = (ctypes.c_char_p * len(keys_bytes))(*keys_bytes)
            return _dll.Key_Hotkey(key_arr, len(keys_bytes), delay_ms)


# ------------------ 自动打开（可选） ------------------
try:
    HIDDevice.open()
except RuntimeError as e:
    print(e)
    raise
# ------------------ 测试入口 ------------------
if __name__ == "__main__":
    try:
        time.sleep(1)
        # HIDDevice.mouse.move(100, 50)
        # HIDDevice.mouse.click(HIDDevice.mouse.LEFT)
        # HIDDevice.keyboard.type("Hello Arduino Static!")
        HIDDevice.keyboard.hotkey("LCTRL", "LALT", "DELETE")
    finally:
        HIDDevice.close()
