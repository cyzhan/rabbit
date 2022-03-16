class UnAuthorizedException(Exception):
    status_code = 401

    def __init__(self, message):
        Exception.__init__(self)
        self.message = message

    def to_dict(self):
        return {"code": self.status_code, "msg": self.message}