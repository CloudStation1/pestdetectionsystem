from flask import Blueprint, render_template
import json
from minio import Minio
import logging
from datetime import datetime

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

views = Blueprint('views' , __name__)

@views.route('/')
def home():
    return render_template('home.html', data=getData())

def getMinIOConnection():
    return Minio(
        '192.168.2.12:9000',
        access_key='minio',
        secret_key='minio123',
        secure= False)

def getData():
    try:
        client = getMinIOConnection()
        if client.bucket_exists("pestdetection"):
            objects = client.list_objects("pestdetection")
            newDataObj = []
            for obj in objects:
                response = client.get_object(obj.bucket_name,obj.object_name)
                jsonFileContant = json.loads(response.read())
                fileName = jsonFileContant['img_name']
                jsonFileContant['content-type'] = 'image/'+ fileName.split('.')[-1]
                newDataObj.append(jsonFileContant)
                log.info('Object file name : ' + fileName)
            #log.info('Total objects found : ' + str(len(newDataObj)))
            newDataObj.sort(key=lambda newDataObj: datetime.strptime(newDataObj['today_datetime'], "%d-%m-%Y %H:%M:%S"), reverse=True)
            return newDataObj
        else:
            log.error("my-bucket does not exist")
    except Exception as ex:
        log.exception('exception occured')

@views.route('/update')
def On_ObjectAddition():
    client = getMinIOConnection()
    newDataObj = []
    events = client.listen_bucket_notification('pestdetection', events=['s3:ObjectCreated:*']) 
    for event in events:
        objname = event['Records'][0]['s3']['object']['key']
        response = client.get_object('pestdetection', objname)
        jsonFileContant = json.loads(response.read())
        fileName = jsonFileContant['img_name']
        jsonFileContant['content-type'] = 'image/'+ fileName.split('.')[-1]
        newDataObj.append(jsonFileContant)
        break
    log.info('new object added in db :', jsonFileContant['img_name'])
    return newDataObj
