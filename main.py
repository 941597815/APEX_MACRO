import threading
import os
import time
from globals import globals_instance
from linstion import start_mouse_listener, start_keyboard
from macro import worker_macro
from utils import (
    get_mouse_shape,
    disable_keys,
    printLogo,
    precise_sleep,
    showMessage,
    hid_connected,
)
import HIDDevice as Device

if __name__ == "__main__":

    # 初始化device
    try:
        HIDDevice = Device.init(globals_instance.deviceType)
        if HIDDevice is not None:
            globals_instance.device = HIDDevice
    except Exception as e:
        print("出错了：", e)
        showMessage(f"{globals_instance.deviceType}_KM 设备未连接")
        os._exit(0)

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
    printLogo(globals_instance.deviceType)

    last_time = time.time()
    # 启动主进程
    while True:
        # 更新游戏状态
        globals_instance.status = get_mouse_shape() == 0

        # 每秒检查设备连接情况
        if (time.time() - last_time >= 1) and HIDDevice is not None:
            last_time = time.time()
            if not hid_connected(
                globals_instance.device.vid_pid[0],
                globals_instance.device.vid_pid[1],
            ):
                print("设备已断开！程序结束")
                disable_keys([0x14, 0x91])
                time.sleep(1)
                os._exit(0)  # 结束程序

        # 循环间隔
        precise_sleep(0.008)
