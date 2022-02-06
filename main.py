from pydantic import ValidationError
from sanic import Sanic, Request
from sanic.response import json
from route import api


app = Sanic("rabbit")
app.blueprint(api)


# async def custom_validation_handler(request, exception):
#     return json({
#         'code': 40000,
#         'msg': "dfsadf"
#     }, status=400)
#
#
# app.error_handler.add(ValidationError, custom_validation_handler)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8005)


