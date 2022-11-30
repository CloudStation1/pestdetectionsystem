from flask import Blueprint, render_template
import requests 
import json
from datetime import datetime
date = datetime.now()
views = Blueprint('views' , __name__)
@views.route('/')




def home():
    page = requests.args.get('page' , 1 , type=int)
    req = requests.get('https://dummyjson.com/products')
    data = json.loads(req.content)
    return render_template('home.html', data=data, datetime = str(datetime.now()))

@views.route("/NodeConfig")
def NodeConfig():
    return render_template('NodeConfig.html')
#  return render_template("home.html")

#  def index():
    # req = request.get('https://api.zalando.com/brands')
    # data = json.loads(req.content)
    # return render_template('index.html', data=data['all'])