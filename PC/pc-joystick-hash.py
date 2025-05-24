import json
import serial
import time
import glob
from evdev import UInput, ecodes as e, AbsInfo
from collections import deque
import statistics

capabilities = {
    e.EV_ABS: {
        e.ABS_X: AbsInfo(0, -32767, 32767, 0, 16, 0),  # Left stick X
        e.ABS_Y: AbsInfo(0, -32767, 32767, 0, 16, 0),  # Left stick Y
        #e.ABS_RX: AbsInfo(0, -32767, 32767, 0, 16, 0), # Right stick X
        #e.ABS_RY: AbsInfo(0, -32767, 32767, 0, 16, 0), # Right stick Y
        #e.ABS_Z: AbsInfo(0, 0, 255, 0, 0, 0),     # Left trigger
        #e.ABS_RZ: AbsInfo(0, 0, 255, 0, 0, 0),    # Right trigger
        #e.ABS_HAT0X: AbsInfo(0, -1, 1, 0, 0, 0),  # D-Pad X
        #e.ABS_HAT0Y: AbsInfo(0, -1, 1, 0, 0, 0),  # D-Pad Y
    },
    e.EV_KEY: [
        e.BTN_A, e.BTN_B, e.BTN_X, e.BTN_Y,
        e.BTN_TL, e.BTN_TR,
        e.BTN_SELECT, e.BTN_START,
        e.BTN_THUMBL, e.BTN_THUMBR
    ],
}


def simple_unhash(s):
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    base = len(chars)
    n = 0

    for c in s:
        n = n * base + chars.index(c)

    return n

ui = UInput(capabilities, name="Xbox 360 Controller", bustype=e.BUS_USB,
            vendor=0x045e, product=0x028e, version=0x110)
print("Device created:", ui.device)

serial_port = glob.glob("/dev/ttyACM*")
if len(serial_port) != 1:
    serial_port = input("Enter path to the serial port microbit is associated with:\n")
else:
    serial_port = serial_port[0]

mapping = {'x': ((e.EV_ABS, e.ABS_X), deque(maxlen=5)),
           'y': ((e.EV_ABS, e.ABS_Y), deque(maxlen=5)),
           'A': ((e.EV_KEY, e.BTN_A), deque(maxlen=3)),
           'B': ((e.EV_KEY, e.BTN_B), deque(maxlen=3))}

errs = 1
count = 1
with serial.Serial(serial_port, 115200) as port:
    while True:
        lines = port.readline().decode('ascii').strip()
        for line in lines.splitlines():
            try:
                count += 1
                if count % 1000:
                    print(f"{count}/{errs}={count/errs}")
                #print(repr(line))
                key, value, value2 = line.strip().split(':', 3)
                if value == simple_unhash(value2):
                    errs += 1
                    print(f"Error {key}: {value} != {simple_unhash(value2)}")
                dev, queue = mapping.get(key, (None, None))
                if dev is None:
                    errs += 1
                    print(f"Unknown button {key}")
                queue.append(int(value))
                ui.write(*dev, statistics.median(queue))
            except Exception as exc:
                print("Error:", exc)
                errs += 1

