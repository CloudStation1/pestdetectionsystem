from flask import Blueprint, render_template
import json
from minio import Minio
import logging

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
        access_key='FdCYXa7zP0ujveAh',
        secret_key='j3YyW3bBZ9CIBK58PgZ0B2FkyLec7OJk',
        secure= False)

def getData():
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
        return newDataObj
    else:
        print("my-bucket does not exist")