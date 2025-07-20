import serial
import time
from serial.tools import list_ports


class HIDDevice:
    class Mouse:

        LEFT = "LEFT"
        RIGHT = "RIGHT"
        MIDDLE = "MIDDLE"

        def __init__(self, serial_conn):
            self.serial = serial_conn

        def wheel(self, a):
            """
              鼠标滚轮
            :param wheel: 滚轮移动量
            """
            self.serial.write(f"MOVE:{0},{0},{a}\n".encode())

        def move(self, x, y):
            """
              移动鼠标
            :param x: X轴移动量
            :param y: Y轴移动量
            """
            if x == 0 and y == 0:
                return
            # 分段调用 move 函数
            while abs(x) > 127 or abs(y) > 127:
                # 计算当前步长
                step_x = 127 if x > 0 else -127
                step_y = 127 if y > 0 else -127
                # 调用 move 函数
                # driver.move(step_x, step_y)
                self.serial.write(f"MOVE:{step_x},{step_y},{0}\n".encode())
                # 更新 x 和 y
                x -= step_x
                y -= step_y
            # 调用 move 函数处理剩余的部分
            self.serial.write(f"MOVE:{x},{y},{0}\n".encode())

        def press(self, button=LEFT):
            """按下鼠标按钮"""
            self.serial.write(f"MOUSE_BTN:{button}:PRESS\n".encode())

        def release(self, button=LEFT):
            """释放鼠标按钮"""
            self.serial.write(f"MOUSE_BTN:{button}:RELEASE\n".encode())

        def click(self, button=LEFT):
            """点击鼠标按钮"""
            self.serial.write(f"MOUSE_BTN:{button}:CLICK\n".encode())

        def drag(
            self, start_x, start_y, end_x, end_y, button=LEFT, steps=10, delay=0.01
        ):
            """拖拽操作"""
            self.move(start_x, start_y)
            time.sleep(0.1)
            self.press(button)
            time.sleep(0.1)

            # 平滑移动到目标位置
            dx = (end_x - start_x) / steps
            dy = (end_y - start_y) / steps

            for i in range(steps):
                self.move(int(dx), int(dy))
                time.sleep(delay)

            self.release(button)

    class Keyboard:

        # 字母键
        A = "A"
        B = "B"
        C = "C"
        D = "D"
        E = "E"
        F = "F"
        G = "G"
        H = "H"
        I = "I"
        J = "J"
        K = "K"
        L = "L"
        M = "M"
        N = "N"
        O = "O"
        P = "P"
        Q = "Q"
        R = "R"
        S = "S"
        T = "T"
        U = "U"
        V = "V"
        W = "W"
        X = "X"
        Y = "Y"
        Z = "Z"

        # 数字键
        KEY_0 = "0"
        KEY_1 = "1"
        KEY_2 = "2"
        KEY_3 = "3"
        KEY_4 = "4"
        KEY_5 = "5"
        KEY_6 = "6"
        KEY_7 = "7"
        KEY_8 = "8"
        KEY_9 = "9"

        # 功能键
        ENTER = "ENTER"
        ESC = "ESC"
        BACKSPACE = "BACKSPACE"
        TAB = "TAB"
        SPACE = "SPACE"
        MINUS = "MINUS"
        EQUAL = "EQUAL"
        LEFTBRACE = "LEFTBRACE"
        RIGHTBRACE = "RIGHTBRACE"
        BACKSLASH = "BACKSLASH"
        SEMICOLON = "SEMICOLON"
        QUOTE = "QUOTE"
        TILDE = "TILDE"
        COMMA = "COMMA"
        PERIOD = "PERIOD"
        SLASH = "SLASH"
        CAPSLOCK = "CAPSLOCK"

        # F键
        F1 = "F1"
        F2 = "F2"
        F3 = "F3"
        F4 = "F4"
        F5 = "F5"
        F6 = "F6"
        F7 = "F7"
        F8 = "F8"
        F9 = "F9"
        F10 = "F10"
        F11 = "F11"
        F12 = "F12"

        # 其他功能键
        PRINTSCREEN = "PRINTSCREEN"
        SCROLLLOCK = "SCROLLLOCK"
        PAUSE = "PAUSE"
        INSERT = "INSERT"
        HOME = "HOME"
        PAGEUP = "PAGEUP"
        DELETE = "DELETE"
        END = "END"
        PAGEDOWN = "PAGEDOWN"

        # 方向键
        RIGHT = "RIGHT"
        LEFT = "LEFT"
        DOWN = "DOWN"
        UP = "UP"

        # 小键盘
        NUMLOCK = "NUMLOCK"
        KPDIVIDE = "KPDIVIDE"
        KPMULTIPLY = "KPMULTIPLY"
        KPSUBTRACT = "KPSUBTRACT"
        KPADD = "KPADD"
        KPDECIMAL = "KPDECIMAL"
        KPENTER = "KPENTER"
        KP1 = "KP1"
        KP2 = "KP2"
        KP3 = "KP3"
        KP4 = "KP4"
        KP5 = "KP5"
        KP6 = "KP6"
        KP7 = "KP7"
        KP8 = "KP8"
        KP9 = "KP9"
        KP0 = "KP0"

        # 菜单键
        MENU = "MENU"

        # 修饰键
        LCTRL = "LCTRL"
        LSHIFT = "LSHIFT"
        LALT = "LALT"
        LGUI = "LGUI"
        RCTRL = "RCTRL"
        RSHIFT = "RSHIFT"
        RALT = "RALT"
        RGUI = "RGUI"

        def __init__(self, serial_conn):
            self.serial = serial_conn

        def press(self, key):
            """按下键盘按键"""
            self.serial.write(f"KEY:{key}:PRESS\n".encode())

        def release(self, key):
            """释放键盘按键"""
            self.serial.write(f"KEY:{key}:RELEASE\n".encode())

        def click(self, key):
            """点击键盘按键（按下并释放）"""
            self.serial.write(f"KEY:{key}:CLICK\n".encode())

        def type(self, text):
            """输入字符串"""
            self.serial.write(f"TYPE:{text}\n".encode())

        def hotkey(self, *keys, delay=0.05):
            """按下组合键"""
            for key in keys:
                self.press(key)
                time.sleep(delay)

            time.sleep(0.1)

            for key in reversed(keys):
                self.release(key)
                time.sleep(delay)

    def __init__(self, port=None, baudrate=115200):
        if port is None:
            port = self.find_arduino()
        self.serial = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2)  # 等待Arduino初始化
        print("Arduino初始化完成")
        self.mouse = self.Mouse(self.serial)
        self.keyboard = self.Keyboard(self.serial)

    @staticmethod
    def find_arduino():
        """自动检测Arduino Pro Micro"""
        ports = list_ports.comports()
        for p in ports:
            # Arduino Pro Micro的常见ID
            if "2341:8037" in p.hwid or "2341:8036" in p.hwid or "046D:C08B" in p.hwid:
                return p.device
        raise Exception("Arduino设备未找到")

    def release_all(self):
        """释放所有按键"""
        self.serial.write("RELEASE_ALL\n".encode())

    def close(self):
        """关闭连接"""
        self.release_all()
        self.serial.close()


