import json
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import random
from flask_cors import CORS 

app = Flask(__name__)
api = Api(app)
CORS(app)

import requests
import time

def check_fullbin(x,text):
	if x <= 10:
		url = "http://35.231.245.160:5000/notify/admin/Bin ID "+text+" is Full/none"
		response = requests.get(url)
		print(response)
		return 'Full'
	else:
		return 'Empty'

def bin_percentage(x):
	if x >= 50:
		print(x)
		return '100'
	else:
		percentage = (x/float(50))*100
		print(percentage)
		return str(int(percentage))

bin_color = ['Blue bin','Yellow bin','Red bin','Black bin']

def alert(text):
	url = "35.231.245.160:5000/notify/flood/" + text

@app.route('/api/v1/SmartBin/sensor_id/<id>', methods=['GET', 'POST'])
def get_binstatus(id=None):
	url = "https://cie-smart-city.appspot.com/sensors/sensor_id/" + id
	response = requests.get(str(url))
        bin_status = response.json()
	print(bin_status)
	data = {"id":bin_status["id"], "data":{"percentage":bin_percentage(int(bin_status["data"])), "status":check_fullbin(int(bin_status["data"]),bin_status["id"])}, "location":{"coordinate":bin_status["location"]["coordinate"]}}
	return json.dumps(data)

@app.route('/api/v1/SmartBin/', methods=['GET', 'POST'])
def get_allbinstatus():
        url = "https://cie-smart-city.appspot.com/sensors/project_id/SmartBin"
        response = requests.get(str(url))
        bin_status = response.json()
        print(bin_status)
        all_data = []
        for i in range(len(bin_status)):
            data = {"project_id":"SmartBin","id":bin_status[i]["id"], "data":{"percentage":bin_percentage(int(bin_status[i]["data"])), "status":check_fullbin(int(bin_status[i]["data"]),bin_status[i]["id"])}, "location":{"coordinate":bin_status[i]["location"]["coordinate"]}}
            all_data.append(data)
        return json.dumps(all_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True, debug=True)
