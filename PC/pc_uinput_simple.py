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

The input format is "$key:$value" where key is either x, y joystick
axes -1024..1023 or X, Y buttons 0..1
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
    },
    e.EV_KEY: [e.BTN_A, e.BTN_B],
}


ui = UInput(capabilities, name="Xbox 360 Controller", bustype=e.BUS_USB,
            vendor=0x045e, product=0x028e, version=0x110)
print("Device created:", ui.device)

# Initialize the serial port
serial_port = glob.glob("/dev/ttyACM*")
if len(serial_port) != 1:
    serial_port = input("Enter path to the serial port microbit is associated with:\n")
else:
    serial_port = serial_port[0]

# Start the main loop
with serial.Serial(serial_port, 115200) as port:
    while True:
        # Read available lines
        lines = port.readline().decode('ascii').strip()
        # Get one line a time
        for line in lines.splitlines():
            try:
                # Read key:value
                key, value = line.strip().split(':', 1)
                # write the new value to the right axis/button
                if key == 'x':
                    # axes value -1024..1023 joystick requires -32767..32767
                    ui.write(e.EV_ABS, e.ABS_X, 64 * int(value) - 32767)
                elif key == 'y':
                    # axes value -1024..1023 joystick requires -32767..32767
                    ui.write(e.EV_ABS, e.ABS_Y, 64 * int(value) - 32767)
                elif key == 'A':
                    # button value 0..1 joystick uses 0 or not 0
                    ui.write(e.EV_KEY, e.BTN_A, int(value))
                elif key == 'B':
                    # button value 0..1 joystick uses 0 or not 0
                    ui.write(e.EV_KEY, e.BTN_B, int(value))
                else:
                    print("Error: ", line)
            except Exception as exc:
                print("Error:", exc)
