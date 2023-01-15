from flask import Blueprint, render_template
import json
from minio import Minio
views = Blueprint('views' , __name__)
@views.route('/')

def home():
    return render_template('home.html', data=getData())

def getMinIOConnection():
    return Minio(
        'localhost:9000',
        access_key='wXMsa1UNIhxrLdeF',
        secret_key='IscMoplpUPsvrECse4yPURoXHtMugyBB',
        secure= False)

def getData():
    client = getMinIOConnection()
    if client.bucket_exists("cloud"):
        objects = client.list_objects("cloud")
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