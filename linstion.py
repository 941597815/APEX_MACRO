import os
import winsound
import time
from raw_input import keyboard, mouse
from macro import huanjia, SG, ReloadSpeedUp
from utils import is_mouse_at_screen_center, precise_sleep

exclude_kb = [
    {"vid": 0x046D, "pid": 0xC08B},  # 排除这个键盘
    # {"vid": 0x1532},  # 排除该厂商所有键盘设备
]
# exclude_mouse = [{"vid": 0x046D, "pid": 0xC08B}]

alt_pressed = False
ctrl_pressed = False
caps_lock = False
old_time = time.time()
e_status = False


# 鼠标点击回调函数
def on_click(x, y, button, pressed, globals_instance):
    # print(f"x:{x},y:{y},button:{button},pressed:{pressed}")

    if globals_instance.Jitter == "YES":
        if button == "left":
            if pressed:
                globals_instance.mouse_L = True
                if globals_instance.mouse_R and globals_instance.douqiang:
                    globals_instance.running = True
                # print("开始")
            else:
                globals_instance.running = False
                globals_instance.mouse_L = False

                # print("结束")
        if button == "right":
            if pressed:
                globals_instance.mouse_R = True
                if globals_instance.mouse_L and globals_instance.douqiang:
                    globals_instance.running = True

            else:
                globals_instance.mouse_R = False
                globals_instance.running = False

    if globals_instance.QuickPickup == "YES" and button == "x1":
        if pressed:
            globals_instance.mouse_x1 = True
            globals_instance.e = True
        else:
            globals_instance.mouse_x1 = False
            globals_instance.e = False
    if globals_instance.AerialSteering == "YES" and button == "x2":
        if pressed:
            globals_instance.mouse_x2 = True
            globals_instance.zhuanxiang = True
        else:
            globals_instance.mouse_x2 = False
            globals_instance.zhuanxiang = False
            if globals_instance.w:
                globals_instance.device.keyboard.press(
                    globals_instance.device.keyboard.W
                )
                globals_instance.device.keyboard.click(
                    globals_instance.device.keyboard.LSHIFT
                )
            else:
                globals_instance.device.keyboard.release(
                    globals_instance.device.keyboard.W
                )


def on_scroll(x, y, delta, globals_instance):
    global old_time

    # print(f"x:{x},y:{y},delta:{delta}")

    # 不能与其他宏一起调用，否则卡死
    if (
        globals_instance.SuperGlide == "YES"
        and delta > 0
        and globals_instance.status
        and not globals_instance.zhuanxiang
        and not globals_instance.e
    ):
        # 避免频繁触发
        # print(time.time() - old_time)
        if time.time() - old_time > 0.5:
            old_time = time.time()
            SG()
        return


def on_press(key, globals_instance):
    global alt_pressed, ctrl_pressed, caps_lock, old_time, e_status

    # print(f"[kb_press] {key}")

    # 检查按下的键是否是 Home 键
    if key == "home":
        globals_instance.device.close()
        winsound.Beep(800, 100)
        winsound.Beep(600, 100)
        winsound.Beep(400, 100)
        os._exit(0)  # 结束程序
    if key == "lalt":
        alt_pressed = True
    if key == "lctrl":
        ctrl_pressed = True
    if key == "lshift":
        globals_instance.shift_pressed = True
    if key == "space":
        globals_instance.space_pressed = True
    if globals_instance.Jitter == "YES" and key == "caps_lock":
        caps_lock = True
        globals_instance.douqiang = not globals_instance.douqiang
        if globals_instance.douqiang:
            winsound.Beep(800, 200)
        else:
            winsound.Beep(800, 100)
            winsound.Beep(600, 100)
    if (
        (key == "e")
        and globals_instance.status
        and globals_instance.shift_pressed
        and not globals_instance.mouse_x1
    ):  # 按住ctrl
        if not e_status:  # 按住e时只触发一次
            if globals_instance.QuickRope == "YES":
                globals_instance.fast_rope = True
            e_status = True
        precise_sleep(0.011)
        globals_instance.fast_rope = False

    if globals_instance.AerialSteering == "YES" and key == "w":
        globals_instance.w = True

    if key == "a":
        globals_instance.a = True

    if key == "s":
        globals_instance.s = True

    if key == "d":
        globals_instance.d = True


def on_release(key, globals_instance):
    global alt_pressed, ctrl_pressed, caps_lock, e_status

    # print(f"[kb_release] {key}")

    if key == "lalt":
        alt_pressed = False
        # print('altUp')
    if key == "lctrl":
        ctrl_pressed = False
    if key == "lshift":
        globals_instance.shift_pressed = False
    if key == "caps_lock":
        caps_lock = False
    if key == "space":
        globals_instance.space_pressed = False
    # if key == "r":
    #     ReloadSpeedUp()

    if key == "e":
        if globals_instance.QuickRope == "YES":
            e_status = False

        if globals_instance.ArmorChange == "YES":
            globals_instance.fast_rope = False

            if is_mouse_at_screen_center(10) and not globals_instance.status:
                precise_sleep(0.01)
                huanjia(globals_instance)

    if key == "w":
        globals_instance.w = False
        globals_instance.device.keyboard.release(globals_instance.device.keyboard.W)

    if key == "a":
        globals_instance.a = False
        globals_instance.device.keyboard.release(globals_instance.device.keyboard.A)

    if key == "s":
        globals_instance.s = False
        globals_instance.device.keyboard.release(globals_instance.device.keyboard.S)

    if key == "d":
        globals_instance.d = False
        globals_instance.device.keyboard.release(globals_instance.device.keyboard.D)


def start_linstions(globals_instance):

    kb_listener = keyboard.Listener(
        on_press=lambda key: on_press(key, globals_instance),
        on_release=lambda key: on_release(key, globals_instance),
        exclude_devices=exclude_kb,
    )
    mouse_listener = mouse.Listener(
        on_click=lambda x, y, button, pressed: on_click(
            x, y, button, pressed, globals_instance
        ),
        on_scroll=lambda x, y, delta: on_scroll(x, y, delta, globals_instance),
        # exclude_devices=exclude_mouse,
    )

    kb_listener.start()
    mouse_listener.start()
