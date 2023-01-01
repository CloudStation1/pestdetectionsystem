from io import BytesIO
import base64
import torch
from picamera2 import Picamera2
from notifier import telegramMsgSender as tele
import time
import numpy as np
from PIL import Image

class ratDetection:

    def __init__(self, telebot, captureIndex, modelWeight, device):
        self.telebot = telebot
        self.device = device
        self.captureIndex = captureIndex
        self.model = self.loadModel(modelWeight)
    
    def loadModel(self, modelWeight):
        model = torch.hub.load('ultralytics/yolov5', 'custom', path=modelWeight)
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
        buffered = BytesIO()
        img_base64 = Image.fromarray(results.ims)
        img_base64.save(buffered, format="JPEG")
        print(base64.b64encode(buffered.getvalue()).decode('utf-8'))
        #results.print()
        #results.save()
        return results
    
    def __call__(self):
        cam = self.get_camera_feed()
        time.sleep(1)

        while True:
            t1 = time.monotonic()
            frame = cam.capture_array()
            results = self.runDetection(frame)
            t2 = time.monotonic()
            fps = 1/np.round(t2-t1, 2)
            print('fps : ' + fps)
        cam.stop()

def main():
    bot = tele.notifier()
    bot.sendMsg('node started..')
    det = ratDetection(bot, captureIndex=0, modelWeight="best.pt", device="cpu")
    det()

if __name__ == "__main__":
    main()
