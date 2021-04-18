import flask, os, json, random, sys, logging, threading
from flask import (Flask, jsonify, session, make_response, redirect,request, render_template, url_for, Response, stream_with_context)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return jsonify({ "error": "Not Allowed!"})

#------------------#
#      USERS       #
#------------------#
from controllers import user
user = user.User()
app.route('/user/registration', methods=['POST'])(user.registerUser)
app.route('/user/login', methods=['POST'])(user.login)

from controllers import sensor
sensor = sensor.Sensor()
app.route('/sensor/cached/reading', methods=['POST'])(sensor.saveCache)
app.route('/sensor/cached/reading', methods=['GET'])(sensor.getCachedReading)
app.route('/sensor/reading', methods=['POST'])(sensor.saveSensorReading)

from controllers import machine_settings
machine_settings = machine_settings.MachineSettings()
app.route('/settings', methods=['POST'])(machine_settings.create_setting)
app.route('/settings', methods=['PUT'])(machine_settings.update_setting)
app.route('/settings', methods=['GET'])(machine_settings.get_setting)

from controllers import incubation
incubation = incubation.Incubation()
app.route('/incubation', methods=['POST'])(incubation.startIncubation)
app.route('/incubation', methods=['GET'])(incubation.getIncubation)


port = os.getenv('PORT', '5050')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port), debug=True)
