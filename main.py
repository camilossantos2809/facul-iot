import time
import urllib3
import Adafruit_DHT as dht
import RPi.GPIO as gpio

PIN_IN_DHT = 4
PIN_OUT_GPIO = 32
MAIN_URL = 'https://api.thingspeak.com/update?api_key={key}&field1={temp}&field2={hum}'
gpio.setmode(gpio.BOARD)
gpio.setup(PIN_OUT_GPIO, gpio.OUT)

with open('thingspeak-key.txt') as file:
    KEY = file.read()

while True:
    # Get informations about humidity and temperature from DHT11
    humidity, temperature = dht.read_retry(dht.DHT11, PIN_IN_DHT)

    # Send data to thingspeak.com
    urllib3.PoolManager().request('GET', MAIN_URL.format(
        key=KEY, temp=temperature, hum=humidity))
    print("Humidity: {} Temperature: {}".format(humidity, temperature))

    # Verify data and change relé to on or off
    if humidity > 70.0 or temperature > 31.0:
        print("** Ligando Relé **")
        gpio.output(PIN_OUT_GPIO, True)
    else:
        gpio.output(PIN_OUT_GPIO, False)

    # Send data each 15 min
    time.sleep(15*60)
    # time.sleep(20)
