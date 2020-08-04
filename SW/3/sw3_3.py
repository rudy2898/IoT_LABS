import paho.mqtt.client as mqtt
import time
import requests
import json

class MyPublisher:
	def __init__(self, clientID, serviceId, description):
		self.clientID = clientID

		# create an instance of paho.mqtt.client
		self._paho_mqtt = mqtt.Client(self.clientID, False) 
		# register the callback
		self._paho_mqtt.on_connect = self.myOnConnect
		self._paho_mqtt.on_connect = self.myOnConnect
		self.serviceId = serviceId
		self.description = description
		self.end_points = []

		self.messageBroker = 'null'
		self.port = -1

	def start (self):
		#manage connection to broker
		self._paho_mqtt.connect(self.messageBroker, 1883)
		self._paho_mqtt.loop_start()

	def stop (self):
		self._paho_mqtt.loop_stop()
		self._paho_mqtt.disconnect()

	def myPublish(self, message):
		# publish a message with a certain topic
		for t in self.topic:
			self._paho_mqtt.publish(t, message, 2)

	def myOnConnect (self, paho_mqtt, userdata, flags, rc):
		print ("Connected to %s with result code: %d" % (self.messageBroker, rc))

	def registerOnCatalog(self):
		service = {
			"serviceId": self.serviceId,
			"description": self.description,
			"end_points": self.end_points
		}
		requests.put("http://localhost:8080/services/add", json = service)

	def getBrokerInfo(self):
		r = requests.get("http://localhost:8080/broker/info")
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
	mypub = MyPublisher("MyPublisher", "S02", "Invia messaggi alla board per gestire il led")
	mypub.registerOnCatalog()
	mypub.getDeviceTopic("ArduinoYun")
	mypub.getBrokerInfo()
	mypub.start()
	time.sleep(2)
	keep_going = True
	msg = {
		"bn": "Yun", 
		"e": [
			{
				"n": "led", 
				"t": "null", 
				"v": 0, 
				"u": "null"
				}
			]
		}
	while keep_going:
		code = input("Inserire 0 per spegnere il led o 1 per accenderlo.")
		if code == "0":
			msg["e"][0]["v"] = 0
			mypub.myPublish(json.dumps(msg))
		elif code == "1":
			msg["e"][0]["v"] = 1
			mypub.myPublish(json.dumps(msg))
		else:
			keep_going = False
			print("Bye.")
	mypub.stop()
