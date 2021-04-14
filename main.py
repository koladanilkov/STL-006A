#
#
#

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
