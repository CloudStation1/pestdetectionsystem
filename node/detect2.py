import torch
from picamera2 import Picamera2
import time

class ratDetection:

    def __init__(self, captureIndex, modelWeight, device):
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
        results.print()
        results.save()
        return results
    
    def __call__(self):
        cam = self.get_camera_feed()
        time.sleep(1)

        while True:
            frame = cam.capture_array()
            results = self.runDetection(frame)
            break
        cam.stop()



def main():
    im = './test_data/test.jpg'
    #runDetection(im)
    det = ratDetection(captureIndex=0,modelWeight="best.pt", device="cpu")
    det()

if __name__ == "__main__":
    main()
