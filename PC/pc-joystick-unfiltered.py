import re
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

ui = UInput(capabilities, name="Xbox 360 Controller", bustype=e.BUS_USB,
            vendor=0x045e, product=0x028e, version=0x110)
print("Device created:", ui.device)

serial_port = glob.glob("/dev/ttyACM*")
if len(serial_port) != 1:
    serial_port = input("Enter path to the serial port microbit is associated with:\n")
else:
    serial_port = serial_port[0]

with serial.Serial(serial_port, 115200, timeout=1) as port:
    buffer = ""
    while True:
        # Read all available characters
        data = port.read(port.in_waiting or 1).decode('ascii', errors='ignore')
        buffer += data

        # Split into lines if newline exists
        while '\n' in buffer or '\r' in buffer:
            #time.sleep(0.5)
            line, buffer = re.split(r'[\r\n]', buffer, 1)  # First full line, rest stays in buffer
            #print(f"-- {repr(line)}")
            line = line.strip()
            if not line:
                continue
            try:
                #print(repr(line))
                option, value = line.split(':', 1)
                val = float(value)

                if option == "x":
                    if -256 < val < 256:
                        ui.write(e.EV_ABS, e.ABS_X, int(257 * val - 32767))
                    else:
                        print(f"Ignoring x:{val}")
                elif option == "y":
                    if -256 < val < 256:
                        ui.write(e.EV_ABS, e.ABS_Y, int(257 * val - 32767))
                    else:
                        print(f"Ignoring y:{val}")
                elif option == "A":
                    ui.write(e.EV_KEY, e.BTN_A, int(val))
                elif option == "B":
                    ui.write(e.EV_KEY, e.BTN_B, int(val))
                else:
                    print(f"Ignoring {line}")
                ui.syn()
            except Exception as exc:
                print("Error parsing line:", line)
                print("Exception:", exc)
