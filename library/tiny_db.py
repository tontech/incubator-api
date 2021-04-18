import logging, json, os, requests,time
from tinydb import TinyDB, Query

class TinyDb:

    def __init__(self):
        self.cacheDB = TinyDB('cached_documents.json')
        self.cacheQuery = Query()

    def saveCachedDoc(self,json_data):
        return self.cacheDB.insert(json_data)

    def updateCachedDoc(self,json_data,key,val):
        return self.cacheDB.update(json_data, self.cacheQuery[key] == val)

    def getCachedDocs(self,key,val):
        docs = self.cacheDB.search(self.cacheQuery[key] == val)
        return docs

