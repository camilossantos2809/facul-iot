import time
import urllib3
import Adafruit_DHT as dht

PIN_IN = 4
MAIN_URL = 'https://api.thingspeak.com/update?api_key={key}&field1={temp}&field2={hum}'

with open('thingspeak-key.txt') as file:
    KEY = file.read()

while True:
    # Get informations about humidity and temperature from DHT11
    humidity, temperature = dht.read_retry(dht.DHT11, PIN_IN)

    # Send data to thingspeak.com
    urllib3.PoolManager().request('GET', MAIN_URL.format(
        key=KEY, temp=temperature, hum=humidity))
    print("Humidity: {} Temperature: {}".format(humidity, temperature))

    # Send data each 15 min
    time.sleep(15*60)
