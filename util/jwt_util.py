import base64
import hashlib
import hmac
import os
import time
from sanic import Request
from exception.unauthorized_exception import UnAuthorizedException
import ujson
from model.token_body import TokenBody
from util.redis_util import r as redis
from util.redis_util import RedisKey

SALT2 = os.getenv("SALT2")
TOKEN_PERIOD = int(os.getenv("TOKEN_PERIOD"))
RENEW_MARGIN = int(os.getenv("RENEW_MARGIN"))
JWT_HEADER = '{"alg":"HS256","typ":"JWT"}'


def login_verify(request: Request):
    token = request.headers["Authorization"]
    if token is None:
        raise UnAuthorizedException('unauthorized')
    else:
        return verify(token)


def verify(jwt: str) -> TokenBody:
    ary = jwt.split('.')
    string = "{}.{}".format(ary[0], ary[1])
    raw = hmac.new(bytes(SALT2, encoding="utf-8"), bytes(string, encoding="utf-8"), digestmod=hashlib.sha256).digest()
    signature = str(base64.urlsafe_b64encode(raw), 'utf-8').split("=")[0]
    print("signature = {}", signature)
    if signature != ary[2]:
        raise UnAuthorizedException('unauthorized signature')

    length: int = len(ary[1])
    s = ary[1] + '=' * (4 - length % 4)
    body_dict = ujson.loads(base64.b64decode(s))
    token_body = TokenBody(**body_dict)
    current_ts = int(time.time())
    if current_ts > token_body.exp:
        raise UnAuthorizedException('token expired')
    renewable: bool = current_ts > (token_body.exp - RENEW_MARGIN)
    sign_in_redis: bool = redis.get(RedisKey.login_user(token_body.id)) == signature
    print("renewable = {}, sign_in_redis = {}".format(renewable, sign_in_redis))
    if sign_in_redis and renewable:
        body_dict["exp"] = current_ts + TOKEN_PERIOD
        new_token: str = create(body_dict)
        print("new_token = {}".format(new_token))
        redis.set(RedisKey.login_user_temp(token_body.id), signature, ex=10)
        redis.set(RedisKey.login_user(token_body.id), new_token.split('.')[2], ex=TOKEN_PERIOD)
        return token_body
    elif sign_in_redis:
        return token_body

    if renewable:
        sign_in_redis_temp: bool = redis.get(RedisKey.login_user_temp(token_body.id)) == signature
        if sign_in_redis_temp:
            return token_body
        else:
            raise UnAuthorizedException('abcd')
    else:
        raise UnAuthorizedException('efgh')


# do signature verify and expire time check
def verify2(jwt: str) -> TokenBody:
    ary = jwt.split('.')
    string = "{}.{}".format(ary[0], ary[1])
    raw = hmac.new(bytes(SALT2, encoding="utf-8"), bytes(string, encoding="utf-8"), digestmod=hashlib.sha256).digest()
    signature = str(base64.urlsafe_b64encode(raw), 'utf-8').split("=")[0]
    if signature != ary[2]:
        raise UnAuthorizedException('unauthorized signature')

    length: int = len(ary[1])
    s = ary[1] + '=' * (4 - length % 4)
    body_dict = ujson.loads(base64.b64decode(s))
    token_body = TokenBody(**body_dict)
    current_ts = int(time.time())
    if current_ts > token_body.exp:
        raise UnAuthorizedException('token expired')
    return token_body


def create(user_dict: dict) -> str:
    ts = time.time()
    # 取整數
    user_dict['exp'] = int(ts) + TOKEN_PERIOD
    ary = []
    encoded_bytes = base64.urlsafe_b64encode(JWT_HEADER.encode("utf-8"))
    encode_jwt_header = str(encoded_bytes, "utf-8")
    ary.append(encode_jwt_header)

    token_body_string = ujson.dumps(user_dict)
    # Remove any trailing '='s
    encode_jwt_body = str(base64.urlsafe_b64encode(token_body_string.encode("utf-8")), 'utf-8').split("=")[0]
    ary.append(encode_jwt_body)

    string = "{}.{}".format(encode_jwt_header, encode_jwt_body)
    print("string = {}".format(string))
    raw = hmac.new(bytes(SALT2, encoding="utf-8"), bytes(string, encoding="utf-8"), digestmod=hashlib.sha256).digest()
    signature = str(base64.urlsafe_b64encode(raw), 'utf-8').split("=")[0]  # Remove any trailing '='s

    ary.append(signature)
    return '.'.join(ary)


def create_and_store_redis(user_dict: dict) -> str:
    jwt: str = create(user_dict)
    redis.set(RedisKey.login_user(user_dict["id"]), jwt.split(".")[2], ex=TOKEN_PERIOD)
    return jwt
