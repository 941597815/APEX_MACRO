"""
HIDDevice 完整实现（与C++ DLL完全匹配）
用法：
    from hid_device import HIDDevice
    HIDDevice.open()          # 自动使用默认 VID/PID
    HIDDevice.mouse.move(100, 50)
    HIDDevice.keyboard.type("Hello")
    HIDDevice.close()
"""

import ctypes
import os
import time
from typing import Tuple, List

# ------------------ DLL 加载 ------------------
_dll = ctypes.CDLL(
    os.path.join(
        os.path.dirname(__file__), "./rp2040_host_dll.dll"
    )  # 修改为您的DLL路径
)

# ------------------ 原型声明 ------------------
# 设备管理
_dll.HID_Open.argtypes = [ctypes.c_ushort, ctypes.c_ushort]
_dll.HID_Open.restype = ctypes.c_bool
_dll.HID_Close.restype = None
_dll.HID_ReleaseAll.restype = ctypes.c_bool  # 注意这里是HID_ReleaseAll不是ReleaseAll

# 鼠标功能
_dll.Mouse_Move.argtypes = [ctypes.c_int, ctypes.c_int]
_dll.Mouse_Move.restype = ctypes.c_bool
_dll.Mouse_Wheel.argtypes = [ctypes.c_int]
_dll.Mouse_Wheel.restype = ctypes.c_bool
_dll.Mouse_Press.argtypes = [ctypes.c_uint8]
_dll.Mouse_Press.restype = ctypes.c_bool
_dll.Mouse_Release.argtypes = [ctypes.c_uint8]
_dll.Mouse_Release.restype = ctypes.c_bool
_dll.Mouse_Click.argtypes = [ctypes.c_uint8]
_dll.Mouse_Click.restype = ctypes.c_bool
_dll.Mouse_Drag.argtypes = [
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_uint8,
    ctypes.c_int,
    ctypes.c_int,
]
_dll.Mouse_Drag.restype = ctypes.c_bool
_dll.Mouse_ReleaseAll.restype = ctypes.c_bool

# 键盘功能
_dll.Key_Press.argtypes = [ctypes.c_uint8]
_dll.Key_Press.restype = ctypes.c_bool
_dll.Key_Release.argtypes = [ctypes.c_uint8]
_dll.Key_Release.restype = ctypes.c_bool
_dll.Key_Click.argtypes = [ctypes.c_uint8]
_dll.Key_Click.restype = ctypes.c_bool
_dll.Key_Hotkey.argtypes = [ctypes.POINTER(ctypes.c_uint8), ctypes.c_int, ctypes.c_int]
_dll.Key_Hotkey.restype = ctypes.c_bool
_dll.Key_ReleaseAll.restype = ctypes.c_bool

# 游戏手柄功能
_dll.Gamepad_ButtonPress.argtypes = [ctypes.c_uint32]
_dll.Gamepad_ButtonPress.restype = ctypes.c_bool
_dll.Gamepad_ButtonRelease.argtypes = [ctypes.c_uint32]
_dll.Gamepad_ButtonRelease.restype = ctypes.c_bool
_dll.Gamepad_SetLeftStick.argtypes = [ctypes.c_int8, ctypes.c_int8]
_dll.Gamepad_SetLeftStick.restype = ctypes.c_bool
_dll.Gamepad_SetRightStick.argtypes = [ctypes.c_int8, ctypes.c_int8]
_dll.Gamepad_SetRightStick.restype = ctypes.c_bool
_dll.Gamepad_SetTriggers.argtypes = [ctypes.c_int8, ctypes.c_int8]
_dll.Gamepad_SetTriggers.restype = ctypes.c_bool
_dll.Gamepad_SetHat.argtypes = [ctypes.c_uint8]
_dll.Gamepad_SetHat.restype = ctypes.c_bool
_dll.Gamepad_ReleaseAll.restype = ctypes.c_bool

