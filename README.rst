Demonstration project to control PC via microbit
================================================

This is a very simple demonstration project that periodically
reads statuses of various pins on your microbit and sends events
via serial console to your computer, where a python program
uses `pynput <https://pythonhosted.org/pynput/>`_ library to
act as a keyboard and mouse.

Primarily this is used to educate kids and show them how to
control a computer, how to pass messages and handle various
events. It's written around the
`Waveshare joystick <https://github.com/waveshare/JoyStick>`_
but one can modify the code to work with any kind of input
that can be translated into numbers or boolean values. See
the section :ref:`Key mapping` for the standard pin mapping.

There are two options, you can use `MakeCode <makecode.microbit.org>`_
or `MicroPython <https://python.microbit.org/v/2>`_ to utilize
this. With MakeCode I originally had issues to fit everything into
the memory but currently it seems to be working well.

Setup
=====

On your PC you need to install python and the pynput library. Please
search the web on how to install python and pip, installing the pynput
library is then only a matter of executing ``pip install pynput`` command.

When this is prepared, you need to decide whether you'll be using the
MakeCode or MicroPython editors. They both should work the same way,
there is no need (and it won't actually change anything) to follow
both so simply chose whatever suits you the best.

MakeCode
--------

#. Plug your microbit to the Waveshare joystick and connect it to your
   computer.
#. Go to `MakeCode editor <https://makecode.microbit.org>`_
#. Use the "Import" button on the right side of the page and chose
   ``Import URL...``
#. Press "Download" and save the file to your microbit

MicroPython
-----------

#. Plug your microbit to the Waveshare joystick and connect it to your
   computer.
#. Go to `micropython <https://python.microbit.org/v/2>`_
#. Paste the content of the ``MicroPython/microbit.py`` file there
#. Press "Download" and save the file to your microbit

Usage
=====

#. Plug your microbit with the code already downloaded to the Waveshare
   joystick and connect it to your computer.
#. On your computer run the ``PC/pc.py`` file

If everything succeeded your mouse should be moving based on the inputs from
the pins 1 and 2 and keys ``w,s,a,d,<space>`` should be emitted based on the pins
input.

In case the mouse keeps moving in a constant speed even when joystick is in the
middle position, it means there is a certain offset that needs to be compensated.
You can do that by modifying the ``x`` and ``y`` values that are being sent.

Key mapping
===========

You don't really need to use the Waveshare joystick to use this repo,
you can simply connect some buttons and potentiometers, or even
modify the code to use the accelerometer or whatever you can imagine.
The original mapping is:

.. list-table:: Waveshare Joystick mapping

   * - Joystick
     - A
     - B
     - C
     - D
     - E
     - F
     - P
     - X
     - Y
   * - Microbit
     - 5
     - 11
     - 15
     - 14
     - 13
     - 12
     - 8
     - 1
     - 2
