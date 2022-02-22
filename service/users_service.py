from sanic import Request, response
import os
from model.page_model import Page
from model.user_model import User
from sql.user_script import UserSql
from sanic.response import json
from util import encrypt, jwt_util
from util.common import response_ok, response_ok_of


class UserService:
    def __init__(self):
        from util.rdbms import db
        self.__db = db
        self.__salt1 = os.getenv('SALT1')

    async def register(self, user: User) -> response:
        data = user.dict()
        encrypt_pwd = encrypt.md5("{}:{}".format(data['password'], self.__salt1))
        updated_rows = await self.__db.insert(UserSql.REGISTER, [data['name'], encrypt_pwd, data['email']])
        print("rabbit.user updated row = {}".format(updated_rows))
        return response_ok

    async def login(self, body: User):
        data_tuple = await self.__db.query_once(UserSql.GET_USER_INFO_BY_NAME, [body.name])
        if len(data_tuple) == 0:
            return json({'code': 2, 'msg': 'account or password error'})
        pwd_in_db = data_tuple[0].pop('password', None)
        if pwd_in_db != encrypt.md5("{}:{}".format(body.password, self.__salt1)):
            return json({'code': 2, 'msg': 'account or password error'})
        else:
            body.id = data_tuple[0]["id"]
            body_dict = body.dict()
            body_dict.pop("password", None)
            return json({'code': 0, 'msg': "ok",
                         "data": data_tuple[0], 'token': jwt_util.create_and_store_redis(body_dict)})

    async def get_users_list(self, page: Page):
        data: tuple = await self.__db.query_once(UserSql.GET_USERS_INFO, [page.offset(), page.size])
        return response_ok_of(data)

    async def get_user_by_id(self, user_id: int):
        data: tuple = await self.__db.query_once(UserSql.GET_USER_INFO, [user_id])
        if len(data) == 0:
            return json({'code': 1, 'msg': 'request data is not found'})
        return response_ok_of(data[0])


user_service = UserService()
