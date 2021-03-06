from flask import Flask, abort, jsonify, request
import requests
from requests.exceptions import ConnectionError

import galaxyctl_run 

app = Flask(__name__)

@app.route('/galaxyctl_api/v1.0/galaxy-startup', methods=['POST'])
def galaxy_startup():

    # check if galaxy is online, if yes return online
    # else run galaxy-startup script

    if not request.json or not 'endpoint' in request.json:
       abort(400)

    endpoint = request.json['endpoint']

    try:
      response = requests.get(endpoint, verify=False)
    except ConnectionError as e:
      # restart nginx to prevent connection refused
      galaxyctl_run.restart_nginx()
      response = requests.get(endpoint, verify=False)

    sc = str(response.status_code)

    if sc == '200' or sc == '302':
      return jsonify({'galaxy': 'online' }) 

    else:

     return galaxyctl_run.galaxy_startup(endpoint)
