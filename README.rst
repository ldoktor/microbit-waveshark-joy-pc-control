Microbit joystick
=================

Simple project to allow using Micro:bit as a joystick.

There are 2 pieces needed, on micro:bit you need to run one of the
`MicroPython` codes and on your computer one of the `PC` codes.
Micro:bit will then keep sending the current values of selected
axes (joystick, potentioneter, gyroscope, accelerator, ...) or
buttons (A, B, ...) via serial console to your computer, where
python is going to keep reading the serial console and it will
keep passing the new values to the newly created virtual
joystick.

Simple start
============

Prerequisites
-------------

* [python](https://www.python.org/downloads/) installed on your system
* evdev python library installed ``pip3 install evdev``

Simple version
--------------

1. Paste the code from [MicroPython/microbit.py](MicroPython/microbit.py)
   to [Micro:bit micropython editor](https://python.microbit.org/v/3/reference/pins)
   and upload it.

2. Run [PC/pc_uinput_simple.py](PC/pc_uinput_simple.py) on your computer
   ``python3 PC/pc_uinput_simple.py``

3. Look at available joystick devices. On linux you can use
   ``jstest /dev/input/js0``

More reliable version
---------------------

Use [PC/microbit_safer.py](PC/microbit_safer.py) or
[PC/microbit_safer_calibrate.py](PC/microbit_safer_calibrate.py) on microbit
and [PC/pc_uinput.py](PC/pc_uinput.py) or
[PC/pc_uinput_filtered.py](PC/pc_uinput_filtered.py). Those use a simple
checksum to prevent transfer corruptions and greatly improve the accuracy.
