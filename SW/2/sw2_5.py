#from sw2_1_main import *
import paho.mqtt.client as mqtt
import time

BROKER = "iot.eclipse.org"
PORT = 1883
TOPIC = "Catalog"

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
        print("Message recieved.")
        deviceId = msg.payload["Dispositivi"]
        for d in self.devices:
            if d.Id == deviceId:
                d.timestamp = time.time()
            else:
                deviceEndPoints = msg.payload["end_points"]
                deviceResources = msg.payload["risorse"]
                self.devices.append(devices(deviceId, deviceEndPoints, deviceResources))
        print("Topic:'" + msg.topic + "', QoS: '" + str(msg.qos) + "' Message: '" + str(msg.payload) + "'")

    def notify(self, topic, message):
        print("message recieved")

    # risposta del tipo {"Device":"Id", "resources":[], "end_points":[]}


if __name__ == "__main__":
    mqtt_catalog = MyMQTTCatalog("MyMQTTCatalog", TOPIC, BROKER)
    print("wow")
    mqtt_catalog.start()

class devices():
	def __init__(self, uniqueID, end_points, resources):
		self.Id= uniqueID
		self.end_points= end_points
		self.resources= resources
		self.timestamp=time.time()