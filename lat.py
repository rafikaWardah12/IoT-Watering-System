from machine import Pin, ADC, I2C
import utime as time
from dht import DHT11, InvalidChecksum
from pico_i2c_lcd import I2cLcd
from http import connectWifi, sendData, getActive
import json

# use variables instead of numbers:
soil = ADC(Pin(28)) # Soil moisture PIN reference
dht11_pin = Pin(15, Pin.OUT, Pin.PULL_DOWN)    # Pin 15 on Pico
dht = DHT11(dht11_pin)
relay = Pin(2, Pin.OUT)  # Relay control pin
i2c = I2C(id=1,scl=Pin(27),sda=Pin(26),freq=100000)
lcd = I2cLcd(i2c, 0x27, 2, 16)

endpoint = input("Masukan endpoint api: ")
connectWifi("1", "akucomel")
 
# Calibration values
min_moisture = 0
max_moisture = 65535

readDelay = 0.5

while True:
    time.sleep(5)
    
    try:
        #checkActive = getActive(endpoint)
        
        #if checkActive["active"] is False:
        #    print("Pump is not activated manually")
        #    continue
    
    # Read temperature and humidity from DHT11
        t = dht.temperature
        h = dht.humidity

        # Calculate soil moisture percentage
        moisture1 = (max_moisture - soil.read_u16()) * 100 / (max_moisture - min_moisture)

        # Print values
        print("Moisture : " + "%.2f" % moisture1 + "% ")
        print("Temp: {}".format(t))
        print("Humidity: {}".format(h))

        # Relay control logic
        if moisture1 < 60:
            relay.value(1)  # Turn on pump
            print("Pump ON: Tanah kurang air")
        else:
            relay.value(0)  # Turn off pump
            print("Pump OFF: Tanah cukup air")
        
        #sendData(endpoint, t, h, moisture1)
        
        # Clear the LCD and show the values
        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr("Temp: {} C".format(t))
        lcd.move_to(0, 1)
        lcd.putstr("Moisture: {:.2f}%".format(moisture1))

    except InvalidChecksum:
        print("DHT11 checksum error. Skipping reading.")
    except Exception as e:
        print("Error:", e)

