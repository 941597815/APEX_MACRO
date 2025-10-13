import os
import winsound
import time
from pynput import mouse, keyboard
from macro import huanjia, SG, ReloadSpeedUp, jump
from utils import is_mouse_at_screen_center, precise_sleep

alt_pressed = False
ctrl_pressed = False
shift_pressed = False
caps_lock = False
timer = None
timer_E = None
network_restrictions = False
old_time = time.time()
# mouse_R = False
# mouse_L = False
keyboard_ws = False
# douqiang = False
huanjia_status = False
e_status = False
w_status = False


# 鼠标点击回调函数
def on_click(x, y, button, pressed, globals_instance):
    # global mouse_R, mouse_L, douqiang

    if button == mouse.Button.left:  # 检测鼠标左键
        if pressed:
            globals_instance.mouse_L = True
            if globals_instance.mouse_R and globals_instance.douqiang:
                globals_instance.running = True
            # print("开始")
        else:
            globals_instance.running = False
            globals_instance.mouse_L = False

            # print("结束")
    if button == mouse.Button.right:
        if pressed:
            globals_instance.mouse_R = True
            if globals_instance.mouse_L and globals_instance.douqiang:
                globals_instance.running = True

        else:
            globals_instance.mouse_R = False
            globals_instance.running = False

    if button == mouse.Button.x1:
        if pressed:
            globals_instance.e = True
        else:
            globals_instance.e = False
    if button == mouse.Button.x2:
        if pressed:
            globals_instance.zhuanxiang = True
        else:
            globals_instance.zhuanxiang = False


def on_scroll(x, y, dx, dy, globals_instance):
    global old_time

    # print(dy)
    # 不能与其他宏一起调用，否则卡死
    if (
        dy > 0
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


# 鼠标监听器线程
def start_mouse_listener(globals_instance):
    listener = mouse.Listener(
        on_click=lambda x, y, button, pressed: on_click(
            x, y, button, pressed, globals_instance
        ),
        on_scroll=lambda x, y, dx, dy: on_scroll(x, y, dx, dy, globals_instance),
    )
    listener.start()
    listener.join()


def on_press(key, globals_instance):
    global alt_pressed, ctrl_pressed, shift_pressed, caps_lock, timer, network_restrictions, old_time, keyboard_ws, huanjia_status, timer_E, w_status

    # 检查按下的键是否是 Home 键
    if key == keyboard.Key.home:
        globals_instance.device.close()
        winsound.Beep(800, 100)
        winsound.Beep(600, 100)
        winsound.Beep(400, 100)
        os._exit(0)  # 结束程序
    if key == keyboard.Key.alt_l:
        alt_pressed = True
    if key == keyboard.Key.ctrl_l:
        ctrl_pressed = True
    if key == keyboard.Key.shift_l:
        shift_pressed = True
    if key == keyboard.Key.caps_lock:
        caps_lock = True
        globals_instance.douqiang = not globals_instance.douqiang
        if globals_instance.douqiang:
            winsound.Beep(800, 200)
        else:
            winsound.Beep(800, 100)
            winsound.Beep(600, 100)
    # if key == keyboard.Key.f9:
    if key == keyboard.Key.scroll_lock:
        huanjia_status = not huanjia_status
        if huanjia_status:
            winsound.Beep(800, 200)
        else:
            winsound.Beep(800, 100)
            winsound.Beep(600, 100)
    if (
        shift_pressed
        and (
            key == keyboard.KeyCode.from_char("e")
            or key == keyboard.KeyCode.from_char("E")  # or按住shift
            or key == keyboard.KeyCode.from_char("\x05")
        )
        and globals_instance.status
    ):  # 按住ctrl
        jump()
    if (
        key == keyboard.KeyCode.from_char("w")
        or key == keyboard.KeyCode.from_char("W")
        or key == keyboard.KeyCode.from_char("\x17")
    ):
        w_status = True


def on_release(key, globals_instance):
    global alt_pressed, ctrl_pressed, shift_pressed, caps_lock, huanjia_status, w_status

    # print(str(key) == str(keyboard.KeyCode(vk=49)))
    # print(str(key))
    if key == keyboard.Key.alt_l:
        alt_pressed = False
        # print('altUp')
    if key == keyboard.Key.ctrl_l:
        ctrl_pressed = False
    if key == keyboard.Key.shift_l:
        shift_pressed = False
    if key == keyboard.Key.caps_lock:
        caps_lock = False
    # if key == keyboard.KeyCode.from_char("r") or key == keyboard.KeyCode.from_char("R"):
    #     ReloadSpeedUp()
    if (
        key == keyboard.KeyCode.from_char("w")
        or key == keyboard.KeyCode.from_char("W")
        or key == keyboard.KeyCode.from_char("\x17")
    ):
        w_status = False
    if (
        huanjia_status
        and is_mouse_at_screen_center(10)
        and (
            key == keyboard.KeyCode.from_char("e")
            or key == keyboard.KeyCode.from_char("E")  # 按住lshift
            or key == keyboard.KeyCode.from_char("\x05")  # 按住lctrl
        )
    ):
        precise_sleep(0.01)
        if not globals_instance.status:
            huanjia(globals_instance)


def start_keyboard(globals_instance):
    listener = keyboard.Listener(
        on_press=lambda key: on_press(key, globals_instance),
        on_release=lambda key: on_release(key, globals_instance),
    )
    listener.start()
    listener.join()
