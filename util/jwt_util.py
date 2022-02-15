import base64
import hashlib
import hmac
import os

from sanic import Request
from exception.UnAuthorizedException import UnAuthorizedException

SALT2 = os.getenv("SALT2")


# def login_verify(request: Request):
#     token = request.headers["Authorization"]
#     if token is None:
#         raise UnAuthorizedException('unauthorized')
#     else:
#         return verify(token)


# def verify(jwt):
#     ary = jwt.split('.')
#     string = ary[0] + '.' + ary[1]
#     raw = hmac.new(bytes(SALT2, encoding="utf-8"), bytes(string, encoding="utf-8"), digestmod=hashlib.sha256).digest()
#     signature = str(base64.b64encode(raw), 'utf-8')
#     if signature != ary[2]:
#         raise UnAuthorizedException('unauthorized signature')
#
#     body_dict = json.loads(base64.b64decode(ary[1]))
#     ts = time.time()
#     if int(ts) > body_dict['exp']:
#         raise UnAuthorizedException('token expired')
#     return body_dict
