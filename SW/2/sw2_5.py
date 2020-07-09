#from sw2_1_main import *
import paho.mqtt.client as mqtt
import time
import json
from sw2_1_nonweb import *

BROKER = "test.mosquitto.org"
PORT = 1883
TOPIC = "/Catalog"

class MyMQTTCatalog:

    def __init__(self, clientID, topic, broker):
        self.devices = []

        self.clientID = clientID
        self.topic = topic
        self.broker = broker

        self.mqtt_client = mqtt.Client(clientID, False)

        self.mqtt_client.on_connect = self.myOnConnect
        self.mqtt_client.on_message = self.myOnMessageReceived

    def start(self):
        self.mqtt_client.connect(self.broker, PORT)
        self.mqtt_client.loop_start()
        self.mqtt_client.subscribe(self.topic, 2)

    def stop(self):
        self.mqtt_client.unsubscribe(self.topic)
        self.mqtt_client.loop_stop()
        self.mqtt_client.disconnect()

    def myOnConnect(self, paho_mqtt, userdata, flags, rc):
        print("Connected to %s with result code: %d" % (self.broker, rc))

    def myOnMessageReceived(self, paho_mqtt, userdata, msg):
        # A new message is received

        my_json = msg.payload.decode('utf8').replace("'", '"')
        # Load the JSON to a Python list & dump it back out as formatted JSON
        data = json.loads(my_json)
        print(data["Device"])
        deviceId = data["Device"]
        for d in self.devices:
            print("nel for")
            if d.Id == deviceId:
                d.timestamp = time.time()
                break
        else:
            print("nell'else")
            deviceEndPoints = data["end_points"]
            deviceResources = data["risorse"]
            d = devices(deviceId, deviceEndPoints, deviceResources)
            self.devices.append(d)
        print("Topic:'" + msg.topic + "', QoS: '" + str(msg.qos) + "' Message: '" + str(msg.payload) + "'")

    def notify(self, topic, msg):
        print("Topic:'" + msg.topic + "', QoS: '" + str(msg.qos) + "' Message: '" + str(msg.payload) + "'")
    # risposta del tipo {"Device":"Id", "resources":[], "end_points":[]}


if __name__ == "__main__":
    mqtt_catalog = MyMQTTCatalog("MyMQTTCatalog", TOPIC, BROKER)
    mqtt_catalog.start()
    a = 0
    while a < 10:
        a += 1
        time.sleep(4)
    mqtt_catalog.stop()