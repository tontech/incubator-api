import logging, json, time

from flask import Flask, jsonify, request
from library.common import Common
from library.bx_cloudant import BxCloudant

class Report(BxCloudant, Common):

    def getNotifications(self):

        notifs = self.getDocumentByKey(design="notification", view="getNotifications", is_desc=True, limit=100)
        if notifs and len(notifs) > 0:
            notifs  = list(map(lambda x: x["value"], notifs))
            notifs.sort(key=lambda x: x.get('timestamp',''), reverse=True)
            notifs = notifs[:100]
        else:
            notifs = []

        ret = dict()
        ret["status"] = "ok"
        ret["message"] = "Success"
        ret["notifs"] = notifs
        
        return self.returnFunction(ret)

    def getReached(self):
        notifs = self.getDocumentByKey(design="notification", view="getMinMaxNotif", is_desc=True)
        if notifs and len(notifs) > 0:
            notifs  = list(map(lambda x: x["value"], notifs))
            notifs.sort(key=lambda x: x.get('timestamp',''), reverse=True)
            notifs = notifs[:20]
        else:
            notifs = []

        ret = dict()
        ret["status"] = "ok"
        ret["message"] = "Success"
        ret["reaches"] =  notifs
        
        return self.returnFunction(ret)


    def getLatestScan(self):
        notifs = self.getDocumentByKey(design="notification", view="getLatestScan", is_desc=True)
        if notifs and len(notifs) > 0:
            notifs  = list(map(lambda x: x["value"], notifs))
            notifs.sort(key=lambda x: x.get('timestamp',''), reverse=True)
            notifs = notifs[0]
            del notifs["title"]
            del notifs["message"]
            del notifs["notif_type"]
            del notifs["type"]
        else:
            notifs = {}

        ret = dict()
        ret["status"] = "ok"
        ret["message"] = "Success"
        ret["scan"] = notifs  
        
        return self.returnFunction(ret)

