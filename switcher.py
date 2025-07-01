from gpiozero import LED
from signal import pause
relayObj = LED(26)
led1 = LED(19)
led2 = LED(13)

def relay(state=False):
    # led.blink()
    output="USB ON"
    if(state==True):
        relayObj.on()
    else:
        relayObj.off()
        output="USB OFF"
    return output

def led(index=1,state=False):
    if(index==1):
        output=LED1(state)
    else:
        output=LED2(state)
    return output

def LED1(state=False):
    output="LED 1 ON"
    if(state==True):
        led1.on()
    else:
        led1.off()
        output="LED 1 OFF"
    return output

def LED2(state=False):
    output="LED 2 ON"
    if(state==True):
        led2.on()
    else:
        led2.off()
        output="LED 2 OFF"
    return output