# 使用示例
if __name__ == "__main__":
    dev = HIDDevice()  # 自动检测端口

    # 鼠标操作示例
    dev.mouse.move(555, 0)  #
    dev.mouse.press()  # 按下左键
    dev.mouse.move(20, 30)  # 移动鼠标
    dev.mouse.release()  # 释放左键
    dev.mouse.click("RIGHT")
    dev.mouse.click("MIDDLE")
    dev.mouse.drag(0, 0, 100, 100)  # 拖拽操作

    # 键盘测试
    key_list = [
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z",
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "ENTER",
        "ESC",
        "BACKSPACE",
        "TAB",
        "SPACE",
        "MINUS",
        "EQUAL",
        "LEFTBRACE",
        "RIGHTBRACE",
        "BACKSLASH",
        "SEMICOLON",
        "QUOTE",
        "TILDE",
        "COMMA",
        "PERIOD",
        "SLASH",
        "CAPSLOCK",
        "F1",
        "F2",
        "F3",
        "F4",
        "F5",
        "F6",
        "F7",
        "F8",
        "F9",
        "F10",
        "F11",
        "F12",
        "PRINTSCREEN",
        "SCROLLLOCK",
        "PAUSE",
        "INSERT",
        "HOME",
        "PAGEUP",
        "DELETE",
        "END",
        "PAGEDOWN",
        "RIGHT",
        "LEFT",
        "DOWN",
        "UP",
        "NUMLOCK",
        "KPDIVIDE",
        "KPMULTIPLY",
        "KPSUBTRACT",
        "KPADD",
        "KPDECIMAL",
        "KPENTER",
        "KP1",
        "KP2",
        "KP3",
        "KP4",
        "KP5",
        "KP6",
        "KP7",
        "KP8",
        "KP9",
        "KP0",
        "MENU",
        "LCTRL",
        "LSHIFT",
        "LALT",
        "LGUI",
        "RCTRL",
        "RSHIFT",
        "RALT",
        "RGUI",
    ]
    print("测试所有按键")
    for key in key_list:
        # print(key)
        dev.keyboard.press(key)
        dev.keyboard.release(key)
        time.sleep(0.1)
    time.sleep(1)
    # 组合键
    print("测试组合按键")
    dev.keyboard.press("LALT")  # 按下左Ctrl
    dev.keyboard.click(dev.keyboard.TAB)  # 点击C键
    dev.keyboard.release("LALT")  # 释放左Ctrl
    time.sleep(1)
    # 输入文本
    print("测试输入文本")
    dev.keyboard.type("Hello Arduino HID!")
    time.sleep(1)
    print("所有测试完成")

    dev.close()
