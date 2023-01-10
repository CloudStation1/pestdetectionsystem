import json
import base64
import os
import io
from commenFunc import CommenFunc
from minio import Minio
import uuid
import logging

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

class Cluster(CommenFunc):

    def subscribe(self):
        client = self.getMQTTConnection()
        client.subscribe(self.getTopic())
        client.on_message = self.onMessage
        client.loop_forever()
        log.info('subscribed to topic:' + self.getTopic())

    def onMessage(self, client, userdata, msg):
        try:
            log.info('mqtt msg received')
            if (msg.topic == self.getTopic()):
                client = self.getMinIO()
                if client.bucket_exists(self.bucketName):
                    client.put_object(self.bucketName, self.getJsonFileName(), io.BytesIO(msg.payload), len(msg.payload), content_type = self.contentType)
                    log.info('File uploaded to Minio')
        except Exception as e:
            log.exception('exception occured')

    def getJsonFileName(self):
        return uuid.uuid4().hex + '.json'

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

def main():
    log.debug('mqttreceiver started..')
    cl = Cluster('192.168.178.38', 32267)
    cl.setTopic('detect/rat')
    cl.setMinIoConfig('192.168.178.38:30544','SvgpyrBtHEp5QEXe','AJess9U1cPLxqejFkDGikM4Is1ftie0e','pestdetection','application/json')
    cl.subscribe()

if __name__ == "__main__":
    main()