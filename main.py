from dotenv import load_dotenv
from sanic import Sanic, json
import os

from exception.UnAuthorizedException import UnAuthorizedException


def create_app():
    app = Sanic("rabbit")

    from route import get_bps
    app.blueprint(get_bps())

    app.error_handler.add(Exception, catch_anything)
    app.error_handler.add(UnAuthorizedException, unauthorized_access)
    return app


def catch_anything(request, exception):
    print(str(exception))
    return json({"code": 1, "msg": "internal server error"}, status=500)


def unauthorized_access(request, e):
    print(e.to_dict())
    return json({"code": 1, "msg": "unauthorized"}, status=401)


if __name__ == '__main__':
    load_dotenv()
    create_app().run(host='127.0.0.1', port=os.getenv("SERVER_PORT"))


