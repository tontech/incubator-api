import os,sys,logging,ast,json
from datetime import datetime, date, timedelta as td
from flask import jsonify
import pytz
import hashlib
from pyblake2 import blake2b
from hmac import compare_digest


lib_path = os.path.abspath(os.path.join(".."))
sys.path.append(lib_path)

class Common:

    def returnFunction(self, return_object):
        return jsonify(return_object)


    def readJson(self,_file):
        config = {}
        with open('%s.json' % _file, 'r') as f:
            config = json.load(f)
            logging.info("Read Json File : %s" % config)

        return config


    def getTimeNow(self):
        return datetime.now(pytz.timezone('Asia/Manila')).strftime("%Y-%m-%d %H:%M:%S")
    
    def getEpochTime(self):
        return datetime.now(pytz.timezone('Asia/Manila')).strftime("%s")

    def str2DateTime(self, dt_str):
        return datetime.strptime(dt_str,"%Y-%m-%d %H:%M:%S")

    def getDTObject(self):
        return datetime.now()+td(hours=8)

    def blake2bHashing(self, str_ing):
        config = self.readJson("config")
        config_hash = config["HASHING"]
        h = blake2b(digest_size=config_hash["AUTH_SIZE"], key=config_hash["SECRET_KEY"].encode('utf-8'))
        h.update(str_ing.encode('utf-8'))
        return h.hexdigest()

    def verifyHash(self, str_ing, hashed_string):
        good_hash = self.blake2bHashing(str(str_ing))
        return compare_digest(str(good_hash),str(hashed_string))

