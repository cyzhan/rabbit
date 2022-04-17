import asyncio
from dotenv import load_dotenv
from sanic import Sanic, json, app
import os
from exception.logic_error_exception import LogicErrorException
from exception.unauthorized_exception import UnAuthorizedException


def create_app():
    app = Sanic("rabbit")

    from route import get_bps
    app.blueprint(get_bps())

    app.error_handler.add(UnAuthorizedException, unauthorized_access)
    app.error_handler.add(LogicErrorException, catch_logic_error)
    app.error_handler.add(Exception, catch_anything)
    # app.add_task(notify_server_started_after_five_seconds())

    @app.listener('before_server_start')
    def init(sanic, loop):
        if loop is None:
            print('loop is none')
        print('before start')
        # global sem
        # concurrency_per_worker = 4
        # sem = asyncio.Semaphore(concurrency_per_worker, loop=loop)

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


async def notify_server_started_after_five_seconds():
    await asyncio.sleep(5)
    print('Server successfully started!')
    loop = asyncio.get_running_loop()
    print('loop get !')


# @app.listener('before_server_start')
# def init(sanic, loop):
#     print('before start')


if __name__ == '__main__':
    load_dotenv()
    create_app().run(host='127.0.0.1', port=os.getenv("SERVER_PORT"))

