pins.set_pull(DigitalPin.P5, PinPullMode.PULL_UP)
pins.set_pull(DigitalPin.P11, PinPullMode.PULL_UP)
names = ["A", "B", "C", "D", "E", "F", "P"]
inputs = [DigitalPin.P5,
    DigitalPin.P11,
    DigitalPin.P15,
    DigitalPin.P14,
    DigitalPin.P13,
    DigitalPin.P12,
    DigitalPin.P8]
status = [0, 0, 0, 0, 0, 0, 0]

def on_forever():
    # Buttons handling
    for i in range(7):
        if pins.digital_read_pin(inputs[i]) == status[i]:
            if status[i]:
                status[i] = 0
            else:
                status[i] = 1
            serial.write_value(names[i], status[i])
    basic.pause(10)
basic.forever(on_forever)

def on_forever2():
    # Joystick handling
    # My Joystick has offset of +10 on x axis
    serial.write_value("x",
        Math.map(pins.analog_read_pin(AnalogPin.P1), 0, 1024, -1024, 1024) - 10)
    # My Joystick has offset of -4 on y axis
    serial.write_value("y",
        Math.map(pins.analog_read_pin(AnalogPin.P2), 1024, 0, -1024, 1024) + 4)
    basic.pause(10)
basic.forever(on_forever2)
