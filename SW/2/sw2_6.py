import paho.mqtt.client as PahoMQTT
import time

broker_mqtt = "test.mosquitto.org"
port_mqtt = 1883
topic = "/Catalog"

class MyMQTTPublisher:
	def __init__(self, clientID, topic, broker, port):
		self.clientID = clientID
		# create an instance of paho.mqtt.client
		self._paho_mqtt = PahoMQTT.Client(self.clientID, False) 
		# register the callback
		self._paho_mqtt.on_connect = self.myOnConnect
		#self.messageBroker = 'mqtt.eclipse.org'
		self.messageBroker = broker

	def start (self):
		#manage connection to broker
		self._paho_mqtt.connect(self.messageBroker, port_mqtt)
		self._paho_mqtt.loop_start()

	def stop (self):
		self._paho_mqtt.loop_stop()
		self._paho_mqtt.disconnect()

	def myPublish(self, topic, message):
		# publish a message with a certain topic
		self._paho_mqtt.publish(topic, message, 2)
		print("Message sent")

	def myOnConnect (self, paho_mqtt, userdata, flags, rc):
		print ("Connected to %s with result code: %d" % (self.messageBroker, rc))

if __name__ == "__main__":
	print(f"Connessione al broker: {broker_mqtt} alla porta: {port_mqtt}")
	my_mqtt = MyMQTTPublisher("IoT device_publisher", topic, broker_mqtt, port_mqtt)
	my_mqtt.start()

	done = False
#	command_menu = 'Type:\n "add" to add a new device or refresh its timestamp (expected json file)\n "end" to quit\n'
	device1={
        "Device": "Dispositivo1", 
        "risorse": "tante", 
        "end_points":[0, 1, 2]
        }
	while True:
		my_mqtt.myPublish(topic, str(device1))
		time.sleep(5)
#	while not done:
#		print(command_menu)
#		command = input("Insert: ")
#		if command == "add":
#			json_string = input("Json string: ")
#			my_mqtt.myPublish(topic, json_string)
#			print(json_string)
#			time.sleep(60)
#		elif command == "finish":
#			print("Closing the program")
#			done = True
#		else: 
#			print("Wrong command, please try again")