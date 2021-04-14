import time
from mymqtt import MQTTClient
import ubinascii
import machine
import micropython
from machine import Pin, PWM
import network
import esp
import gc
gc.collect()
import utime
uid = machine.unique_id()

wifiSSID = 'VECTRO'
wifiPASS = 'minivolkmcollaigul'
mqtt_server = '109.248.175.143'
client_id = ubinascii.hexlify(machine.unique_id())
topic_sub_scan = b'controllers/scan/'
topic_sub_koef_brightness = b'controllers/set/koef_brightness'
topic_sub_power = b'controller/'+ ubinascii.hexlify(machine.unique_id()) + b'/power'


topic_pub_scan = b'controllers/' + ubinascii.hexlify(machine.unique_id())
topic_pub_status = b'controller/' + ubinascii.hexlify(machine.unique_id()) + b'/satus'


koef_brightnes = 1
power = 100
nowPower = 100
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(wifiSSID, wifiPASS)
print('conneting to wifi..')
while not station.isconnected():
    pass

print('Connection successful')
print(station.ifconfig())

p13 = Pin(13, Pin.OUT)    
p13.off()                


pwm17 = PWM(Pin(17), freq=1000, duty=power*10)
