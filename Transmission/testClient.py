import random
import json
import base64
from paho.mqtt import client as mqtt_client


broker = '192.168.31.219'
port = 1883
topic = "data/file"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
username = 'client'
password = 'test'


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        #print(msg.topic)
        m_decode = str(msg.payload.decode('utf-8','ignore'))
        m_in = json.loads(m_decode)
        dest_path = 'processImg/'
        img_name = m_in['img_name']
        image_byte = base64.b64decode(m_in['img_content'])
        f = open(dest_path + img_name, 'wb')
        f.write(image_byte)
        print('Image Receive Sucessfully.')

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
