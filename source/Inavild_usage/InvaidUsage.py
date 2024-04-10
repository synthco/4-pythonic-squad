
class InvaidUsage(Exception):
    def __init__(self, msg, status_code = None, payload = None):
        self.message = msg
        if status_code is not None:
            self.status_code = status_code
        if payload is not None:
            self.payload = payload


    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


