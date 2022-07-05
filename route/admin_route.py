from sanic import Blueprint, Request, response, json

admin_bp = Blueprint("admin_bp", url_prefix="/admin")


@admin_bp.route("/menu", methods=['GET'])
async def get_menu(request: Request) -> response:
    return json({'code': 0, 'msg': 'ok', 'data': [
        {'menuId': 10, 'name': '會員'}
    ]})
