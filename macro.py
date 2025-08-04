import time
import random
from globals import globals_instance
from Arduino import HIDDevice
from utils import random_delay_ms, truncated_normal_random, Delay

arduino = HIDDevice()
globals_instance.arduino = arduino


def huanjia():
    if globals_instance.resolution == 1:
        n = 1
    elif globals_instance.resolution == 2:
        n = 2560 / 1920
    else:
        n = 1
    arduino.mouse.move(int(-580 * n), int(14 * n))
    random_delay_ms(3, 6)
    arduino.mouse.click()
    random_delay_ms(3, 6)
    arduino.mouse.move(0, int((72 - 14) * n))
    random_delay_ms(3, 6)
    arduino.mouse.click()
    random_delay_ms(3, 6)
    arduino.mouse.move(0, int((180 - 72) * n))
    random_delay_ms(3, 6)
    arduino.mouse.click()
    random_delay_ms(3, 6)
    arduino.mouse.move(0, int((282 - 180) * n))
    random_delay_ms(3, 6)
    arduino.mouse.click()
    random_delay_ms(3, 6)
    arduino.keyboard.click(arduino.keyboard.TAB)


def SG():
    arduino.keyboard.press(arduino.keyboard.SPACE)
    arduino.keyboard.click(arduino.keyboard.C)
    arduino.keyboard.release(arduino.keyboard.SPACE)


def yaqiang():
    arduino.mouse.move(0, truncated_normal_random(2, 5))


def dundun():
    if random.randint(0, 1):
        arduino.keyboard.press(arduino.keyboard.LCTRL)
        random_delay_ms(50, 300)
        arduino.keyboard.release(arduino.keyboard.LCTRL)
        random_delay_ms(150, 200)


def Scope():
    if random.randint(0, 1):
        arduino.mouse.press(arduino.mouse.RIGHT)
        random_delay_ms(80, 260)
        arduino.mouse.release(arduino.mouse.RIGHT)
        random_delay_ms(80, 260)


def ReloadSpeedUp():
    arduino.keyboard.click(arduino.keyboard.F1)
    random_delay_ms(880, 900)
    arduino.mouse.move(-10, 10)
    random_delay_ms(80, 100)
    arduino.mouse.click()


def worker_macro():
    while True:
        if globals_instance.status:
            if globals_instance.running:
                num = truncated_normal_random(3, 5)
                arduino.mouse.move(num, num)
                random_delay_ms(1, 4)
                arduino.mouse.move(-1 * num, -1 * num)
                random_delay_ms(1, 4)
                yaqiang()
                random_delay_ms(1, 4)
            elif globals_instance.mouse_L and not globals_instance.mouse_R:
                # dundun()
                # Scope()
                pass

            if globals_instance.e:
                arduino.keyboard.click(arduino.keyboard.E)
                random_delay_ms(5, 10)

            if globals_instance.zhuanxiang:
                arduino.keyboard.click(arduino.keyboard.SPACE)
                random_delay_ms(0, 5)
                arduino.keyboard.press(arduino.keyboard.LSHIFT)
                for i in range(truncated_normal_random(3, 7)):
                    arduino.keyboard.click(arduino.keyboard.W)
                    random_delay_ms(0, 5)
                arduino.keyboard.release(arduino.keyboard.LSHIFT)

            else:
                time.sleep(0.001)
        else:
            time.sleep(0.001)
