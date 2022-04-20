from sanic import Blueprint, json, Request, response
from model.order_model import OrderList
from service.order_sv import order_service
from util.my_decorators import list_body_validator, authorized

orders_bp = Blueprint("orders_bp", url_prefix="/orders")


@orders_bp.route("", methods=['POST'])
@list_body_validator(clz=OrderList)
@authorized()
async def create_order(request: Request, items: list) -> response:
    print('items = {}'.format(items))
    return json(await order_service.create_order(items, request.ctx.token_body))


@orders_bp.route("", methods=['GET'])
async def get_products(request: Request) -> response:
    return json(await order_service.get_products([1, 3, 7]))
