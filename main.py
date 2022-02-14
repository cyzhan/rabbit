from dotenv import load_dotenv
from sanic import Sanic
import os


def create_app():
    app = Sanic("rabbit")

    from route import get_bps
    app.blueprint(get_bps())

    # app.error_handler.add(ValidationError, custom_validation_handler)
    return app


if __name__ == '__main__':
    load_dotenv()
    create_app().run(host='127.0.0.1', port=os.getenv("SERVER_PORT"))


