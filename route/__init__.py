from sanic import Blueprint
from route.user_bp import users_bp
from route.system_bp import system_bp


def get_bps():
    return Blueprint.group(users_bp, system_bp, url_prefix="/rabbit")
