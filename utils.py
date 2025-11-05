import win32gui
import win32api
import time
import math
import random
import ctypes
import tkinter as tk
from tkinter import messagebox
import hid
import cv2
import numpy as np
import mss


def printLogo(device):

    if device == "RP2040":
        logo = r"""     


 █████╗ ██████╗ ███████╗██╗  ██╗
██╔══██╗██╔══██╗██╔════╝╚██╗██╔╝
███████║██████╔╝█████╗   ╚███╔╝ 
██╔══██║██╔═══╝ ██╔══╝   ██╔██╗ 
██║  ██║██║     ███████╗██╔╝ ██╗
╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝
                                                 
              RP2040

    """
    elif device == "RP2040_HOST":
        logo = r"""     


 █████╗ ██████╗ ███████╗██╗  ██╗
██╔══██╗██╔══██╗██╔════╝╚██╗██╔╝
███████║██████╔╝█████╗   ╚███╔╝ 
██╔══██║██╔═══╝ ██╔══╝   ██╔██╗ 
██║  ██║██║     ███████╗██╔╝ ██╗
╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝
                                                 
        RP2040/RP2350 HOST

    """
    elif device == "ARDUINO":
        logo = r"""     


 █████╗ ██████╗ ███████╗██╗  ██╗
██╔══██╗██╔══██╗██╔════╝╚██╗██╔╝
███████║██████╔╝█████╗   ╚███╔╝ 
██╔══██║██╔═══╝ ██╔══╝   ██╔██╗ 
██║  ██║██║     ███████╗██╔╝ ██╗
╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝
                                                 
        Arduino Pro Micro

    """
    print(logo)


def get_mouse_shape():
    # 获取鼠标光标形状
    cursor = win32gui.GetCursorInfo()
    # print(cursor)
    cursor_shape = cursor[1]
    return cursor_shape


def is_mouse_at_screen_center(tolerance=5):
    """
    判断鼠标是否在屏幕中心附近。

    :param tolerance: 允许的误差范围（像素），默认±5像素
    :return: True 表示在中心附近，False 表示不在
    """
    # 获取屏幕分辨率
    screen_width = win32api.GetSystemMetrics(0)
    screen_height = win32api.GetSystemMetrics(1)

    # 计算屏幕中心坐标
    center_x = screen_width // 2
    center_y = screen_height // 2

    # 获取当前鼠标位置
    mouse_x, mouse_y = win32gui.GetCursorPos()

    # 判断是否在中心附近（考虑误差范围）
    return abs(mouse_x - center_x) <= tolerance and abs(mouse_y - center_y) <= tolerance


def is_app_active(app_name):
    """
    判断指定的应用程序是否在前台且处于激活状态
    :param app_name: 应用程序的窗口标题或进程名称
    :return: True 或 False
    """
    # 获取当前前台窗口的句柄
    hwnd = win32gui.GetForegroundWindow()
    if hwnd == 0:
        return False  # 没有前台窗口
    # 获取前台窗口的标题
    window_title = win32gui.GetWindowText(hwnd)
    # print(hwnd, window_title)

    # 检查窗口标题是否包含目标应用名称
    if app_name.lower() in window_title.lower():
        return True

    return False


def truncated_normal_random(m, n):
    """高性能的正态分布随机数生成器"""
    if m >= n:
        raise ValueError("范围上限必须大于下限")

    mean = (m + n) / 2
    sigma = (n - m) / (2 * 1.645)  # 使用预计算的1.645优化

    # 使用高效的正态分布转换
    z0 = math.sqrt(-2.0 * math.log(random.random())) * math.cos(
        2.0 * math.pi * random.random()
    )
    value = round(mean + z0 * sigma)

    return max(m, min(n, value))  # 截断边界


def random_delay_ms(min_ms, max_ms):
    """优化的毫秒级延迟函数"""
    delay_ms = truncated_normal_random(min_ms, max_ms)
    precise_sleep(delay_ms / 1000)
    return delay_ms


def game_status():
    return (get_mouse_shape() == 0) and is_app_active("穿越火线")


def disable_keys(keys):
    """
    把指定列表中当前处于“开”状态的锁键关闭。
    目前仅支持 Caps Lock / Num Lock / Scroll Lock
    参数 keys: 可迭代对象,元素为虚拟键码(int)
    """
    # 只处理我们认识的那三个锁键
    LOCK_KEYS = {0x14, 0x90, 0x91}  # Caps, Num, Scroll
    for vk in keys:
        if vk not in LOCK_KEYS:
            continue
        # 当前是否“开”
        if ctypes.windll.user32.GetKeyState(vk) & 1:
            # 模拟一次按键：按下然后立即释放，实现状态翻转
            ctypes.windll.user32.keybd_event(vk, 0, 0, 0)  # KEYDOWN
            ctypes.windll.user32.keybd_event(vk, 0, 2, 0)  # KEYUP


def precise_sleep(duration, precision: float = 0.0001, get_now=time.perf_counter):
    """
    自适应补偿的精确 sleep

    :param duration:  需要休眠的总时长（秒）
    :param precision: 最大允许忙等时长（秒），也是误差上限
    :param get_now:   时间源，默认 time.perf_counter
    """
    end = get_now() + duration
    while True:
        remaining = end - get_now()
        if remaining <= 0:
            break
        if remaining > precision:  # 真正可控的 sleep 时长
            time.sleep(remaining - precision)


def showMessage(msg: str, title="提示"):
    # 隐藏主窗口
    root = tk.Tk()
    root.withdraw()

    # 弹出提示框
    messagebox.showinfo(title, msg)


def hid_connected(vid: int, pid: int) -> bool:
    return any(
        d["vendor_id"] == vid and d["product_id"] == pid for d in hid.enumerate()
    )


def template_exists(template_path, threshold=0.8, region=None):
    """True-存在，False-不存在"""
    with mss.mss() as sct:
        monitor = region if region else sct.monitors[0]
        hay = cv2.cvtColor(np.array(sct.grab(monitor)), cv2.COLOR_BGRA2BGR)
    tpl = cv2.imread(template_path, cv2.IMREAD_COLOR)
    if tpl is None:
        raise FileNotFoundError(template_path)
    res = cv2.matchTemplate(hay, tpl, cv2.TM_CCOEFF_NORMED)
    return res.max() >= threshold


if __name__ == "__main__":
    # random_delay_ms(100, 800)
    # disable_keys([0x14, 0x91])
    # time.sleep(3)
    # print(get_mouse_shape())
    # # showMessage("123123123123123123")

    # if hid_connected(0x046D, 0xC08F):
    #     print("已连接")
    # else:
    #     print("未连接")
    import HIDDevice as Device
    from globals import globals_instance

    HIDDevice = Device.init(globals_instance.deviceType)
    while 1:
        a = template_exists("imgs/lctrl.png", 0.98, region=(914, 546, 966, 572))
        # print(a)
        if a:
            # HIDDevice.keyboard.click(HIDDevice.keyboard.LCTRL)
            precise_sleep(0.015)
            HIDDevice.keyboard.press(HIDDevice.keyboard.SPACE)
            precise_sleep(0.003)
            HIDDevice.keyboard.click(HIDDevice.keyboard.C)
            HIDDevice.keyboard.release(HIDDevice.keyboard.SPACE)
