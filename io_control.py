import rtde_io
import rtde_receive
import time
from gpiozero import RGBLED

rtde_receive_ = rtde_receive.RTDEReceiveInterface("192.168.2.66")

led = RGBLED(23, 24, 25)

while True:
    try:
        if rtde_receive_.getDigitalOutState(0):
            led.value = (0,1,0)
        else:
            led.value = (0,0,0)
        time.sleep(0.1)
    except:
        break

