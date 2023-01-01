import json
import base64
import os
import io
from commenFunc import CommenFunc
from minio import Minio

class Cluster(CommenFunc):

    def subscribe(self):
        client = self.getMQTTConnection()
        client.subscribe(self.getTopic())
        client.on_message = self.onMessage
        client.loop_forever()

    def onMessage(self, client, userdata, msg):
        try:
            if (msg.topic == self.getTopic()):
                client = self.getMinIO()
                if client.bucket_exists(self.bucketName):
                    client.put_object(self.bucketName, self.getJsonFileName(msg.payload), io.BytesIO(msg.payload), len(msg.payload), content_type = self.contentType)
                    print('File uploaded to Minio')
        except Exception as e:
            print(e)

    def getJsonFileName(self, payload):
        m_in = json.loads(str(payload.decode('utf-8','ignore')))
        filename, file_extension = os.path.splitext(m_in['img_name'])
        return filename + '(' + m_in['today_datetime'] + ').json'

    def getMinIO(self):
        return Minio(
            self.hostName,
            access_key = self.accessKey,
            secret_key = self.secretKey,
            secure=False
        )

    def setMinIoConfig(self, hostName, accessKey, secretKey, bucketName, contentType):
        self.hostName = hostName
        self.accessKey = accessKey
        self.secretKey = secretKey
        self.bucketName = bucketName
        self.contentType = contentType

# cl = Cluster('192.168.31.219', 1883)
# cl.setTopic('detect/rat')
# cl.setMinIoConfig('localhost:9000','78SHN5mbnrYYoOy2','as1QQn2Gnhepvx3E2tJ6vZLnUGVkZmLY','cloud','application/json')
# cl.subscribe()