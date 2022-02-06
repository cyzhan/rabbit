from functools import wraps
from sanic.response import json
from sanic import Request
from pydantic import ValidationError
from ujson import loads


def body_validator(clz):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request: Request, *args, **kwargs):
            try:
                obj = clz(**request.json)
                print('hello before f')
                response = await f(request, *args, **kwargs)
                print('hello after f, before return')
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
