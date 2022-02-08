from sanic import Blueprint
from sanic import Request, response
from sanic.response import json
from sanic_ext import validate
from model.user_model import User
from util import encrypt
from util.my_decorators import body_validator
from util.rdbms import db
from sql.user_script import UserSql
from util.common import response_ok, response_ok_of

users_bp = Blueprint("users_bp", url_prefix="/users")
SALT = "f93tnlay1FSk3LF03nf&Zmhr"


@users_bp.route("", methods=['POST'])
# @validate(json=User)
@body_validator(clz=User)
async def register(request: Request, body: User) -> response:
    data = body.dict()
    encrypt_pwd = encrypt.md5(SALT + ':' + data['password'])
    updated_rows = await db.insert(UserSql.REGISTER, [data['name'], encrypt_pwd, data['email']])
    print("updated row = {}".format(updated_rows))
    return response_ok


@users_bp.route("/login", methods=['POST'])
@body_validator(clz=User)
async def login(request: Request, body: User) -> response:
    # print(body)
    data_tuple = await db.query_once(UserSql.GET_USER_INFO_BY_NAME, [body.name])
    if len(data_tuple) == 0:
        print("1")
        return json({'code': 40002, 'msg': 'account or password error'})
    pwd_in_db = data_tuple[0].pop('password', None)
    print('pwd in db = {}'.format(pwd_in_db))
    print('body.password = {}'.format(encrypt.md5(SALT + ':' + body.password)))
    if pwd_in_db == encrypt.md5(SALT + ':' + body.password):
        return response_ok_of(data_tuple[0])
    print("2")
    return json({'code': 40002, 'msg': 'account or password error'})


@users_bp.route("", methods=['GET'])
async def get_users_list(request: Request) -> response:
    login_obj = request.json
    return response_ok


@users_bp.route("/<user_id:int>", methods=['GET'])
async def get_user_by_id(request: Request, user_id: int) -> response:
    print("user_id = {}".format(user_id))
    data_tuple = await db.query_once(UserSql.GET_USER_INFO, [user_id])
    if len(data_tuple) == 0:
        return json({'code': 40001, 'msg': 'no data'})
    return response_ok_of(data_tuple[0])


@users_bp.route("/<user_id:int>", methods=['PUT'])
async def update_users_info(request: Request, user_id: int) -> response:
    # login_obj = request.json
    return response_ok