# 数据读取
_dll.HID_Read.argtypes = [ctypes.POINTER(ctypes.c_uint8), ctypes.c_int]
_dll.HID_Read.restype = ctypes.c_int
_dll.HID_ParseMouseReport.argtypes = [
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.c_int,
    ctypes.POINTER(ctypes.c_int),
    ctypes.POINTER(ctypes.c_int),
    ctypes.POINTER(ctypes.c_int),
    ctypes.POINTER(ctypes.c_int),
    ctypes.POINTER(ctypes.c_int),
]
_dll.HID_ParseMouseReport.restype = ctypes.c_bool

# ------------------ 静态常量 ------------------
_DEFAULT_VID_PID = (0x046D, 0xC08B)  # 替换为您的设备VID/PID


# ------------------ 顶层类 ------------------
class HIDDevice:
    """HIDDevice 顶层静态类（全局单例）"""

    vid_pid = _DEFAULT_VID_PID

    # ---------- 设备管理 ----------
    @staticmethod
    def open(vid_pid: Tuple[int, int] = None) -> None:
        """
        打开HID设备
        :param vid_pid: 可选，指定设备的VID和PID元组
        """
        vid, pid = vid_pid or _DEFAULT_VID_PID
        if not _dll.HID_Open(vid, pid):
            raise RuntimeError(f"无法打开HID设备 (VID: 0x{vid:04X}, PID: 0x{pid:04X})")

    @staticmethod
    def close() -> None:
        """关闭HID设备"""
        _dll.HID_Close()

    @staticmethod
    def release_all() -> bool:
        """释放所有按键状态"""
        return _dll.HID_ReleaseAll()  # 使用HID_ReleaseAll而不是ReleaseAll

    # ---------- 静态鼠标 ----------
    class mouse:
        """鼠标操作静态类"""

        LEFT = 0x01
        RIGHT = 0x02
        MIDDLE = 0x04
        BACK = 0x08
        FORWARD = 0x10

        @staticmethod
        def move(x: int, y: int) -> bool:
            """
            移动鼠标指针
            :param x: 水平移动量（正数向右）
            :param y: 垂直移动量（正数向下）
            :return: 操作是否成功
            """
            return _dll.Mouse_Move(x, y)

        @staticmethod
        def wheel(scroll: int, pan: int = 0) -> bool:
            """
            滚动鼠标滚轮
            :param scroll: 垂直滚动量（正数向上）
            :param pan: 水平滚动量（正数向右）
            :return: 操作是否成功
            """
            return _dll.Mouse_Wheel(scroll, pan)

        @staticmethod
        def press(button: int = LEFT) -> bool:
            """
            按下鼠标按钮
            :param button: 按钮常量（LEFT/RIGHT/MIDDLE等）
            :return: 操作是否成功
            """
            return _dll.Mouse_Press(button)

        @staticmethod
        def release(button: int = LEFT) -> bool:
            """
            释放鼠标按钮
            :param button: 按钮常量
            :return: 操作是否成功
            """
            return _dll.Mouse_Release(button)

        @staticmethod
        def click(button: int = LEFT) -> bool:
            """
            点击鼠标按钮
            :param button: 按钮常量
            :param duration_ms: 点击持续时间（毫秒）
            :return: 操作是否成功
            """
            if not _dll.Mouse_Press(button):
                return False
            return _dll.Mouse_Release(button)

        @staticmethod
        def drag(
            x: int, y: int, button: int = LEFT, steps: int = 10, delay_ms: int = 10
        ) -> bool:
            """
            拖拽操作
            :param x: 水平移动量
            :param y: 垂直移动量
            :param button: 按住哪个按钮拖拽
            :param steps: 移动步数
            :param delay_ms: 每步之间的延迟（毫秒）
            :return: 操作是否成功
            """
            return _dll.Mouse_Drag(x, y, button, steps, delay_ms)

        @staticmethod
        def release_all() -> bool:
            """释放所有鼠标按钮"""
            return _dll.Mouse_ReleaseAll()

    # ---------- 静态键盘 ----------
    class keyboard:
        """键盘操作静态类"""

        # 字母键
        A = 0x04
        B = 0x05
        C = 0x06
        D = 0x07
        E = 0x08
        F = 0x09
        G = 0x0A
        H = 0x0B
        I = 0x0C
        J = 0x0D
        K = 0x0E
        L = 0x0F
        M = 0x10
        N = 0x11
        O = 0x12
        P = 0x13
        Q = 0x14
        R = 0x15
        S = 0x16
        T = 0x17
        U = 0x18
        V = 0x19
        W = 0x1A
        X = 0x1B
        Y = 0x1C
        Z = 0x1D

        # 数字键
        KEY_1 = 0x1E
        KEY_2 = 0x1F
        KEY_3 = 0x20
        KEY_4 = 0x21
        KEY_5 = 0x22
        KEY_6 = 0x23
        KEY_7 = 0x24
        KEY_8 = 0x25
        KEY_9 = 0x26
        KEY_0 = 0x27

        # 功能键
        ENTER = 0x28
        ESC = 0x29
        BACKSPACE = 0x2A
        TAB = 0x2B
        SPACE = 0x2C
        MINUS = 0x2D
        EQUAL = 0x2E
        LEFTBRACE = 0x2F
        RIGHTBRACE = 0x30
        BACKSLASH = 0x31
        SEMICOLON = 0x33
        QUOTE = 0x34
        TILDE = 0x35
        COMMA = 0x36
        PERIOD = 0x37
        SLASH = 0x38

        # 功能键
        CAPSLOCK = 0x39
        F1 = 0x3A
        F2 = 0x3B
        F3 = 0x3C
        F4 = 0x3D
        F5 = 0x3E
        F6 = 0x3F
        F7 = 0x40
        F8 = 0x41
        F9 = 0x42
        F10 = 0x43
        F11 = 0x44
        F12 = 0x45

        # 特殊键
        PRINTSCREEN = 0x46
        SCROLLLOCK = 0x47
        PAUSE = 0x48
        INSERT = 0x49
        HOME = 0x4A
        PAGEUP = 0x4B
        DELETE = 0x4C
        END = 0x4D
        PAGEDOWN = 0x4E
        RIGHT = 0x4F
        LEFT = 0x50
        DOWN = 0x51
        UP = 0x52

        # 小键盘
        KP0 = 0x62
        KP1 = 0x59
        KP2 = 0x5A
        KP3 = 0x5B
        KP4 = 0x5C
        KP5 = 0x5D
        KP6 = 0x5E
        KP7 = 0x5F
        KP8 = 0x60
        KP9 = 0x61
        KPENTER = 0x58
        KPDECIMAL = 0x63

        # 修饰键
        LCTRL = 0xE0
        LSHIFT = 0xE1
        LALT = 0xE2
        LGUI = 0xE3
        RCTRL = 0xE4
        RSHIFT = 0xE5
        RALT = 0xE6
        RGUI = 0xE7

        @staticmethod
        def press(key: int) -> bool:
            """
            按下键盘按键
            :param key: 键值常量
            :return: 操作是否成功
            """
            return _dll.Key_Press(key)

        @staticmethod
        def release(key: int) -> bool:
            """
            释放键盘按键
            :param key: 键值常量
            :return: 操作是否成功
            """
            return _dll.Key_Release(key)

        @staticmethod
        def click(key: int) -> bool:
            """
            点击键盘按键
            :param key: 键值常量
            :param duration_ms: 按键持续时间（毫秒）
            :return: 操作是否成功
            """
            if not _dll.Key_Press(key):
                return False
            return _dll.Key_Release(key)

        # @staticmethod
        # def type(text: str) -> bool:
        #     """
        #     输入文本
        #     :param text: 要输入的文本
        #     :return: 操作是否成功
        #     """
        #     return _dll.Key_Type(text.encode("utf-8"))

        @staticmethod
        def hotkey(*keys: int, delay_ms: int = 50) -> bool:
            """
            组合键操作
            :param keys: 要按下的键值常量
            :param delay_ms: 按键间延迟（毫秒）
            :return: 操作是否成功
            """
            key_arr = (ctypes.c_uint8 * len(keys))(*keys)
            return _dll.Key_Hotkey(key_arr, len(keys), delay_ms)

        @staticmethod
        def release_all() -> bool:
            """释放所有键盘按键"""
            return _dll.Key_ReleaseAll()

    # ---------- 静态游戏手柄 ----------
    class gamepad:
        """游戏手柄操作静态类（完整31按钮支持）"""

        # 完整32位按钮掩码定义（0-30）
        BUTTON_0 = 1 << 0  # A / South
        BUTTON_1 = 1 << 1  # B / East
        BUTTON_2 = 1 << 2  # C (保留)
        BUTTON_3 = 1 << 3  # X / North
        BUTTON_4 = 1 << 4  # Y / West
        BUTTON_5 = 1 << 5  # Z (保留)
        BUTTON_6 = 1 << 6  # TL (左肩键)
        BUTTON_7 = 1 << 7  # TR (右肩键)
        BUTTON_8 = 1 << 8  # TL2 (左扳机按钮)
        BUTTON_9 = 1 << 9  # TR2 (右扳机按钮)
        BUTTON_10 = 1 << 10  # Select
        BUTTON_11 = 1 << 11  # Start
        BUTTON_12 = 1 << 12  # Mode (Xbox键/PS键)
        BUTTON_13 = 1 << 13  # ThumbL (左摇杆按下)
        BUTTON_14 = 1 << 14  # ThumbR (右摇杆按下)
        BUTTON_15 = 1 << 15  # 保留
        BUTTON_16 = 1 << 16  # 保留
        BUTTON_17 = 1 << 17  # 保留
        BUTTON_18 = 1 << 18  # 保留
        BUTTON_19 = 1 << 19  # 保留
        BUTTON_20 = 1 << 20  # 保留
        BUTTON_21 = 1 << 21  # 保留
        BUTTON_22 = 1 << 22  # 保留
        BUTTON_23 = 1 << 23  # 保留
        BUTTON_24 = 1 << 24  # 保留
        BUTTON_25 = 1 << 25  # 保留
        BUTTON_26 = 1 << 26  # 保留
        BUTTON_27 = 1 << 27  # 保留
        BUTTON_28 = 1 << 28  # 保留
        BUTTON_29 = 1 << 29  # 保留
        BUTTON_30 = 1 << 30  # 保留（实际HID规范只到30）

        # 常用别名（兼容Xbox/PS布局）
        BUTTON_A = BUTTON_0  # Xbox A / PS Cross
        BUTTON_B = BUTTON_1  # Xbox B / PS Circle
        BUTTON_X = BUTTON_3  # Xbox X / PS Square
        BUTTON_Y = BUTTON_4  # Xbox Y / PS Triangle
        BUTTON_SOUTH = BUTTON_0  # 标准HID名称
        BUTTON_EAST = BUTTON_1
        BUTTON_NORTH = BUTTON_3
        BUTTON_WEST = BUTTON_4
        BUTTON_LB = BUTTON_6  # 左肩键
        BUTTON_RB = BUTTON_7  # 右肩键
        BUTTON_LT = BUTTON_8  # 左扳机按钮
        BUTTON_RT = BUTTON_9  # 右扳机按钮
        BUTTON_BACK = BUTTON_10  # Select/Back
        BUTTON_START = BUTTON_11
        BUTTON_GUIDE = BUTTON_12  # Xbox Guide/PS Home
        BUTTON_L3 = BUTTON_13  # 左摇杆按下
        BUTTON_R3 = BUTTON_14  # 右摇杆按下

        # 方向键状态（与HID规范完全一致）
        HAT_CENTERED = 0
        HAT_UP = 1
        HAT_UP_RIGHT = 2
        HAT_RIGHT = 3
        HAT_DOWN_RIGHT = 4
        HAT_DOWN = 5
        HAT_DOWN_LEFT = 6
        HAT_LEFT = 7
        HAT_UP_LEFT = 8

        @staticmethod
        def button_press(button: int) -> bool:
            """按下指定按钮（支持所有31个按钮）"""
            if button > (1 << 30):
                raise ValueError("按钮掩码值过大，最大支持31个按钮(0-30)")
            return _dll.Gamepad_ButtonPress(button)

        @staticmethod
        def button_release(button: int) -> bool:
            """释放指定按钮"""
            if button > (1 << 30):
                raise ValueError("按钮掩码值过大，最大支持31个按钮(0-30)")
            return _dll.Gamepad_ButtonRelease(button)

        @staticmethod
        def button_click(button: int, duration_ms: int = 100) -> bool:
            """
            点击游戏手柄按钮
            :param button: 按钮常量
            :param duration_ms: 点击持续时间（毫秒）
            :return: 操作是否成功
            """
            if not _dll.Gamepad_ButtonPress(button):
                return False
            time.sleep(duration_ms / 1000)
            return _dll.Gamepad_ButtonRelease(button)

        @staticmethod
        def set_left_stick(x: int, y: int) -> bool:
            """
            设置左摇杆位置
            :param x: 水平轴 (-127 到 127)
            :param y: 垂直轴 (-127 到 127)
            :return: 操作是否成功
            """
            return _dll.Gamepad_SetLeftStick(
                max(-127, min(127, x)), max(-127, min(127, y))
            )

        @staticmethod
        def set_right_stick(x: int, y: int) -> bool:
            """
            设置右摇杆位置
            :param x: 水平轴 (-127 到 127)
            :param y: 垂直轴 (-127 到 127)
            :return: 操作是否成功
            """
            return _dll.Gamepad_SetRightStick(
                max(-127, min(127, x)), max(-127, min(127, y))
            )

        @staticmethod
        def set_triggers(left: int, right: int) -> bool:
            """
            设置触发器值
            :param left: 左触发器 (-127 到 127)
            :param right: 右触发器 (-127 到 127)
            :return: 操作是否成功
            """
            return _dll.Gamepad_SetTriggers(
                max(-127, min(127, left)), max(-127, min(127, right))
            )

        @staticmethod
        def set_hat(direction: int) -> bool:
            """
            设置方向键状态
            :param direction: 方向常量（HAT_UP等）
            :return: 操作是否成功
            """
            if direction not in range(9):  # 0-8
                raise ValueError("方向值必须在0-8之间")
            return _dll.Gamepad_SetHat(direction)

        @staticmethod
        def hat_click(direction: int, duration_ms: int = 100) -> bool:
            """
            点击方向键
            :param direction: 方向常量
            :param duration_ms: 点击持续时间（毫秒）
            :return: 操作是否成功
            """
            if not _dll.Gamepad_SetHat(direction):
                return False
            time.sleep(duration_ms / 1000)
            return _dll.Gamepad_SetHat(HIDDevice.gamepad.HAT_CENTERED)

        # 便捷方向操作方法
        @staticmethod
        def hat_up() -> bool:
            """方向上"""
            return _dll.Gamepad_SetHat(HIDDevice.gamepad.HAT_UP)

        @staticmethod
        def hat_down() -> bool:
            """方向下"""
            return _dll.Gamepad_SetHat(HIDDevice.gamepad.HAT_DOWN)

        @staticmethod
        def hat_left() -> bool:
            """方向左"""
            return _dll.Gamepad_SetHat(HIDDevice.gamepad.HAT_LEFT)

        @staticmethod
        def hat_right() -> bool:
            """方向右"""
            return _dll.Gamepad_SetHat(HIDDevice.gamepad.HAT_RIGHT)

        @staticmethod
        def hat_center() -> bool:
            """方向回中"""
            return _dll.Gamepad_SetHat(HIDDevice.gamepad.HAT_CENTERED)

        @staticmethod
        def release_all() -> bool:
            """释放所有按钮和摇杆"""
            return _dll.Gamepad_ReleaseAll()

    @staticmethod
    def mouse_to_gamepad(data: int, cmd_id: int = 3) -> bool:
        buf = (ctypes.c_uint8 * 1)(data)
        return _dll.Mouse_To_Gamepad(buf, cmd_id)

    # ---------- 数据读取 ----------
    @staticmethod
    def read(buffer_size: int = 64) -> bytes:
        """
        读取HID数据
        :param buffer_size: 缓冲区大小
        :return: 读取到的数据
        """
        buf = (ctypes.c_uint8 * buffer_size)()
        size = _dll.HID_Read(buf, buffer_size)
        if size > 0:
            return bytes(buf[:size])
        return b""

    @staticmethod
    def parse_mouse_report(data: bytes) -> dict:
        """
        解析鼠标报告数据
        :param data: 原始报告数据
        :return: 解析后的字典或None
        """
        report_id = ctypes.c_int()
        buttons = ctypes.c_int()
        x = ctypes.c_int()
        y = ctypes.c_int()
        wheel = ctypes.c_int()

        buf = (ctypes.c_uint8 * len(data))(*data)
        if _dll.HID_ParseMouseReport(
            buf,
            len(data),
            ctypes.byref(report_id),
            ctypes.byref(buttons),
            ctypes.byref(x),
            ctypes.byref(y),
            ctypes.byref(wheel),
        ):
            return {
                "report_id": report_id.value,
                "buttons": buttons.value,
                "x": x.value,
                "y": y.value,
                "wheel": wheel.value,
            }
        return None


