import paho.mqtt.client as mqtt
import time
import json
from requests import *


class MyMQTTCatalog:

    def __init__(self, clientID,broker,port, topic):
        self.clientID = clientID
        self.topic = topic
        self.broker =broker
        self.port=port
        self.mqtt_client = mqtt.Client(clientID, False)
        self.mqtt_client.on_connect = self.myOnConnect
        self.mqtt_client.on_message = self.myOnMessageReceived

    def start(self):
        self.mqtt_client.connect(self.broker, self.port)
        self.mqtt_client.loop_start()
        self.mqtt_client.subscribe(self.topic, 2)

    def stop(self):
        self.mqtt_client.unsubscribe(self.topic)
        self.mqtt_client.loop_stop()
        self.mqtt_client.disconnect()

    def myOnConnect(self, paho_mqtt, userdata, flags, rc):
        print("Connected to %s with result code: %d" % (self.broker, rc))

    def myOnMessageReceived(self, paho_mqtt, userdata, msg):
        my_json = msg.payload.decode('utf8').replace("'", '"')
        # Load the JSON to a Python list & dump it back out as formatted JSON
        data = json.loads(my_json)
        requests.put("http://192.168.1.52:8080/Devices/add", json = data)

    def notify(self, topic, msg):
        print("Topic:'" + msg.topic + "', QoS: '" + str(msg.qos) + "' Message: '" + str(msg.payload) + "'")
    # risposta del tipo {"Device":"Id", "resources":[], "end_points":[]}
