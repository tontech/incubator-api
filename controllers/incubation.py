import logging, json, time

from flask import Flask, jsonify, request
from models.incubation import IncubationModel
from library.common import Common
from library.bx_cloudant import BxCloudant


class Incubation(BxCloudant, Common):
    
    def startIncubation(self):
        params = request.get_json(force=True)
        ret = {
                "status": "error",
                "message": ""
                }
        
        time_now = self.getTimeNow()
        start_date = params.get("start_date",False)
        if start_date is False:
            return self.returnFunction({
                "status": "error",
                "message": "start_date not found"
                })
        machine_id = params.get("machine_id",False)
        if machine_id is False:
            return self.returnFunction({
                "status": "error",
                "message": "machine_id not found"
                })
        incubation_id = "incubation-"+str(machine_id)

        machine_settings = self.getDocumentById("machinesettings-"+machine_id)
        incubation_days = 26
        if machine_settings and machine_settings.get("value",False):
            incubation_days = machine_settings["value"].get("incubation_days",26)
        end_date = self.getEndDate(start_date, incubation_days)


        time.sleep(0.5)
        incubation = self.getDocumentById(incubation_id)
        print("incubation: ",incubation)
        if incubation and incubation.get("_id",False):
            to_update_list = [
                {
                    "field": "updated_at", 
                    "value": time_now
                },
                {
                    "field": "start_date", 
                    "value": start_date
                },
                {
                    "field": "end_date", 
                    "value": end_date
                },
            ]

            db_ret = self.update_doc_fields(machine_id, to_update_list)

            ret = {
                "status": "ok",
                "message": "successfully update machine incubation.",
                "db_ret": db_ret
            }
        else:
            incubation = IncubationModel(created_at=time_now, updated_at=time_now, machine_id=machine_id, \
                start_date=start_date, end_date=end_date)
            incubation_json = incubation.to_struct()
            incubation_json["_id"] = incubation_id

            db_ret = self.saveDocument(incubation_json)
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

    def getIncubation(self):

        machine_id = request.args.get('machine_id', None)
        time_now = self.getTimeNow()

        if machine_id is None:
            return self.returnFunction({
                "status": "error",
                "message": "machine_id not found"
                })

        doc = self.getDocumentById("incubation-"+machine_id)

        if (not doc) or ("error" in doc):
            ret = {
                "status": "error",
                "message": "incubation data not found"
            }
        else:
            doc["start_date"] = "2021-04-15 15:14:34"
            incubation_days = self.getDateDifference(time_now,doc["start_date"])
            incubation_period = self.getDateDifference(doc["end_date"],doc["start_date"])
            incubation_percentage = (float(incubation_days)/float(incubation_period)) * 100
            doc["incubation_days"] = incubation_days
            doc["incubation_percentage"] = round(incubation_percentage,2)
            ret = {
                "status": "ok",
                "incubation": doc
            }
        return self.returnFunction(ret)

