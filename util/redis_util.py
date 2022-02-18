import os
import redis

r = redis.Redis(host=os.getenv("REDIS_HOST"), port=int(os.getenv("REDIS_PORT")), db=0,
                charset="utf-8", decode_responses=True)


class RedisKey:
    def __init__(self):
        print("ok")

    @staticmethod
    def login_user_temp(user_id: int) -> str:
        return "login_user_temp:{}".format(user_id)

    @staticmethod
    def login_user(user_id: int) -> str:
        return "login_user:{}".format(user_id)
