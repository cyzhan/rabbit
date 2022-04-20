from sanic import Blueprint
from route.products_route import products_bp
from route.orders_route import orders_bp
from route.users_route import users_bp
from route.system_route import system_bp


def get_bps():
    return Blueprint.group(users_bp,
                           system_bp,
                           orders_bp,
                           products_bp,
                           url_prefix="/rabbit")
