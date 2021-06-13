import logging, json, os, requests,time

from cloudant.client import Cloudant
from cloudant.view import View
from cloudant.design_document import DesignDocument
from cloudant.adapters import Replay429Adapter
from cloudant import cloudant_bluemix

from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

from library.common import Common

class BxCloudant:

    client = ""
    env = ""
    mydb = ""
    cloudantInfo = {}
    dbInfo = {}



    def __init__(self):
        common = Common()
        global cloudantInfo,dbInfo,env,mydb,client
        appConfig=common.readJson('config')
        if 'VCAP_SERVICES' in os.environ and 'cloudantNoSQLDB' in json.loads(os.getenv('VCAP_SERVICES')):
            vcap = json.loads(os.getenv('VCAP_SERVICES'))
            cloudantInfo = vcap['cloudantNoSQLDB'][0]['credentials']
        else:
            cloudantInfo=appConfig['CLOUDANT']

        client = Cloudant(cloudantInfo['username'], cloudantInfo['password'], url=cloudantInfo['url'], adapter=Replay429Adapter(retries=20, initialBackoff=0.1),
            connect=True, auto_renew=True)
        
        dbInfo = appConfig['DATABASE']
        env = appConfig['ENVIRONMENT']
        mydb = self.getDatabase(dbInfo[env])

    def createDatabase(self, dbname):
        global client
        mydb = client.create_database(dbname)

        if mydb.exists():
            return True
        else:
            return False

    def getDatabase(self, dbname):
        global client
        mydb = client[dbname]
        return mydb

    def saveDocument(self, doc):
        global mydb
        return mydb.create_document(doc)
    
    def bulkDocuments(self,doc_list):
        global mydb
        save_doc = mydb.bulk_docs(doc_list)
        return save_doc


    def getDocumentRangeKey(self, design, view, is_desc=True, start_key="", end_key="", limit=False ):
        global mydb
        view_connect = View(DesignDocument(mydb,document_id=design),view)
        if limit:
            return view_connect(descending=is_desc, startkey=start_key, endkey=end_key, limit=limit)['rows']
        else:
            return view_connect(descending=is_desc, startkey=start_key, endkey=end_key)['rows']
    
    def getDocumentByKey(self, design, view, key=False, is_desc=True, limit=False):
        global mydb
        view_connect = View(DesignDocument(mydb,document_id=design),view)
        if key:
            if limit:
                return view_connect(descending=is_desc, key=key, limit=limit)['rows']
            else:
                return view_connect(descending=is_desc, key=key)['rows']
        else:
            return view_connect(descending=is_desc)['rows']
    
    def getDocumentFilter(self,design, view, is_desc=True, emit="", limit=False):
        global cloudantInfo,dbInfo,env
        sort_by = ""
        if is_desc:
            sort_by = "descending=true&"
        url = "https://%s:%s@%s/%s/_design/%s/_view/%s?%s%s"%(cloudantInfo['username'], cloudantInfo['password'],cloudantInfo['host'], dbInfo[env], design, view, sort_by, emit)
        if limit:
            url += '&limit=%d'%limit

        # EXECUTE GET REQUEST
        result = requests.get(url)

        # CONVERT TO JSON
        json_data = result.json()
        logging.info("JSON RESERVED : %s " % str(json_data))

        # GET VALUE
        rows = []
        if json_data:
            if (not json_data) or "error" in json_data:
                time.sleep(1)
                result = requests.get(url)
                json_data = result.json()
                if "rows" in json_data:
                    rows = json_data["rows"]
                logging.info("JSON RESERVED : %s " % str(json_data.get('reason')))
            else: rows = json_data["rows"]

        return rows

    def getDocumentById(self, Id):
        global cloudantInfo,dbInfo,env
        url = "https://%s:%s@%s/%s/%s"%(cloudantInfo['username'], cloudantInfo['password'],cloudantInfo['host'], dbInfo[env], Id)

        # EXECUTE GET REQUEST WITH RETRY AND BACKOFF FACTOR
        s = requests.Session()
        retries = Retry(total=5,backoff_factor=0.1)
        s.mount('http://', HTTPAdapter(max_retries=retries))
        result = s.get(url)

        # CONVERT TO JSON
        json_data = result.json()
        logging.info("JSON RESERVED : %s " % str(json_data))
        return json_data

    def fetch_document(self, doc_id):
        global mydb
        if doc_id in mydb:
            return mydb[doc_id]
        else:
            return False
	
    def delete_document(self, doc_id):
        global mydb
        # First retrieve the document
        my_document = mydb[doc_id]

        # Delete the document
        my_document.delete()

    def fetch_document_bulk(self, doc_ids, fields=False):
        global mydb
        selector = {
                "_id": {
                      "$in": doc_ids
                    }
                }
        if fields:
            resp = mydb.get_query_result(selector, raw_result=True, fields=fields)
        else:
            resp = mydb.get_query_result(selector, raw_result=True)
        return resp.get('docs',[])

    def fetch_document_by_selector(self, selector, fields = False):
        global mydb
        if fields:
            resp = mydb.get_query_result(selector, fields=fields, raw_result=True)
        else:
            resp = mydb.get_query_result(selector, raw_result=True)
        return resp.get('docs',[])

    def update_doc_fields(self, doc_id, doc_fields):
        global mydb
        doc = mydb[doc_id]

        for obj in doc_fields:
            doc[obj.get("field")] = obj.get("value","")

        return doc.save()

    def update_doc_field(self, doc_id, field, value):
        global mydb
        doc = mydb[doc_id]
        ret = doc.update_field(
                action=doc.field_set,
                field=field,
                value=value,
                max_tries=10
            )
        return ret

