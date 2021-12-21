from gpiozero import LED
from signal import pause
led = LED(4)

def myLED():
    led.blink()


def myLEDOn():
    # led.blink()
    led.on()
    return "On"

def myLEDOff():
    # led.blink()
    led.off()
    return "Off"