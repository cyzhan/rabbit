class LogicErrorException(Exception):
    code = 500
    msg = 'internal error'

    def __init__(self, code=None, msg=None):
        Exception.__init__(self)
        if code is not None:
            self.code = code
        if msg is not None:
            self.msg = msg

    def to_dict(self):
        return {"code": self.code, "msg": self.msg}
