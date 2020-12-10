from datetime import datetime
import pytz
class User:

    keys = [
           "name",
           "mobile_number",
           "email",
           "password",
            ]

    def new(self, params):
        ret = {
                'status': 'ok',
                'message': 'ok',
                'doc': {
                    'created_at': self.getTimeNow(),
                    'type': 'user'
                    }
                }
        for key in self.keys:
            if key in params:
                if key=='password':
                    ret['doc'][key] = self.blake2bHashing(params[key])
                else:
                    ret['doc'][key] = params[key]
            else:
                ret['status'] = 'error'
                ret['message'] = 'missing parameter: '+key
                break

        return ret

