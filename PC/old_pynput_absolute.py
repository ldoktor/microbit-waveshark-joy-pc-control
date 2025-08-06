"""
Simple program to read $key:$value lines from serial console and move mouse
or press keys accordingly via pynput library.
"""
import serial
import time
import pynput
from pynput.mouse import Button
from pynput.keyboard import Key
import glob

# If single ttyACM* device found, use it, otherwise ask for input
serial_port = glob.glob("/dev/ttyACM*")
if len(serial_port) != 1:
    serial_port = input("Enter path to the serial port microbit is associated with:\n")
else:
    serial_port = serial_port[0]

# Initialize mouse and keyboard
mouse = pynput.mouse.Controller()
keyboard = pynput.keyboard.Controller()
# You can modify the event-key mapping here
keyboard_mapping = {"P": Key.space, "E": 'w', "C": 's', "F": 'a', "D": 'd'}

with serial.Serial(serial_port, 115200) as port:
    while True:
        # Until infinity read lines and act
        # (use ctrl+c to interrupt)
        try:
            # Read the line
            line = port.readline().decode('ascii').strip()
            print(line)
            line = line.split(':', 1)
            if len(line) != 2:
                continue
            option, value = line
            # mouse x
            if option == "xy":
                x, y = value.split(';')
                # Display resolution is 1920x1080, input is -1024..1024
                mouse.position = (int(x) + 960, int(y) * 0.54 + 553)
            elif option == "x":
                x = float(value)
                mouse.move(x - _x, 0)
                _x = x
            # mouse y
            elif option == "y":
                y = float(value)
                mouse.move(0, y - _y)
                _y = y
            # mouse clicks
            elif option in "AB":
                print(line)
                if option == "A":
                    button = Button.left
                else:
                    button = Button.right
                if int(value) == 0:
                    mouse.release(button)
                else:
                    mouse.press(button)
            # key presses
            elif option in "CDEFP":
                print(line)
                if int(value):
                    keyboard.press(keyboard_mapping[option])
                else:
                    keyboard.release(keyboard_mapping[option])
        except (ValueError, KeyError) as details:
            print(details)
