from sanic import Blueprint
from .user_bp import users_bp
from .system_bp import system_bp

api = Blueprint.group(users_bp, system_bp, url_prefix="/rabbit")
