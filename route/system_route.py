from sanic import Blueprint, response
from sanic.response import json
from sanic import Request

system_bp = Blueprint("system_bp", url_prefix="/system")


@system_bp.route("/version")
async def get_version(request: Request) -> response:
    return json({'version': 'v0.1.0'})


@system_bp.route("/pydantic-test")
async def pydantic_test(request: Request) -> response:
    return json({'version': 'v0.1.0'})
