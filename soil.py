import machine
import utime
from dht import DHT11
from machine import I2C, Pin
from pico_i2c_lcd import I2cLcd

# Pin configurations
dht_pin = Pin(15)
relay_pin = Pin(2, Pin.OUT)
soil_moisture_pin = Pin(14)
i2c = I2C(1, scl=Pin(27), sda=Pin(26), freq=100000)

# LCD setup
lcd = I2cLcd(i2c, 0x27, 2, 16)  # Adjust address and dimensions if needed

# DHT11 setup
dht_sensor = DHT11(dht_pin)

# Read soil moisture
def read_soil_moisture():
    adc = machine.ADC(soil_moisture_pin)
    moisture_level = adc.read_u16()
    return moisture_level

# Display data on LCD
def update_lcd(temp, hum, soil_moisture):
    lcd.clear()
    lcd.putstr("Temp: {:.1f}C".format(temp))
    lcd.move_to(0, 1)
    lcd.putstr("Hum: {:.1f}% Soil:{}".format(hum, soil_moisture))

# Control relay based on soil moisture level
def control_relay(soil_moisture, threshold=30000):  # Adjust threshold based on your sensor
    if soil_moisture < threshold:
        relay_pin.on()
    else:
        relay_pin.off()

# Main loop
while True:
    try:
        dht_sensor.measure()
        temperature = dht_sensor.temperature()
        humidity = dht_sensor.humidity()
        soil_moisture = read_soil_moisture()

        update_lcd(temperature, humidity, soil_moisture)
        control_relay(soil_moisture)

        utime.sleep(2)
    except Exception as e:
        lcd.clear()
        lcd.putstr("Error: {}".format(str(e)))
        utime.sleep(5)
