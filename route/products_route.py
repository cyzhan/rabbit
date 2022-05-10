from sanic import Blueprint, Request, response, json

from model.common_model import IntegerList
from model.page_model import Page
from service.product_sv import product_service
from util.my_decorators import authorized, list_body_validator

products_bp = Blueprint("products_bp", url_prefix="/products")


@products_bp.route("", methods=['GET'])
@authorized()
async def get_products(request: Request) -> response:
    page = Page(index=request.args.get("pageIndex"), size=request.args.get("pageSize"))
    ids: list = request.args.getlist('id')
    return json(await product_service.get_products(page=page, ids=ids))
