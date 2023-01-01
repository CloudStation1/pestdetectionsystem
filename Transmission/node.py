import base64
import json
import os.path as path
from datetime import datetime
from commenFunc import CommenFunc

class Node(CommenFunc):

    def __init__(self, brokerId, port):
        super().__init__(brokerId, port)

    def getImageName(self, img):
        return path.basename(img)

    def isImgFound(self, img):
        if path.exists(img):
            return 1
        else:
            return 0

    def checkResult(self,result, img):
        if (result == 0):
            print('Image('+ self.getImageName(img) +') Sent Sucessfully.')
        else:
            print('Image('+ self.getImageName(img) +') Can not send.')

    def prepareJsonImg(self, img, matchPer):
        try:
            if not self.isImgFound(img):
                raise Exception("Image not Found.")
            f = open(img, 'rb')
            image_byte = base64.b64encode(f.read())
            image_str = image_byte.decode('ascii')  # byte to str
            todaydate = datetime.now()
            data = {
                'img_name' : self.getImageName(img),
                'today_datetime' : todaydate.strftime("%d-%m-%Y %H:%M:%S"),
                'match_percent' : matchPer,
                'img_content' : image_str
            }
            return json.dumps(data)
        except Exception as e:
            print(e)

    def transferData(self, img, matchPer):
        try:
            if not self.isImgFound(img):
                raise Exception("Image not Found.")

            client = self.getMQTTConnection()
            client.loop_start()
            preparedImg = self.prepareJsonImg(img, matchPer)
            result, count = client.publish(self.getTopic(), preparedImg)
            self.checkResult(result, img)
            client.loop_stop()
        except Exception as e:
            print(e)

# p1 = Node('192.168.31.219', 1883);
# p1.setTopic('detect/rat')
# p1.transferData('images/IMG_5981.jfif', 64)