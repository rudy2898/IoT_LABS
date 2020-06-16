from sw2_1 import *
import json
import paho.mqtt.client as PahoMQTT

broker_q = "mqtt.eclipse.org"
port = "8080"

class MyMQTTCatalog:

    def __init__(self, clientID, topic, broker):
        self.clientID = clientID
        self.topic = topic
        self.broker = broker
        self._paho_mqtt = PahoMQTT.Client(clientID, False)

        self._paho_mqtt.on_connect = self.myOnConnect
        self._paho_mqtt.on_message = self.myOnMessageReceived

    def start(self):
        self._paho_mqtt.connect(self.broker, port)
        self._paho_mqtt.loop_start()
        self._paho_mqtt.subscribe(self.topic, 2)

    def stop(self):
        self._paho_mqtt.unsubscribe(self.topic)
        self._paho_mqtt.loop_stop()
        self._paho_mqtt.disconnect()

    def myOnConnect(self, paho_mqtt, userdata, flags, rc):
        print("Connected to %s with result code: %d" % (self.broker, rc))

    def myOnMessageReceived(self, paho_mqtt, userdata, msg):
        # A new message is received
        print("Topic:'" + msg.topic + "', QoS: '" + str(msg.qos) + "' Message: '" + str(msg.payload) + "'")

    # risposta del tipo {"Device":"Id", "resources":[], "end_points":[]}
    def notify(self,topic,msg):
        body = json.loads(msg)
        dev = Catalog.getDev_list()

        find = False
        for i in range(dev):
            if body['Device'] == dev[i]:
                Catalog.updateTimestamp(i)
                find = True
        if not find:
            Catalog.addDevices(body)


if __name__ == "__main__":
    mqtt_catalog = MyMQTTCatalog("MyMQTTCatalog", "IoT devices", broker_q)
    mqtt_catalog.start()
