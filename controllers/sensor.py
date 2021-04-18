import logging, json

from flask import Flask, jsonify, request
from models.sensor import Sensor
from library.tiny_db import TinyDb
from library.bx_cloudant import BxCloudant
from library.common import Common


class Sensor(Sensor, TinyDb, BxCloudant, Common):

    def saveCache(self):
        params = request.get_json(force=True)
        ret = {
                "status": "error",
                "message": ""
                }

        sensor_reading = self.new(params)

        print("sensor Reading: ",sensor_reading)

        if sensor_reading["status"] == "ok":
            docs = self.getCachedDocs("type","sensor-reading")
            doc = sensor_reading.get("doc",{})
            if len(docs)>0:
                self.updateCachedDoc(doc,"type","sensor-reading")
            else:
                self.saveCachedDoc(doc)
            ret["status"] = "ok"
            ret["message"] = "Successfuly cached sensor reading"
        else:
            ret["message"] = sensor_reading.get("message", "Something went wrong :(")

        return self.returnFunction(ret)

    def getCachedReading(self):
        ret = {
                "status": "error",
                "message": ""
                }
        docs = self.getCachedDocs("type","sensor-reading")

        if len(docs)>0:
            ret["status"] = "ok"
            ret["message"] = "Cached reading found."
            ret["reading"] = docs[0]
        else:
            ret["message"] = "No cached sensor reading found"

        return self.returnFunction(ret)

    def saveSensorReading(self):
        params = request.get_json(force=True)
        ret = {
                "status": "error",
                "message": ""
                }

        sensor_reading = self.new(params)

        print("sensor Reading: ",sensor_reading)

        if sensor_reading["status"] == "ok":
            doc = sensor_reading.get("doc",{})
            self.saveDocument(doc)
            ret["status"] = "ok"
            ret["message"] = "Successfuly saved sensor reading"
        else:
            ret["message"] = sensor_reading.get("message", "Something went wrong :(")

        return self.returnFunction(ret)