# ------------------ 自动打开（可选） ------------------
try:
    HIDDevice.open()
except RuntimeError as e:
    print(e)
    raise
# ------------------ 测试入口 ------------------
if __name__ == "__main__":
    try:
        # 初始化设备
        HIDDevice.open()
        # time.sleep(3)
        old = time.time()
        for i in range(100):
            HIDDevice.mouse.move(1, 1)
        print((time.time() - old) / 100)
        time.sleep(1)

        # print("测试鼠标点击")
        # HIDDevice.mouse.click(HIDDevice.mouse.LEFT)
        # time.sleep(1)

        # # 测试键盘
        # print("测试键盘输入A")
        # HIDDevice.keyboard.click(HIDDevice.keyboard.A)
        # time.sleep(1)

        # print("测试组合键Ctrl+C")
        # HIDDevice.keyboard.hotkey(HIDDevice.keyboard.LCTRL, HIDDevice.keyboard.C)
        # time.sleep(1)

        # # 测试游戏手柄
        # print("测试游戏手柄按钮A")
        # HIDDevice.gamepad.button_click(HIDDevice.gamepad.BUTTON_A)
        # time.sleep(1)

        # print("测试摇杆")
        # HIDDevice.gamepad.set_left_stick(100, -50)
        # time.sleep(1)
        # HIDDevice.gamepad.set_left_stick(0, 0)
        # HIDDevice.mouse_to_gamepad(0)
        # 测试数据读取
        # print("尝试读取数据...")
        # while 1:
        #     data = HIDDevice.read()
        #     if data:
        #         # print(f"收到数据: {data.hex()}")
        #         report = HIDDevice.parse_mouse_report(data)
        #         if report:
        #             print(f"解析结果: {report}", end="\r", flush=True)

    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        HIDDevice.release_all()
        HIDDevice.close()
