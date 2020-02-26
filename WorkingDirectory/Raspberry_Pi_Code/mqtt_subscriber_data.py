"""
Brief:
    This script is for subscribing to MQTT service.
    This script continuously monitors the channel for data.
    Whenever data arrives, it creates a new file in data folder and places the data in that file
    When there is NO continuous data arrival for more than 5 secs, it will consider as end of stream
    Then it call the function from AnalyzeDataFunctions script and passed this file name
    were the further analysis is carried out
"""

import paho.mqtt.client as mqtt
from time import gmtime, strftime
import time
from datetime import datetime
from mqtt_data_helper_func import *
from AnalyzeDataFunctions import *
MQTT_SERVER = "localhost"
MQTT_PATH = "accelarationData"

# Defining global variables to get coffee instances stored in different
# files and execute once a stream of data is complete.
currentFileTime = datetime.now()
lastDataFrameArrivalTime = time.time()  # to handle callback if no data arrives indicating end of coffee
storeData = False							# a boolean to latch to handle events


def on_connect(client, userdata, flags, rc):
    """
    Defining on connect and on message callback
    The callback for when the client receives a CONNECT response from the server.
    :param client: client object
    :param userdata: userdata (Not required)
    :param flags: flags (Not required)
    :param rc: return code (Not required)
    :return: None (Not required)
    """
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PATH)


def on_message(client, userdata, msg):
    """
    The callback for when a PUBLISH message is received from the server.
    :param client: client object
    :param userdata: userdata (Not required)
    :param msg: the payload message which contains the data
    :return:
    """
    # Bring all the global variables to this scope otherwise python makes new local copies
    global currentFileTime
    global lastDataFrameArrivalTime
    global storeData
    # If this is first instance then make a new file with current time and start placing the data in that file
    if storeData is False:
        storeData = True
        currentFileTime = datetime.now()
        print("Opening a new file and storing data in : " + str(currentFileTime.strftime("%Y_%m_%d_%H_%M_%S"))+"...")
    # Store the incoming msg.payload of data to the file
    msg.payload = msg.payload.decode("utf-8")
    dataslice = str(msg.payload)[0:10]
    print("Channel::accelarationData:" + str(dataslice).replace("\n", " ") + "...")
    lastDataFrameArrivalTime = time.time()
    fileName = currentFileTime.strftime("%Y_%m_%d_%H_%M_%S")
    store_data(fileName, msg.payload)
# on_message END


# define object of mqtt client and set the attributes
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_SERVER, 1883, 60)

# client.loop_forever()		# loop forever if want to continuously listen to publisher

# implementing manual loop forever to handle in-between data processing events
run = True
while run:
    # loop every 10ms
    client.loop(0.01)

    # if current data stream  has ended then call the predictNewDataPoint from AnalyzeDataFunctions script to analyse
    if ((time.time() - lastDataFrameArrivalTime) > 5) and storeData is True:
        storeData = False
        print("Reached End of Data Frame and processing data stored in file :"
              + str(currentFileTime.strftime("%Y_%m_%d_%H_%M_%S"))+ ".txt ...")

        # calling the predictNewDataPoint function which handles processing of data
        predictNewDataPoint(currentFileTime, 'data', None)
