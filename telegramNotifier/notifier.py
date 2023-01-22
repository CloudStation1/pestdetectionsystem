import os
import json
import base64
import logging
from paho.mqtt import client as mqtt
import requests

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

class telegramSender:

    def sendMsg(self, message, file):
        try:
            base_url = "https://api.telegram.org/bot5820363513:AAHBQiy7GBUAPO18gaFz-VzqqBMspsASjgc/sendPhoto"
            parameters = { "chat_id" : "5269537317", "caption" : message }
            #link={'photo': open(r'/root/cloudComputing/pestdetectionsystem/Notification_application/tmp.jpg','rb')}
            link={'photo': open(file,'rb')}
            resp = requests.post(base_url, data = parameters, files=link)
            log.info(resp.text)
        except Exception as e:
            log.exception('Exception occured ' + str(e))

class mqttconnection:

    def __init__(self, broker, port, topic):
        self.brokerId = broker
        self.port = port
        self.topic = topic

    def getMQTTConnection(self):
        try:
            client = mqtt.Client()
            client.on_connect = self.on_connect
            client.connect(self.brokerId, self.port)
            return client
        except Exception as e:
            log.exception('exception occured')

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            log.info('Connected to Broker ' + self.brokerId)
        else:
            log.error("Failed to connect, return code %d\n", rc)

    def subscribe(self):
        client = self.getMQTTConnection()
        client.subscribe('detect/rat')
        client.on_message = self.onMessage
        client.loop_forever()
        log.info('subscribed to topic:' + self.topic)

    def onMessage(self, client, userdata, msg):
        try:
            log.info('mqtt msg received')
            if (msg.topic == self.topic):
                recmsg = json.loads(str(msg.payload.decode('utf-8','ignore')))
                imgcontent = base64.b64decode(recmsg['img_content'])
                filePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tmp.jpg")
                f = open(filePath, "wb")
                f.write(imgcontent)
                f.close()
                log.info('image generated..')
                tele = telegramSender()
                log.info('sending image..')
                tele.sendMsg('rat detected', filePath)
                log.info('removing image..')
                os.remove(filePath)
        except Exception as e:
            log.exception('exception occured')

def main():
    connection = mqttconnection('192.168.2.12', 1883, 'detect/rat')
    connection.subscribe()

if __name__ == "__main__":
    main()
