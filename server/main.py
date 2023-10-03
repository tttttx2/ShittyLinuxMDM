from flask import Flask, request, render_template, send_from_directory, redirect
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from os import listdir
import uuid
import json
import glob
import os

app = Flask(__name__)

# Setup basic auth
auth = HTTPBasicAuth()
users = {
    "admin": generate_password_hash(os.getenv('ADMIN_PASS')),
}


@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username



# Setup redirect and hosting of frontend

@app.route('/')
def redirect_to_client():
   return redirect('client/index.html')

@app.route('/client/<path:path>')
def client(path):
    return send_from_directory('../client', path)

# API and thus the backend functionality

# create new device
@app.route('/api/devices/create')
@auth.login_required
def api_device_create():
    token = str(uuid.uuid1())
    filename = '/app/data/devices/{}/metadata.json'.format(token)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    f = open(filename, 'w')
    f.write(json.dumps({'token':token, 'hostname':'N/A', 'status':'onboarding'}))
    f.close()

    filename = '/app/data/devices/{}/onboarding.sh'.format(token)
    f = open(filename, 'w')
    f.write("TODO: DEFINE ONBOARDING SCRIPT")
    f.close()
    return token

# list all devices
@app.route('/api/devices')
@auth.login_required
def api_devices():
    devices = [i.split('/')[-1] for i in glob.glob(f'/app/data/devices/*', recursive=False)]
    return json.dumps(devices)

# list specific device
@app.route('/api/devices/<path:device>')
@auth.login_required
def api_device_list(device):
    #TODO: Input sanitization
    filename = '/app/data/devices/{}/metadata.json'.format(device)
    f = open(filename)
    data = json.loads(f.read())
    if data['status']=='onboarding':
        data["message"] = "Please run the onboarding command 'curl https://{}/devices/{}/script/onboarding.sh | sh -' on the device".format(os.getenv('URL'), device)
    return json.dumps(data)

# expose client config scripts
@app.route('/api/devices/<path:device>/script/<path:script>')
def api_device_file(device, script):
    return send_from_directory('/app/data/devices/{}'.format(device), script)

if __name__ == '__main__':
    app.debug = True
    app.run(port=80, host="0.0.0.0")
