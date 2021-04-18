class Sensor:

    keys = [
            "timestamp",
            "machine_id",
            "temperature",
            "humidity"
            ]


    def new(self, params):
        ret = {
                'status': 'ok',
                'message': 'ok',
                'doc': {
                    'created_at': self.getTimeNow(),
                    'type': 'sensor-reading'
                    }
                }
        for key in self.keys:
            if key in params:
                ret['doc'][key] = params[key]
            else:
                ret['status'] = 'error'
                ret['message'] = 'missing parameter: '+key
                break

        return ret
