import sys
sys.path.append('../')

from io import BytesIO
import base64
import torch
from picamera2 import Picamera2
import time
import numpy as np
from PIL import Image
import base64
import json
import os.path as path
from datetime import datetime
import paho.mqtt.client as mqtt
import logging
from logging.handlers import RotatingFileHandler

#logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logFile = 'detect2.log'
log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')

my_handler = RotatingFileHandler(logFile, mode='a', maxBytes=5*1024*1024, backupCount=2, encoding=None, delay=0)

my_handler.setFormatter(log_formatter)
my_handler.setLevel(logging.DEBUG)

app_log = logging.getLogger('root')
app_log.setLevel(logging.DEBUG)

app_log.addHandler(my_handler)


class mqttClient():

    def __init__(self, brokerId, port, topic):
        self.brokerId = brokerId
        self.port = port
        self.topic = topic
        self.isConnected = False
        self.client = self.setupConnection()

    def checkResult(self,result):
        if (result == 0):
            app_log.info('Sent Sucessfully.')
        else:
            app_log.error('Image Can not send.')

    def prepareJsonImg(self, data, matchPer):
        try:
            #f = open(img, 'rb')
            #image_byte = base64.b64encode(f.read())
            #image_str = image_byte.decode('utf-8')  # byte to str
            #todaydate = datetime.now()
            data = {
                'img_name' : 'rat',
                'today_datetime' : datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                'match_percent' : matchPer,
                'img_content' : data
            }
            return json.dumps(data)
        except Exception as e:
            app_log.error(str(e))

    def transferData(self, data, matchPer):
        try:
            if self.isConnected == False:
                self.connect()
            self.client.loop_start()
            preparedImg = self.prepareJsonImg(data, matchPer)
            result, count = self.client.publish(self.topic, preparedImg)
            self.checkResult(result)
            self.client.loop_stop()
        except Exception as e:
            app_log.error(str(e))
            
    def setupConnection(self):
            client = mqtt.Client()
            client.on_connect = self.on_connect
            client.on_disconnect = self.on_disconnect
            return client
    
    def connect(self):
        try:
            self.client.connect(self.brokerId, self.port)
        except Exception as e:
            app_log.error(str(e))

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            app_log.info('Connected to Broker ' + self.brokerId)
            self.isConnected = True
        else:
            app_log.warning("Failed to connect, return code %d\n", rc)
            
    def on_disconnect(self, client, userdata, rc):
            app_log.warning("Disconnected from broker: %d\n", rc)
            self.isConnected = False

class ratDetection:

    def __init__(self, mqttsender, captureIndex, modelWeight, device):
        self.device = device
        self.captureIndex = captureIndex
        self.mqttsender = mqttsender 
        self.model = self.loadModel(modelWeight)
    
    def loadModel(self, modelWeight):
        model = torch.hub.load('ultralytics/yolov5', 'custom', path=modelWeight)
        model.conf = 0.60
        model.iou = 0.45
        return model

    def setModelConfig(self, confidance=0.4):
        self.confidance = confidance

    def get_camera_feed(self):
        picam = Picamera2()
        picam.start()
        return picam

    def runDetection(self, frame):
        self.model.to(self.device)
        results = self.model(frame)
        if results.pandas().xyxy[0].empty == False:
            x0, y0, x1, y1, c, d =results.xyxy[0][0]
            detectionConfidance = np.round(c.numpy().astype(float), 3);
            app_log.info(f"rat detected with confidance of {detectionConfidance}%")
            results.render()
            for img in results.ims:
                buffered = BytesIO()
                img_base64 = Image.fromarray(img)
                img_base64.save(buffered, format="JPEG")
                #print(base64.b64encode(buffered.getvalue()).decode('utf-8'))
                self.mqttsender.transferData(base64.b64encode(buffered.getvalue()).decode('utf-8'), str(detectionConfidance))
    
    def __call__(self):
        cam = self.get_camera_feed()
        time.sleep(1)

        while True:
            t1 = time.monotonic()
            frame = cam.capture_array()
            self.runDetection(frame)
            t2 = time.monotonic()
            fps = 1/np.round(t2-t1, 2)
            app_log.info('Current FPS: ' + str(round(fps,3)))
        cam.stop()

def main():
    mqttsender = mqttClient('192.168.2.12', 31736, 'detect/rat')
    det = ratDetection(mqttsender, captureIndex=0, modelWeight="best.pt", device="cpu")
    det()

if __name__ == "__main__":
    main()
