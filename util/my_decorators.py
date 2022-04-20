from functools import wraps
from sanic.response import json
from sanic import Request
from pydantic import ValidationError
from ujson import loads
from exception.unauthorized_exception import UnAuthorizedException
from .jwt_util import verify2, create
import os
import time
from .redis_util import r as redis
from .redis_util import RedisKey

TOKEN_PERIOD = int(os.getenv("TOKEN_PERIOD"))
RENEW_MARGIN = int(os.getenv("RENEW_MARGIN"))


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
                    "msg": "invalided input [{}]".format(msg1)
                }, status=400)
        return decorated_function
    return decorator


def list_body_validator(clz: type):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request: Request, *args, **kwargs):
            try:
                obj = clz(items=request.json)
                response = await f(request, *args, **kwargs, items=obj.items)
                return response
            except ValidationError as e:
                print(e.json())
                ary = loads(e.json())
                msg1 = ary[0]['loc'][0]
                return json({
                    "code": 40000,
                    "msg": "invalided input [{}]".format(msg1)
                }, status=400)
        return decorated_function
    return decorator


def authorized():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request: Request, *args, **kwargs):
            jwt: str = request.headers["Authorization"]
            is_authorized: bool
            token_body = verify2(jwt=jwt)
            ary = jwt.split('.')
            signature: str = ary[2]
            current_ts = int(time.time())
            renewable: bool = current_ts > (token_body.exp - RENEW_MARGIN)
            sign_in_redis: bool = redis.get(RedisKey.login_user(token_body.id)) == signature
            request.ctx.new_token = None

            if sign_in_redis and renewable:
                new_token_body: dict = token_body.dict()
                new_token_body["exp"] = current_ts + TOKEN_PERIOD
                new_token: str = create(new_token_body)
                # print("new token = {}".format(new_token))
                redis.set(RedisKey.login_user_temp(token_body.id), signature, ex=10)
                redis.set(RedisKey.login_user(token_body.id), new_token.split('.')[2], ex=TOKEN_PERIOD)
                request.ctx.token_body = token_body
                request.ctx.new_token = new_token
                return await f(request, *args, **kwargs)
            elif sign_in_redis:
                request.ctx.token_body = token_body
                return await f(request, *args, **kwargs)

            if renewable:
                sign_in_redis_temp: bool = redis.get(RedisKey.login_user_temp(token_body.id)) == signature
                if sign_in_redis_temp:
                    request.ctx.token_body = token_body
                    return await f(request, *args, **kwargs)

            raise UnAuthorizedException('token expired')
        return decorated_function
    return decorator
