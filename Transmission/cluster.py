import json
import base64
from paho.mqtt import client as mqtt

class Cluster:
    broker = '192.168.31.219'
    port = 1883
    topic = 'rat/img'    

    def getMQTTConnection(self):
        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.connect(self.broker, self.port)
        return client

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print('Connected to Broker ' + self.broker)
        else:
            print("Failed to connect, return code %d\n", rc)

    def subscribe(self):
        client = self.getMQTTConnection()
        client.subscribe(self.topic)
        client.on_message = self.on_message
        client.loop_forever()

    def on_message(self, client, userdata, msg):
        try:
            if (msg.topic == self.topic):
                dest_path = 'processImg/'
                m_in = json.loads(str(msg.payload.decode('utf-8','ignore')))
                img_name = m_in['img_name']
                image_byte = base64.b64decode(m_in['img_content'])
                f = open(dest_path + img_name, 'wb')
                f.write(image_byte)
                print('Image('+ img_name +') Receive Sucessfully.')
        except Exception as e:
            print(e)

cl = Cluster()
cl.subscribe()