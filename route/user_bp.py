from sanic import Blueprint
from sanic import Request, response
from sanic.response import json
from sanic_ext import validate
from model.user_model import User
from util.my_decorators import body_validator

users_bp = Blueprint("users_bp", url_prefix="/users")


@users_bp.route("", methods=['POST'])
@validate(json=User)
async def register(request: Request, body: User) -> response:
    my_obj = request.json
    print('name = {}, email = {}, password = {}'.format(my_obj['name'], my_obj['email'], my_obj['password']))
    return json({'code': 20000, 'msg': 'ok'})


@users_bp.route("/login", methods=['POST'])
@body_validator(clz=User)
async def login(request: Request, body: User) -> response:
    print(body)
    return json({'code': 20000, 'msg': 'ok'})


@users_bp.route("", methods=['GET'])
async def get_users_list(request: Request) -> response:
    login_obj = request.json
    return json({'code': 20000, 'msg': 'ok'})


@users_bp.route("/<user_id:int>", methods=['GET'])
async def get_user_by_id(request: Request, user_id: int) -> response:
    print("user_id = {}".format(user_id))
    return json({'code': 20000, 'msg': 'ok'})


@users_bp.route("/<user_id:int>", methods=['PUT'])
async def update_users_info(request: Request, user_id: int) -> response:
    login_obj = request.json
    return json({'code': 20000, 'msg': 'ok'})
