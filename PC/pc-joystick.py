import serial
import time
import glob
from evdev import UInput, ecodes as e, AbsInfo

capabilities = {
    e.EV_ABS: {
        e.ABS_X: AbsInfo(128, 0, 255, 0, 15, 0),  # Left stick X
        e.ABS_Y: AbsInfo(128, 0, 255, 0, 15, 0),  # Left stick Y
        e.ABS_RX: AbsInfo(128, 0, 255, 0, 15, 0), # Right stick X
        e.ABS_RY: AbsInfo(128, 0, 255, 0, 15, 0), # Right stick Y
        e.ABS_Z: AbsInfo(0, 0, 255, 0, 0, 0),     # Left trigger
        e.ABS_RZ: AbsInfo(0, 0, 255, 0, 0, 0),    # Right trigger
        e.ABS_HAT0X: AbsInfo(0, -1, 1, 0, 0, 0),  # D-Pad X
        e.ABS_HAT0Y: AbsInfo(0, -1, 1, 0, 0, 0),  # D-Pad Y
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

with serial.Serial(serial_port, 115200) as port:
    while True:
        lines = port.readline().decode('ascii').strip()
        for line in lines.splitlines():
            try:
                print(repr(line))
                line = line.strip().split(':', 1)
                if len(line) != 2:
                    continue
                option, value = line
                if option == "x":
                    val = float(value)
                    if val > 100 and val < 150:
                        ui.write(e.EV_ABS, e.ABS_X, 128)
                    else:
                        ui.write(e.EV_ABS, e.ABS_X, min(255, max(0, int(float(value)))))
                elif option == "y":
                    if val > 100 and val < 150:
                        ui.write(e.EV_ABS, e.ABS_Y, 128)
                    else:
                        ui.write(e.EV_ABS, e.ABS_Y, min(255, max(0, int(float(value)))))
                elif option == "A":
                    ui.write(e.EV_KEY, e.BTN_A, int(value))
                elif option == "B":
                    ui.write(e.EV_KEY, e.BTN_B, int(value))
                else:
                    continue
                ui.syn()
            except Exception as exc:
                print("Error:", exc)
