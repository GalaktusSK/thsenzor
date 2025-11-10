from dht import DHT11 as DHT
from machine import Pin

pin = Pin(27, Pin.IN)
sensor = DHT(pin)

sensor.measure()
temp = sensor.temperature()
hum = sensor.humidity()

print(temp, hum)
