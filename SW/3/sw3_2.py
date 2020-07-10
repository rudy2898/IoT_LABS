import paho.mqtt.client as mqtt
import time
import requests
import json


class MySubscriber:

	def __init__(self, clientID, serviceId, description, end_points = []):
		self.clientID = clientID
		# create an instance of paho.mqtt.client
		self._paho_mqtt = mqtt.Client(clientID, False) 

		# register the callback
		self._paho_mqtt.on_connect = self.myOnConnect
		self._paho_mqtt.on_message = self.myOnMessageReceived

		self.serviceId = serviceId
		self.descrizione = description
		self.end_points = end_points
		self.topic = '/this/is/my/topic'
		self.messageBroker = 'iot.eclipse.org'
		self.port = 'nulla'


	def start (self):
		#manage connection to broker
		self._paho_mqtt.connect(self.messageBroker, 1883)
		self._paho_mqtt.loop_start()
		# subscribe for a topic
		for t in self.topic:
			self._paho_mqtt.subscribe(t, 2)

	def stop (self):
		self._paho_mqtt.unsubscribe(self.topic)
		self._paho_mqtt.loop_stop()
		self._paho_mqtt.disconnect()

	def myOnConnect (self, paho_mqtt, userdata, flags, rc):
		print ("Connected to %s with result code: %d" % (self.messageBroker, rc))

	def myOnMessageReceived (self, paho_mqtt , userdata, msg):
		# A new message is received
		print ("Topic:'" + msg.topic+"', QoS: '"+str(msg.qos)+"' Message: '"+str(msg.payload) + "'")
	
	def registerOnCatalog(self):
		service = {
			"Servizi": self.serviceId,
		"descrizione": self.descrizione,
			"end_points": self.end_points
		}
		requests.put("http://localhost:8080/services/add", json = service)

	def getBrokerInfo(self):
		r = requests.get("http://localhost:8080/broker/info") #controllare che cosa ritorna requests
		info = json.loads(r.content.decode('utf-8'))
		self.messageBroker = info["brokerIp"]
		self.port = info["brokerPort"]
		print(f"{self.port} {self.messageBroker}")
	
	def getDeviceTopic(self, deviceId):
		r = requests.get("http://localhost:8080/devices/search/"+deviceId)
		info = json.loads(r.content.decode('utf-8'))
		self.topic = info["end_points"]
		print(self.topic)




if __name__ == "__main__":
	mysub = MySubscriber("MySubscriber 1", "S01", "MQTT subscriber che riceve messaggi sui valori di temperatura.")
	mysub.getDeviceTopic("ArduinoYun")
	mysub.registerOnCatalog()
	mysub.getBrokerInfo()
	mysub.start()
	while True:
		pass
	mysub.stop()