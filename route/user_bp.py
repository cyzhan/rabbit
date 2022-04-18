from sanic import Blueprint, json
from sanic import Request, response
from model.page_model import Page
from model.password_model import Password
from model.register_model import RegisterModel
from model.user_model import User
from util.my_decorators import body_validator, authorized
from util.common import response_ok
from service.users_service import user_service

users_bp = Blueprint("users_bp", url_prefix="/users")


@users_bp.route("", methods=['POST'])
# @validate(json=User)
@body_validator(clz=RegisterModel)
async def register(request: Request, body: RegisterModel) -> response:
    return json(await user_service.register(user=body))


@users_bp.route("/login", methods=['POST'])
@body_validator(clz=User)
async def login(request: Request, body: User) -> response:
    return json(await user_service.login(body))


@users_bp.route("", methods=['GET'])
@authorized()
async def get_users_list(request: Request) -> response:
    page = Page(index=request.args.get("pageIndex"), size=request.args.get("pageSize"))
    return json(await user_service.get_users_list(request, page=page))


@users_bp.route("/<user_id:int>", methods=['GET'])
@authorized()
async def get_user_by_id(request: Request, user_id: int) -> response:
    # token_body = request.ctx.token_body
    # print("id:{},name:{}".format(token_body.id, token_body.name))
    return json(await user_service.get_user_by_id(request=request, user_id=user_id))


@users_bp.route("/<user_id:int>", methods=['PUT'])
async def update_users_info(request: Request, user_id: int) -> response:
    # login_obj = request.json
    return json(response_ok())


@users_bp.route("/password/<user_id:int>", methods=['PATCH'])
@body_validator(clz=Password)
@authorized()
async def update_user_password(request: Request, body: Password, user_id: int) -> response:
    # login_obj = request.json
    # print("user_id: {}, password: {}, confirm_password: {}".format(user_id, body.password, body.confirmPassword))
    return json(response_ok(new_token=request.ctx.new_token))
