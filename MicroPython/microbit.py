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
Simple program to print microbit inputs/sensors to serial console.

The output format is $key:$value, the axes range is -1024..1023,
buttons values are 0 and non 0.
"""
from microbit import *
import utime

# Button names
names = ["A", "B", "C", "D", "E", "F", "P"]
# Associated pins to the button names
pins = [pin5, pin11, pin15, pin14, pin13, pin12, pin8]
# The current status of pins (to avoid sending unless the status changed)
status = [0, 0, 0, 0, 0, 0, 0]

while True:
    # Joystick, always send the new value
    # x has offset of 24 on my joystick
    # y has offset of 2 on my joystick
    print("xy:%s;%s" % ((pin1.read_analog() * 2 - 1048),
                        (pin2.read_analog() * -2 + 1026)))
    # Keys, iterate over the names/pins/status
    for i in range(7):
        # If the current pin input doesn't match our status
        if pins[i].read_digital() == status[i]:
            # update our status
            status[i] = 0 if status[i] else 1
            # send the current button name and the value
            print("%s:%s" % (names[i], status[i]))
            # Rest a bit to prevent flooding serial console
            utime.sleep_ms(2)
