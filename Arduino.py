import hid
import time

VID_PID = (0x046D, 0xC08B)  # 罗技G102
# VID_PID = (0xCAFE, 0x4004)  # 罗技G102


# VID_PID = (0x046D, 0xC08F)  # 罗技G403 Logitech G403 Wired Gaming Mouse


def precise_sleep(duration, precision: float = 0.0001, get_now=time.perf_counter):
    """
    自适应补偿的精确 sleep, 用于解决time.sleep函数累计误差问题

    :param duration:  需要休眠的总时长（秒）
    :param precision: 最大允许忙等时长（秒），也是误差上限。 默认1ms
    :param get_now:   时间源，默认 time.perf_counter
    """
    end = get_now() + duration
    while True:
        remaining = end - get_now()
        if remaining <= 0:
            break
        if remaining > precision:  # 真正可控的 sleep 时长
            time.sleep(remaining - precision)


class HIDDevice:
    """HID 版本的键盘鼠标控制"""

    class Mouse:
        LEFT, RIGHT, MIDDLE = "LEFT", "RIGHT", "MIDDLE"

        def __init__(self, parent):
            self.parent = parent  # 指向 HIDDevice 实例

        def _send(self, cmd: str):
            self.parent._send(cmd)  # 调用父类公共方法

        def wheel(self, a):
            self._send(f"MOVE:0,0,{a}")

        def move(self, x, y):
            if x == 0 and y == 0:
                return
            # 先处理 x、y 均超过 127 的情况，逐轴拆解
            while abs(x) > 127 or abs(y) > 127:
                step_x = 0
                step_y = 0
                # 仅当 x 需要拆步时才拆
                if abs(x) > 127:
                    step_x = 127 if x > 0 else -127
                    x -= step_x
                # 仅当 y 需要拆步时才拆
                if abs(y) > 127:
                    step_y = 127 if y > 0 else -127
                    y -= step_y
                self._send(f"MOVE:{step_x},{step_y},0")
            # 剩余不足 127 的“尾量”一次性发完
            self._send(f"MOVE:{x},{y},0")

        def press(self, button=LEFT):
            self._send(f"MOUSE_BTN:{button}:PRESS")

        def release(self, button=LEFT):
            self._send(f"MOUSE_BTN:{button}:RELEASE")

        def click(self, button=LEFT):
            self._send(f"MOUSE_BTN:{button}:CLICK")

        def drag(
            self, start_x, start_y, end_x, end_y, button=LEFT, steps=10, delay=0.01
        ):
            self.move(start_x, start_y)
            precise_sleep(0.1)
            self.press(button)
            precise_sleep(0.1)
            dx = (end_x - start_x) / steps
            dy = (end_y - start_y) / steps
            for _ in range(steps):
                self.move(int(dx), int(dy))
                precise_sleep(delay)
            self.release(button)

    class Keyboard:
        # 所有键名与原来保持一致
        A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z = (
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
        )
        KEY_0, KEY_1, KEY_2, KEY_3, KEY_4, KEY_5, KEY_6, KEY_7, KEY_8, KEY_9 = (
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
        )
        # 其他键同理……
        ENTER, ESC, BACKSPACE, TAB, SPACE = "ENTER", "ESC", "BACKSPACE", "TAB", "SPACE"
        F1, F2, F3, F4, F5, F6, F7, F8, F9, F10, F11, F12 = (
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
        )
        LCTRL, LSHIFT, LALT, LGUI, RCTRL, RSHIFT, RALT, RGUI = (
            "LCTRL",
            "LSHIFT",
            "LALT",
            "LGUI",
            "RCTRL",
            "RSHIFT",
            "RALT",
            "RGUI",
        )

        def __init__(self, parent):
            self.parent = parent

        def _send(self, cmd: str):
            self.parent._send(cmd)

        def press(self, key):
            self._send(f"KEY:{key}:PRESS")

        def release(self, key):
            self._send(f"KEY:{key}:RELEASE")

        def click(self, key):
            self._send(f"KEY:{key}:CLICK")

        def type(self, text):
            self._send(f"TYPE:{text}")

        def hotkey(self, *keys, delay=0.05):
            for k in keys:
                self.press(k)
                precise_sleep(delay)
            precise_sleep(0.1)
            for k in reversed(keys):
                self.release(k)
                precise_sleep(delay)

    def __init__(self, vid_pid=None):
        if vid_pid is None:
            vid_pid = VID_PID
        self.last_time = time.perf_counter()
        self.dev = hid.device()
        self.dev.open(*vid_pid)
        self.mouse = self.Mouse(self)
        self.keyboard = self.Keyboard(self)

    def release_all(self):
        self._send("RELEASE_ALL")

    def close(self):
        self.release_all()
        self.dev.close()

    def _send(self, cmd: str):
        # 第 0 字节放 Report ID 0，后面跟命令
        buf = b"\x00" + (cmd + "\n").encode()
        buf = buf.ljust(64, b"\0")[:64]
        # Windows 会把 < 1 ms 的 HID 报文合并；给每条报文 ≥ 1 ms 间隔即可彻底解决“有时arudino收不到报文”的问题。
        if time.perf_counter() - self.last_time <= 0.001:
            precise_sleep(0.001)
        # 距离上次发送的时间大于1ms才发送本次命令
        self.dev.write(buf)
        self.last_time = time.perf_counter()
        # print(">>>", repr(buf))


# ----------------- 示例 -----------------
if __name__ == "__main__":
    dev = HIDDevice()
    time.sleep(1)
    # 鼠标操作示例
    # dev.mouse.move(255, 0)  #
    # dev.mouse.press()  # 按下左键
    # dev.mouse.move(20, 30)  # 移动鼠标
    # dev.mouse.release()  # 释放左键
    # dev.mouse.click("RIGHT")
    # dev.mouse.click("MIDDLE")
    # dev.mouse.drag(0, 0, 100, 100)  # 拖拽操作

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
    # print("测试所有按键")
    # for key in key_list:
    #     # print(key)
    #     dev.keyboard.press(key)
    #     dev.keyboard.release(key)
    #     time.sleep(0.1)
    # time.sleep(1)
    # 组合键
    print("测试组合按键")
    # dev.keyboard.press("LALT")
    # dev.keyboard.click(dev.keyboard.TAB)
    # dev.keyboard.release("LALT")
    # time.sleep(1)
    # 输入文本
    print("测试输入文本")
    dev.keyboard.type("Hello Arduino HID!")
    # time.sleep(1)
    # print("所有测试完成")

    dev.close()
