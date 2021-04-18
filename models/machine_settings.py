from jsonmodels import models, fields, errors, validators

class Settings(models.Base):
    updated_at = fields.StringField(required=True)
    created_at = fields.StringField(required=True)
    humidity_min =  fields.FloatField(required=True, default=50)
    humidity_max =  fields.FloatField(required=True, default=60)
    temperature_min =  fields.FloatField(required=True, default=36)
    temperature_max =  fields.FloatField(required=True, default=42)
    incubation_days = fields.IntField(required=True, default=26)
    tilting_interval = fields.FloatField(required=True, default=4)
    heater = fields.BoolField(required=True, default=False)
    heater_fan_motor = fields.BoolField(required=True, default=False)
    humidifier = fields.BoolField(required=True, default=False)
    humidifier_fan_motor = fields.BoolField(required=True, default=False)
    type = fields.StringField(required=True, default="settings")
