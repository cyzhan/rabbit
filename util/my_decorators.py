from functools import wraps
from sanic.response import json
from sanic import Request
from pydantic import ValidationError
from ujson import loads


def body_validator(clz: type):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request: Request, *args, **kwargs):
            try:
                obj = clz(**request.json)
                response = await f(request, *args, **kwargs, body=obj)
                return response
            except ValidationError as e:
                print(e.json())
                ary = loads(e.json())
                msg1 = ary[0]['loc'][0]
                return json({
                    "code": 40000,
                    "msg": "invalided input {}".format(msg1)
                }, status=400)
        return decorated_function
    return decorator
