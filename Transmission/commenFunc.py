from paho.mqtt import client as mqtt

class CommenFunc:

	def __init__(self, brokerId, port):
		self.brokerId = brokerId
		self.port = port

	def setTopic(self, topic):
		self.topic = topic

	def getTopic(self):
		return self.topic

	def getMQTTConnection(self):
		try:
			client = mqtt.Client()
			client.on_connect = self.on_connect
			client.connect(self.brokerId, self.port)
			return client
		except Exception as e:
			print(e)

	def on_connect(self, client, userdata, flags, rc):
		if rc == 0:
			print('Connected to Broker ' + self.brokerId)
		else:
			print("Failed to connect, return code %d\n", rc)