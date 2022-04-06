pins.setPull(DigitalPin.P5, PinPullMode.PullUp)
pins.setPull(DigitalPin.P11, PinPullMode.PullUp)
let names = ["A", "B", "C", "D", "E", "F", "P"]
let inputs = [DigitalPin.P5, DigitalPin.P11, DigitalPin.P15, DigitalPin.P14, DigitalPin.P13, DigitalPin.P12, DigitalPin.P8]
let status = [0, 0, 0, 0, 0, 0, 0]
basic.forever(function on_forever() {
    for (let i = 0; i < 7; i++) {
        if (pins.digitalReadPin(inputs[i]) == status[i]) {
            if (status[i]) {
                status[i] = 0
            } else {
                status[i] = 1
            }
            
            serial.writeValue(names[i], status[i])
        }
        
    }
    basic.pause(10)
})
basic.forever(function on_forever2() {
    serial.writeValue("x", Math.map(pins.analogReadPin(AnalogPin.P1), 0, 1024, -1024, 1024))
    serial.writeValue("y", Math.map(pins.analogReadPin(AnalogPin.P2), 1024, 0, -1024, 1024))
    basic.pause(10)
})
