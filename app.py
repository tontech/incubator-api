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

port = os.getenv('PORT', '5050')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port), debug=True)
