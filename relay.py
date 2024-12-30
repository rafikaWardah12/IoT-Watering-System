from machine import Pin
import time

relay = Pin(2, Pin.OUT) # The pin that is connected to the Input Circuit of the Relay

while True:  # Loop forever
    relay.value(0)  # Turn the relay ON
    print("on")
    time.sleep(1)
    relay.value(1)  # Turn the relay OFF
    print("off")
    time.sleep(1)
    