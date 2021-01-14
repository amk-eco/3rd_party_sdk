from lib._led import *
import time
import sys

_gkit_led = None
GPIO_LED = 31

def get_led():
    """Returns a driver to control the AI.Makers.Kit LED light with various animations.

    led = gkit.drivers.get_led()

    # You may set any LED animation:
    led.set_state(gkit.drivers.LED.PULSE_QUICK)
    led.set_state(gkit.drivers.LED.BLINK)

    # Or turn off the light but keep the driver running:
    led.set_state(gkit.drivers.LED_OFF)
    """
    global _gkit_led
    if _gkit_led is None:
        _gkit_led = LED(channel=GPIO_LED)
        _gkit_led.start()
    return _gkit_led

if len(sys.argv) is not 3:
    exit(1)

if not(int(sys.argv[1]) >= 0  and int(sys.argv[1]) <=8):
    exit(1)
if not(int(sys.argv[2]) >= 0  and int(sys.argv[2]) <=20):
    exit(1)


led = get_led()
led.set_state(int(sys.argv[1]))
time.sleep(int(sys.argv[2]))
led.stop()
