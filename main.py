from globals import globals_instance
import threading
import sys
from linstion import start_mouse_listener, start_keyboard
from macro import worker_macro
from utils import (
    get_mouse_shape,
    disable_keys,
    printLogo,
    precise_sleep,
)
from Arduino import HIDDevice


if __name__ == "__main__":

    # 初始化Arduino设备
    globals_instance.arduino = HIDDevice()

    # 启动监听器线程
    listener_mouse_thread = threading.Thread(
        target=start_mouse_listener, args=(globals_instance,), daemon=True
    ).start()
    listener_keyboard_thread = threading.Thread(
        target=start_keyboard, args=(globals_instance,), daemon=True
    ).start()
    listener_macro_thread = threading.Thread(
        target=worker_macro, args=(globals_instance,), daemon=True
    ).start()

    # 关闭按键指示灯
    disable_keys([0x14, 0x91])

    # 启动完成输出
    printLogo()

    # 启动主进程
    while True:
        globals_instance.status = get_mouse_shape() == 0
        try:
            data = globals_instance.arduino.dev.read(1, timeout_ms=3)
            # print("read ->", data)
        except OSError:
            print(OSError, "设备已断开！程序结束")
            disable_keys([0x14, 0x91])
            break

        precise_sleep(0.008)
