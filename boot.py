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

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(wifiSSID, wifiPASS)
print('conneting to wifi..')
while not station.isconnected():
    pass

print('Connection successful')
print(station.ifconfig())


def _otaUpdate():
    print('Checking for Updates...')
    from ota_updater import OTAUpdater
    otaUpdater = OTAUpdater('https://github.com/koladanilkov/STL-006A', github_src_dir='app', main_dir= '.', secrets_file="boot.py")
    otaUpdater.install_update_if_available()
    del(otaUpdater)
    
_otaUpdate()
    

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


p13 = Pin(13, Pin.OUT)    # create output pin on GPIO0
p13.off()                


pwm17 = PWM(Pin(17), freq=1000, duty=power*10)
