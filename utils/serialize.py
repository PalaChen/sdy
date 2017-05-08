from json.encoder import JSONEncoder
import datetime


class DateTypeJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            r = o.isoformat()
            r = r.replace('T', '  ')
            if o.microsecond:
                r = r[:23] + r[26:]
            if r.endswith('+00:00'):
                r = r[:-6]
            return r
