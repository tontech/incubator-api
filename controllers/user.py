import logging, json

from flask import Flask, jsonify, request
from models.user import User
from library.bx_cloudant import BxCloudant
from library.common import Common

class User(BxCloudant, Common, User):

    def registerUser(self):
        params = request.get_json(force=True)
        ret = {
                "status": 'error',
                "message": 'User Exist!'
                }
        user_data = self.new(params)
        if user_data['status']=='ok':
            print("user_data: ",user_data)
            self.saveDocument(user_data['doc'])
            ret['status'] = 'ok'
            ret['message'] = 'successfully created user'
            return self.returnFunction(ret)
        else:
            ret['message'] = user_data['message']
            return self.returnFunction(ret)

    def login(self):
        params = request.get_json(force=True)
        ret = {}

        email = params.get("email",False)
        password = params.get("password",False)

        if not (email and password):
            ret["status"] = "error"
            ret["message"] = "incomplete fields"

        docs = self.getDocumentByKey(design="user",view="userByEmail",key=email)

        if docs:
            doc = docs[0].get("value")
            if self.verifyHash(password,doc.get("password")):
                ret["status"] = "ok"
                ret["message"] = "Login success!"
            else:
                ret["status"] = "error"
                ret["message"] = "Login failed."
        else:
            ret["status"] = "error"
            ret["message"] = "User not found."

        return self.returnFunction(ret)


