from jsonmodels import models, fields, errors, validators

class IncubationModel(models.Base):
    updated_at = fields.StringField(required=True)
    created_at = fields.StringField(required=True)
    machine_id = fields.StringField(required=True)
    start_date = fields.StringField(required=True)
    end_date = fields.StringField(required=True)
    type = fields.StringField(required=True, default="incubation")
