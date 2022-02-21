from sanic import Blueprint
from sanic import Request, response
from sanic.response import json
from model.page_model import Page
from model.password_model import Password
from model.user_model import User
from util import encrypt
from util.my_decorators import body_validator, authorized
from sql.user_script import UserSql
from util.common import response_ok, response_ok_of
import os
from util.rdbms import db
from util import jwt_util

users_bp = Blueprint("users_bp", url_prefix="/users")
SALT1 = os.getenv("SALT1")


@users_bp.route("", methods=['POST'])
# @validate(json=User)
@body_validator(clz=User)
async def register(request: Request, body: User) -> response:
    data = body.dict()
    encrypt_pwd = encrypt.md5("{}:{}".format(data['password'], SALT1))
    updated_rows = await db.insert(UserSql.REGISTER, [data['name'], encrypt_pwd, data['email']])
    print("updated row = {}".format(updated_rows))
    return response_ok


@users_bp.route("/login", methods=['POST'])
@body_validator(clz=User)
async def login(request: Request, body: User) -> response:
    data_tuple = await db.query_once(UserSql.GET_USER_INFO_BY_NAME, [body.name])
    if len(data_tuple) == 0:
        return json({'code': 2, 'msg': 'account or password error'})
    pwd_in_db = data_tuple[0].pop('password', None)
    if pwd_in_db != encrypt.md5("{}:{}".format(body.password, SALT1)):
        return json({'code': 2, 'msg': 'account or password error'})
    else:
        body.id = data_tuple[0]["id"]
        body_dict = body.dict()
        body_dict.pop("password", None)
        return json({'code': 0, 'msg': "ok",
                     "data": data_tuple[0], 'token': jwt_util.create_and_store_redis(body_dict)})


@users_bp.route("", methods=['GET'])
async def get_users_list(request: Request) -> response:
    page = Page(index=request.args.get("pageIndex"), size=request.args.get("pageSize"))
    data_tuple = await db.query_once(UserSql.GET_USERS_INFO, [page.offset(), page.size])
    return response_ok_of(data_tuple)


@users_bp.route("/<user_id:int>", methods=['GET'])
@authorized()
async def get_user_by_id(request: Request, user_id: int) -> response:
    # jwt = request.headers["Authorization"]
    # token_body = jwt_util.verify(jwt)
    token_body = request.ctx.token_body
    print("id:{},name:{}".format(token_body.id, token_body.name))
    data_tuple = await db.query_once(UserSql.GET_USER_INFO, [user_id])
    if len(data_tuple) == 0:
        return json({'code': 1, 'msg': 'request data is not found'})
    return response_ok_of(data_tuple[0])


@users_bp.route("/<user_id:int>", methods=['PUT'])
async def update_users_info(request: Request, user_id: int) -> response:
    # login_obj = request.json
    return response_ok


@users_bp.route("/password/<user_id:int>", methods=['PATCH'])
@body_validator(clz=Password)
@authorized()
async def update_user_password(request: Request, body: Password, user_id: int) -> response:
    # login_obj = request.json
    print("user_id: {}, password: {}, confirm_password: {}".format(user_id, body.password, body.confirmPassword))
    return response_ok
