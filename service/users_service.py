# from sanic import Request, response, Sanic
# from model.user_model import User
# from route.user_bp import SALT1
# from sql.user_script import UserSql
# from util import encrypt
# from util.common import response_ok
# from util.rdbms import MyDBUtil


# class UserService:
#     def __init__(self, db: MyDBUtil, app: Sanic):
#         self.__db = db
#         self.__salt1 = salt1
#
#     async def register(self, request: Request, body: User) -> response:
#         data = body.dict()
#         encrypt_pwd = encrypt.md5("{}:{}".format(data['password'], self.__salt1))
#         updated_rows = self.__db.insert(UserSql.REGISTER, [data['name'], encrypt_pwd, data['email']])
#         print("updated row = {}".format(updated_rows))
#         return response_ok
