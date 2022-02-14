from sanic.response import json
from sanic import response

response_ok = json({'code': 0, 'msg': 'ok'})


def response_ok_of(data: dict) -> response:
    return json({'code': 0, 'msg': 'ok', 'data': data})
