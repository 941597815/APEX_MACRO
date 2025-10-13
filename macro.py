import time
import random

from globals import Globals
from utils import random_delay_ms, truncated_normal_random, precise_sleep


device = None


def huanjia(globals_instance):
    if globals_instance.resolution == 1:
        n = 1
    elif globals_instance.resolution == 2:
        n = 2560 / 1920
    else:
        n = 1
    device.mouse.move(int(-580 * n), int(14 * n))
    random_delay_ms(13, 16)
    device.mouse.click()
    random_delay_ms(13, 16)
    device.mouse.move(0, int((72 - 14) * n))
    random_delay_ms(13, 16)
    device.mouse.click()
    random_delay_ms(13, 16)
    device.mouse.move(0, int((180 - 72) * n))
    random_delay_ms(13, 16)
    device.mouse.click()
    random_delay_ms(13, 16)
    device.mouse.move(0, int((282 - 180) * n))
    random_delay_ms(13, 16)
    device.mouse.click()
    random_delay_ms(13, 16)
    device.keyboard.click(device.keyboard.TAB)


def SG():
    device.keyboard.press(device.keyboard.SPACE)
    # precise_sleep(0.01)
    device.keyboard.click(device.keyboard.C)
    # precise_sleep(0.007)
    device.keyboard.release(device.keyboard.SPACE)


def jump():
    for i in range(truncated_normal_random(5, 12)):
        device.keyboard.click(device.keyboard.SPACE)
        random_delay_ms(0, 5)


def yaqiang():
    device.mouse.move(0, truncated_normal_random(1, 3))


def dundun():
    if random.randint(0, 1):
        device.keyboard.press(device.keyboard.LCTRL)
        random_delay_ms(50, 300)
        device.keyboard.release(device.keyboard.LCTRL)
        random_delay_ms(150, 200)


def Scope():
    if random.randint(0, 1):
        device.mouse.press(device.mouse.RIGHT)
        random_delay_ms(80, 260)
        device.mouse.release(device.mouse.RIGHT)
        random_delay_ms(80, 260)


def ReloadSpeedUp():
    device.keyboard.click(device.keyboard.F1)
    random_delay_ms(880, 900)
    device.mouse.move(-10, 10)
    random_delay_ms(80, 100)
    device.mouse.click()


def worker_macro(globals_instance: Globals):
    global device
    device = globals_instance.device
    last_time = time.time()
    while True:
        if globals_instance.status:
            if globals_instance.running:
                num = truncated_normal_random(3, 5)
                device.mouse.move(-num, num)
                random_delay_ms(1, 4)
                device.mouse.move(num, -num)
                random_delay_ms(1, 4)
                if time.time() - last_time < 1:
                    yaqiang()
                    random_delay_ms(1, 4)
            elif globals_instance.mouse_L and not globals_instance.mouse_R:
                # dundun()
                # Scope()
                pass
            else:
                last_time = time.time()

            if globals_instance.e:
                device.keyboard.click(device.keyboard.E)
                random_delay_ms(5, 10)

            if globals_instance.zhuanxiang:
                device.keyboard.click(device.keyboard.SPACE)
                random_delay_ms(0, 5)
                device.keyboard.press(device.keyboard.LSHIFT)
                for i in range(truncated_normal_random(3, 7)):
                    device.keyboard.click(device.keyboard.W)
                    random_delay_ms(0, 5)
                device.keyboard.release(device.keyboard.LSHIFT)

            else:
                precise_sleep(0.001)
        else:
            precise_sleep(0.001)
