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
Simple program to print microbit inputs/sensors to serial console

The output format is $key:$value:2*$value (the second value is used
to detect transmit errors), the axes range is -1024..1023, buttons
values are 0 and non 0.

Comment/uncomment lines to select different sensors, eventually
add/modify the keys to report as different entry.
"""
from microbit import *
import utime

offsetx = 0
offsety = 0
while True:
    # Centering of pin1 and pin2
    #   Comment-out when using v1 sensor (or use different button)
    if pin_logo.is_touched():
        offsetx = 512 - pin1.read_analog()
        offsety = 512 - pin2.read_analog()
    # Send values of all enabled sensors
    #   Comment/uncomment/modify to submit different values/sensors
    for key, value in (
            ("A", 1 if button_a.is_pressed() else 0),
            ("B", 1 if button_b.is_pressed() else 0),
            ("X", 0 if pin15.read_digital() else 1),
            ("Y", 0 if pin14.read_digital() else 1),
            ("TL", 0 if pin13.read_digital() else 1),
            ("TR", 0 if pin12.read_digital() else 1),
            ("SELECT", 0 if pin8.read_digital() else 1),
            #("START", 1 if pin12.read_digital() else 0),
            #("x", min(32767, max(-32767, 50 * accelerometer.get_x()))),
            #("y", min(32767, max(-32767, 50 * accelerometer.get_y()))),
            ("x", min(32767, max(-32767, 64 * (pin1.read_analog() + offsetx) - 32767))),
            ("y", min(32767, max(-32767, 64 * (1023 - pin2.read_analog() - offsety) - 32767))),
            #("rx", min(32767, max(-32767, 1 * compass.get_x() - 0))),
            #("ry", min(32767, max(-32767, 1 * compass.get_y() - 0))),
            #("z", min(32767, max(-32767, 257 * microphone.sound_level() - 32767)))
    ):
        print('%s:%s:%s' % (key, value, value * 2))
        # Rest a bit after each send
        utime.sleep_ms(2)
