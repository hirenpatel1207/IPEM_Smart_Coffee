# sample coe for publisher
import paho.mqtt.publish as publish
import time
#MQTT_SERVER = "192.168.178.97"
MQTT_SERVER = "localhost" 
MQTT_PATH = "accelarationData"

StartTime = time.time()
EndTime = time.time()
timeDiff= 0
for x in range(10):
    StartTime = time.time()
    publish.single(MQTT_PATH, "1908\n",hostname=MQTT_SERVER)
    time.sleep(1)
    EndTime = time.time()
    timeDiff =EndTime - StartTime


