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

####

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

def mainFunc():
    global power, nowPower, pwm17, koef_brightnes
    if nowPower < power-koef_brightnes or nowPower > power+koef_brightnes:
        if nowPower > power:
            nowPower -= koef_brightnes
            pwm17.duty(nowPower*10)
        
        if nowPower < power:
            nowPower += koef_brightnes
            pwm17.duty(nowPower*10)
        print('%s \n' % (nowPower))       

#Функция для обработки полученного сообщения
def sub_cb(topic, msg):
  print((topic, msg))
  global topic_sub_power, topic_sub_scan, topic_pub_scan, topic_pub_status, power, koef_brightnes, topic_sub_koef_brightness
  if topic == topic_sub_scan and msg == b'1':
    client.publish(topic_pub_scan, str(power))
  elif topic == topic_sub_power:
    power = max(min(power, 15), 100)
    power = int(msg)
    client.publish(topic_pub_status, str(power))
  elif topic == topic_sub_koef_brightness:
    power = max(min(power, 1), 20)
    koef_brightnes = int(msg)




def connect_and_subscribe():
  global mqtt_server, topic_sub_power, topic_pub_scan, uid
  client = MQTTClient(client_id, mqtt_server, user = b'test', password = b'P@ssw0rd!')
  client.set_callback(sub_cb)
  client.connect()
  client.subscribe(topic_sub_power)
  client.subscribe(topic_sub_scan)
  client.subscribe(topic_sub_koef_brightness)
  print('Connected to %s MQTT broker, subscribed to %s , %s and %s topics' % (mqtt_server, topic_sub_power, topic_sub_scan, topic_sub_koef_brightness))
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()

try:
  client = connect_and_subscribe()
except OSError as e:
  restart_and_reconnect()

timeLastRedact = utime.ticks_ms()
while True:
  try:
    client.check_msg()
    if utime.ticks_ms() - timeLastRedact > 100:
        mainFunc()
        timeLastRedact = utime.ticks_ms()
  except OSError as e:
    restart_and_reconnect()
