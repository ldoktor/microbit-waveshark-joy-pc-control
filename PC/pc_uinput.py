# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# See LICENSE for more details.
#
# Copyright: Lukas Doktor 2025
# Author: Lukas Doktor <ldoktor@redhat.com>
"""
Simulates a gamepad-like device taking input from serial console

The input format is "$key:$value:$value*2" (the second value is
used to detect transmit errors)
"""
import serial
import time
import glob
from evdev import UInput, ecodes as e, AbsInfo

# Define the capabilities for the controller
capabilities = {
    e.EV_ABS: {
        e.ABS_X: AbsInfo(0, -32767, 32767, 0, 16, 0),  # Left stick X
        e.ABS_Y: AbsInfo(0, -32767, 32767, 0, 16, 0),  # Left stick Y
        e.ABS_RX: AbsInfo(0, -32767, 32767, 0, 16, 0), # Right stick X
        e.ABS_RY: AbsInfo(0, -32767, 32767, 0, 16, 0), # Right stick Y
        e.ABS_Z: AbsInfo(0, 0, 255, 0, 0, 0),     # Left trigger
        e.ABS_RZ: AbsInfo(0, 0, 255, 0, 0, 0),    # Right trigger
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


class ControllerSimulator:
    """
    Creates a virtual /dev/input/jsXXX device and sets it's values based on
    the serial port input.

    Input format is $key:$value:2*$value where the 2*$value is used to
    eliminate corrupted input. The axis expected range is -1024..1023
    buttons use 0 or non 0.
    """
    def __init__(self):
        self.ui = UInput(capabilities, name="Xbox 360 Controller", bustype=e.BUS_USB,
                         vendor=0x045e, product=0x028e, version=0x110)
        print("Device created:", self.ui.device)

        # Initialize the serial port
        self.serial_port = glob.glob("/dev/ttyACM*")
        if len(self.serial_port) != 1:
            self.serial_port = input("Enter path to the serial port microbit is associated with:\n")
        else:
            self.serial_port = self.serial_port[0]

        # Mapping from serial console keys to joystick (type, device) tuples
        self.mapping = {'x': (e.EV_ABS, e.ABS_X),
                        'y': (e.EV_ABS, e.ABS_Y),
                        'rx': (e.EV_ABS, e.ABS_RX),
                        'ry': (e.EV_ABS, e.ABS_RY),
                        'z': (e.EV_ABS, e.ABS_Z),
                        'A': (e.EV_KEY, e.BTN_A),
                        'B': (e.EV_KEY, e.BTN_B),
                        'X': (e.EV_KEY, e.BTN_X),
                        'Y': (e.EV_KEY, e.BTN_Y),
                        'TL': (e.EV_KEY, e.BTN_TL),
                        'TR': (e.EV_KEY, e.BTN_TR),
                        'SELECT': (e.EV_KEY, e.BTN_SELECT),
                        'START': (e.EV_KEY, e.BTN_START)}
        self.errs = 1
        self.count = 1

    def run(self):
        with serial.Serial(self.serial_port, 115200) as port:
            while True:
                lines = port.readline().decode('ascii').strip()
                for line in lines.splitlines():
                    try:
                        # Ignore lines starting with '#' (print them)
                        if line.startswith("#"):
                            print(line)
                            continue
                        # Calculate error-rate
                        self.count += 1
                        if self.count % 1000 == 0:  # Print progress every 1000 counts
                            print(f"{self.errs}/{self.count}*100={self.errs / self.count * 100}%")

                        # Get values from this line
                        key, value_str, value2_str = line.strip().split(':', 2)
                        value = int(value_str)  # Convert the string to an integer

                        # Check if value read properly (avoid transfer errors)
                        if int(value2_str) // 2 != value:
                            self.errs += 1
                            print(f"Error {key}: {repr(value)} != {repr(int(value2_str) // 2)}")

                        # Map serial console key to joystick type/device
                        dev_type, dev = self.mapping.get(key, (None, None))
                        if dev is None:
                            # We failed to map the serial console key,
                            # probably transfer error...
                            self.errs += 1
                            print(f"Unknown button {key}")
                        else:
                            # Write the current value for the current axis/btn
                            self.ui.write(dev_type, dev, value)
                    except Exception as exc:
                        # Something terrible happened, print the details
                        print("Error:", exc)
                        self.errs += 1


# This is the main entry-point
if __name__ == "__main__":
    # Initialize the controller
    controller = ControllerSimulator()
    # Start the main loop
    controller.run()
