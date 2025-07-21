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
multiplyx = 1
multiplyy = 1
while True:
    # Calibration of pin1 and pin2
    #   Comment-out when using v1 sensor (or use different button)
    # To use full-calibration hold button A and touch the logo pin. A top left
    # LED should light. Move your controller to top left location, hold it
    # and press button B. A bottom right LED should light. Move your
    # controller to bottom right location, hold it and press button A. You
    # should see "B" on microbit now and some debug info on serial console.
    # Pressing button B resums the main loop using the calibrated input.
    if pin_logo.is_touched():
        if button_a.is_pressed():
            display.set_pixel(0,0,9)
            minx = float("inf")
            miny = float("inf")
            maxx = -float("inf")
            maxy = -float("inf")
            while not button_b.is_pressed():
                minx = min(pin1.read_analog(), minx)
                miny = min(pin2.read_analog(), miny)
                print("#%s:%s:%s:%s" % (pin1.read_analog(), pin2.read_analog(), minx, miny))
            display.set_pixel(4,4,9)
            while not button_a.is_pressed():
                maxx = max(maxx, pin1.read_analog())
                maxy = max(maxy, pin2.read_analog())
                print("#%s:%s:%s:%s" % (pin1.read_analog(), pin2.read_analog(), maxx, maxy))
            multiplyx = 65534 / (maxx - minx)
            offsetx = -multiplyx * minx - 32767
            multiplyy = 65534 / (maxy - miny)
            offsety = -multiplyy * miny - 32767
            print("#minx: %s, miny: %s, maxx: %s, maxy: %s, %sx+%s, %sy+%s"
                  % (minx, miny, maxx, maxy, multiplyx, offsetx, multiplyy, offsety))
            print("#xmin = %s, xmax = %s, ymin = %s, ymax = %s"
                  % (multiplyx * minx + offsetx, multiplyx * maxx + offsetx, multiplyy * miny + offsety, multiplyy * maxy + offsety))
            while not button_b.is_pressed():
                display.scroll("B")
        else:
            offsetx = 512 - pin1.read_analog()
            offsety = 512 - pin2.read_analog()
    # Send values of all enabled sensors
    #   Comment/uncomment/modify to submit different values/sensors
    for key, value in (
            ("A", 1 if button_a.is_pressed() else 0),
            ("B", 1 if button_b.is_pressed() else 0),
            ("X", 0 if pin15.read_digital() else 1),
            ("Y", 0 if pin14.read_digital() else 1),
            #("TL", 0 if pin13.read_digital() else 1),
            #("TR", 0 if pin12.read_digital() else 1),
            #("SELECT", 0 if pin8.read_digital() else 1),
            #("START", 1 if pin12.read_digital() else 0),
            #("x", min(32767, max(-32767, 50 * accelerometer.get_x()))),
            #("y", min(32767, max(-32767, 50 * accelerometer.get_y()))),
            ("x", int(min(32767, max(-32767, multiplyx * pin1.read_analog() + offsetx)))),
            ("y", int(min(32767, max(-32767, multiplyy * pin2.read_analog() + offsety)))),
            #("rx", min(32767, max(-32767, 1 * compass.get_x() - 0))),
            #("ry", min(32767, max(-32767, 1 * compass.get_y() - 0))),
            #("z", min(32767, max(-32767, 257 * microphone.sound_level() - 32767)))
    ):
        print('%s:%s:%s' % (key, value, value * 2))
        # Rest a bit after each send
        utime.sleep_ms(2)
