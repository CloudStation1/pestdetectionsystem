import torch

model = torch.hub.load('ultralytics/yolov5', 'custom', path='./best.pt')

def setModelConfig():
    model.conf = 0.50

def runDetection(img):
    results = model(img)
    results.print()
    results.save()

def main():
    im = './test_data/test.jpg'
    runDetection(im)

if __name__ == "__main__":
    main()