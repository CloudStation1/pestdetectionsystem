import base64
import json
import os.path as path
from paho.mqtt import client as mqtt

class Node:
    broker = '192.168.31.219'
    port = 1883
    topic = 'rat/img'

    def __init__(self, img=''):
        self.img = img

    def getMQTTConnection(self):
        try:
            client = mqtt.Client()
            client.on_connect = self.on_connect
            client.connect(self.broker, self.port)
            return client
        except Exception as e:
            print(e)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print('Connected to Broker ' + self.broker)
        else:
            print("Failed to connect, return code %d\n", rc)

    def getImageName(self):
        return path.basename(self.img)

    def isImgFound(self):
        if path.exists(self.img):
            return 1
        else:
            return 0

    def checkResult(self,result):
        if (result == 0):
            print('Image('+ self.getImageName() +') Sent Sucessfully.')
        else:
            print('Image('+ self.getImageName() +') Can not send.')

    def prepareJsonImg(self):
        try:
            if not self.isImgFound():
                raise Exception("Image not Found.")
            f = open(self.img, 'rb')
            image_byte = base64.b64encode(f.read())
            image_str = image_byte.decode('ascii')  # byte to str
            data = {
                'img_name' : self.getImageName(),
                'img_content' : image_str
            }
            return json.dumps(data)
        except Exception as e:
            print(e)

    def transferData(self):
        try:
            if not self.isImgFound():
                raise Exception("Image not Found.")

            client = self.getMQTTConnection()
            client.loop_start()
            preparedImg = self.prepareJsonImg()
            result, count = client.publish(self.topic, preparedImg)
            self.checkResult(result)
            client.loop_stop()
        except Exception as e:
            print(e)

# imgArray = ['IMG_5981.jfif', 'IMG_5982.jfif', 'IMG_5983.jfif', 'IMG_5984.jfif', 'IMG_5985.jfif', 'IMG_5986.jfif', 'IMG_5987.jfif', 'IMG_5988.jfif', 'IMG_5989.jfif', 'IMG_5990.jfif']
imgArray = ['IMG_5981.jfif']
for img in imgArray:
    p1 = Node('images/'+img);
    p1.transferData()