from flask import Flask, jsonify, request
from models.machine_settings import Settings
from library.common import Common
from library.bx_cloudant import BxCloudant

class MachineSettings(Common, BxCloudant):

    def create_setting(self):
        params = request.get_json(force=True)
        time_now = self.getTimeNow()

        machine_id = params.get("machine_id",None)
        if machine_id is None:
            return self.returnFunction({
                    "status": "error",
                    "message": "machine_id not found"
                    })
        settings = Settings(created_at=time_now, updated_at=time_now)
        for key in params:
            settings.__setattr__(key,params[key])

        error = settings.validate()
        if error is not None:
            return self.returnFunction({
                "status": "error",
                "msg": error
            })

        settings_json = settings.to_struct()
        settings_json["_id"] = "machinesettings-"+machine_id

        db_ret = self.saveDocument(settings_json)
        
        if db_ret.get("_id",False):
            ret = {
                "status": "ok",
                "message": "successfully save machine settings",
                "db_ret": db_ret
                    }
        else:
            ret = {
                "status": "error",
                "message": db_ret.get("error","failed to save to db."),
                "db_ret": db_ret
                    }
        return self.returnFunction(ret)


    def update_setting(self): 
        params = request.get_json(force=True)
        time_now = self.getTimeNow()

        machine_id = params.get("machine_id",None)
        if machine_id is None:
            return self.returnFunction({
                    "status": "error",
                    "message": "machine_id not found"
                    })
        fields = params.get("fields",{})

        doc = self.getDocumentById(machine_id)

        if (not doc) or ("error" in doc):
            return self.returnFunction({
                    "status": "error",
                    "message": "machine settings not found"
                    })

        to_update_list = [{"field": "updated_at", "value": time_now}]
        for key in doc:
            val = fields.get(key,None)
            if val != None:
                to_update_list.append({
                    "field": key,
                    "value": val
                    })

        print("to_update: ",to_update_list)

        db_ret = self.update_doc_fields(machine_id, to_update_list)

        return self.returnFunction({
            "status": "ok",
            "message": "successfully update machine settings",
            "db_ret": db_ret
            })

    def get_setting(self):

        machine_id = request.args.get('machine_id', None)

        if machine_id is None:
            return self.returnFunction({
                "status": "error",
                "message": "machine_id not found"
                })

        doc = self.getDocumentById("machinesettings-"+machine_id)
        if (not doc) or ("error" in doc):
            return self.returnFunction({
                    "status": "error",
                    "message": "machine settings not found"
                    })
        else:
            return self.returnFunction({
                "status": "ok",
                "settings": doc
                })


                
                












