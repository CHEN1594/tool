import pydirectinput
import random
import time

def press_i():
    pydirectinput.keyDown('i')
    time.sleep(0.05)
    pydirectinput.keyUp('i')

def press_ai():
    pydirectinput.keyDown('a')
    time.sleep(0.02)
    pydirectinput.keyDown('i')
    time.sleep(0.05)
    pydirectinput.keyUp('i')
    time.sleep(0.02)
    pydirectinput.keyUp('a')

def press_di():
    pydirectinput.keyDown('d')
    time.sleep(0.02)
    pydirectinput.keyDown('i')
    time.sleep(0.05)
    pydirectinput.keyUp('i')
    time.sleep(0.02)
    pydirectinput.keyUp('d')

combos = [press_i, press_ai, press_di]
weights = [0.6, 0.2, 0.2]  # 概率权重：i=60%，ai=20%，di=20%

while True:
    action = random.choices(combos, weights=weights, k=1)[0]
    action()
    time.sleep(random.uniform(0.05, 0.1))
