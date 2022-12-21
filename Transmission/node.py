import random
import time
import base64
import json
from paho.mqtt import client as mqtt_client


broker = '192.168.31.219'
port = 1883
topic = "data/file"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'client'
password = 'test'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print(flags)
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def prepareJsonImg(imgName):
    imgPath = 'images/'
    f = open(imgPath + imgName, 'rb')
    image_byte = base64.b64encode(f.read())
    image_str = image_byte.decode('ascii')  # byte to str
    data = {
        'img_path' : imgPath,
        'img_name' : imgName,
        'img_content' : image_str     
    }
    return data

def publishMsg(client):
    time.sleep(1)
    imgArray = ['IMG_5981.jfif', 'IMG_5982.jfif', 'IMG_5983.jfif', 'IMG_5984.jfif', 'IMG_5985.jfif', 'IMG_5986.jfif', 'IMG_5987.jfif', 'IMG_5988.jfif', 'IMG_5989.jfif', 'IMG_5990.jfif']
    for imgName in imgArray:
        img = prepareJsonImg(imgName)
        jmod = json.dumps(img)
        result = client.publish(topic, jmod)
        print(result)
def run():
    client = connect_mqtt()
    client.loop_start()
    publishMsg(client)

if __name__ == '__main__':
    run()
