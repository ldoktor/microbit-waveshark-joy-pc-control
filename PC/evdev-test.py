from evdev import UInput, ecodes as e, AbsInfo
import time

cap = {
    e.EV_KEY: [e.BTN_A],
    e.EV_ABS: {
        e.ABS_X: AbsInfo(0, 0, 255, 0, 0, 0)
    }
}

ui = UInput(cap, name="Test Virtual Device", bustype=e.BUS_USB)
print(f"Created virtual input device at {ui.device}")

# Simulate some input
for i in range(10):
    ui.write(e.EV_KEY, e.BTN_A, 1)
    ui.syn()
    time.sleep(0.1)
    ui.write(e.EV_KEY, e.BTN_A, 0)
    ui.syn()
    time.sleep(0.1)
