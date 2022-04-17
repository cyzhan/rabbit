from dotenv import load_dotenv
from sanic import Sanic, json
import os
from exception.logic_error_exception import LogicErrorException
from exception.unauthorized_exception import UnAuthorizedException
from util.aiodb_util import db

load_dotenv()


def create_app():
    app = Sanic("rabbit")

    from route import get_bps
    app.blueprint(get_bps())

    app.error_handler.add(UnAuthorizedException, unauthorized_access)
    app.error_handler.add(LogicErrorException, catch_logic_error)
    app.error_handler.add(Exception, catch_anything)
    app.register_listener(on_start, 'after_server_start')

    return app


def catch_anything(request, exception):
    print(str(exception))
    return json({"code": 1, "msg": "internal server error"}, status=500)


def unauthorized_access(request, e):
    print(e.to_dict())
    return json({"code": 1, "msg": "unauthorized"}, status=401)


def catch_logic_error(request, e):
    print(e.to_dict)
    return json({"code": e.code, "msg": e.msg}, status=500)


async def on_start(sanic_app, loop):
    await db.create_pool(loop=loop)


if __name__ == '__main__':
    create_app().run(host='127.0.0.1', port=os.getenv("SERVER_PORT"))

