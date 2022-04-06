# Add your Python code here. E.g.
from microbit import *
import utime

names = ["A", "B", "C", "D", "E", "F", "P"]
pins = [pin5, pin11, pin15, pin14, pin13, pin12, pin8]
status = [0, 0, 0, 0, 0, 0, 0]

while True:
    # Joystick
    # x has offset of 24 on my joystick
    print("x:%s" % (pin1.read_analog() * 2 - 1048))
    # y has offset of 2 on my joystick
    print("y:%s" % (pin2.read_analog() * -2 + 1026))
    # Keys
    for i in range(7):
        if pins[i].read_digital() == status[i]:
            status[i] = 0 if status[i] else 1
            print("%s:%s" % (names[i], status[i]))
    utime.sleep_ms(10)

