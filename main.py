from globals import globals_instance
import threading
import time
from linstion import start_mouse_listener, start_keyboard
from macro import worker_macro
from utils import get_mouse_shape, disable_keys, printLogo


if __name__ == "__main__":
    # 启动监听器线程
    listener_mouse_thread = threading.Thread(
        target=start_mouse_listener, args=(globals_instance,), daemon=True
    ).start()
    listener_keyboard_thread = threading.Thread(
        target=start_keyboard, args=(globals_instance,), daemon=True
    ).start()
    listener_macro_thread = threading.Thread(target=worker_macro, daemon=True).start()

    # 关闭按键指示灯
    disable_keys([0x14, 0x91])

    # print("启动完成")
    printLogo()
    while True:
        globals_instance.status = get_mouse_shape() == 0
        try:
            globals_instance.arduino.dev.read(1, timeout_ms=5)
        except OSError:
            print("设备已断开！程序结束")
            disable_keys([0x14, 0x91])
            # time.sleep(1)
            break

        time.sleep(0.008)
