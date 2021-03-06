import os
from sanic import Request
from model.page_model import Page
from model.register_model import RegisterModel
from model.user_model import User
from sql import user_sql
from util import encrypt, jwt_util
from util.common import response_ok, response_error


class UserService:
    def __init__(self):
        from util.aiodb_util import db
        self.__db = db
        self.__salt1 = os.getenv('SALT1')

    async def register(self, user: RegisterModel) -> dict:
        data = user.dict()
        encrypt_pwd = encrypt.md5("{}:{}".format(data['password'], self.__salt1))
        updated_rows = await self.__db.insert_or_update(sql=user_sql.REGISTER,
                                                        params=[data['name'], encrypt_pwd, data['email']])
        if updated_rows is 0:
            return response_error(3, 'account or email is used')
        return response_ok()

    async def login(self, body: User) -> dict:
        data_tuple = await self.__db.query_once(sql=user_sql.GET_USER_INFO_BY_NAME, params=[body.name])
        if len(data_tuple) == 0:
            return response_error(2, 'invalid login info')
        pwd_in_db = data_tuple[0].pop('password', None)
        if pwd_in_db != encrypt.md5("{}:{}".format(body.password, self.__salt1)):
            return response_error(2, 'invalid login info')
        else:
            body.id = data_tuple[0]["id"]
            body.email = data_tuple[0]['email']
            body_dict = body.dict()
            body_dict.pop("password", None)
            data_tuple[0]['token'] = jwt_util.create_and_store_redis(body_dict)
            return response_ok(data_tuple[0])

    async def get_users_list(self, request: Request, page: Page) -> dict:
        data: tuple = await self.__db.query_once(sql=user_sql.GET_USERS_INFO, params=[page.offset(), page.size])
        return response_ok(data=data, new_token=request.ctx.new_token)

    async def get_user_by_id(self, request: Request, user_id: int) -> dict:
        data: tuple = await self.__db.query_once(sql=user_sql.GET_USER_INFO, params=[user_id])
        if len(data) == 0:
            return response_error(1, 'resource not found')
        return response_ok(data=data[0], new_token=request.ctx.new_token)


user_service = UserService()
