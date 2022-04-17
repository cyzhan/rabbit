import os
import aiomysql
from pymysql import converters


def cursor_inject(func) -> any:
    async def wrapper(*args, **kwargs):
        async with db.get_pool().acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                try:
                    result = await func(*args, **kwargs, cursor=cur)
                    await conn.commit()
                    return result
                except Exception as e:
                    await conn.rollback()
                    raise e
    return wrapper


class AioDBUtil:
    def __init__(self):
        self.__pool = None

    def get_pool(self):
        return self.__pool

    async def close_pool(self):
        self.__pool.close()
        await self.__pool.wait_closed()

    @cursor_inject
    async def query_once(self, sql: str, cursor, params=None) -> tuple:
        if params is None:
            params = []
        count: int = await cursor.execute(sql, params)
        print(f'fetch row count = {count}')
        return await cursor.fetchall()

    @cursor_inject
    async def insert_or_update(self, sql: str, cursor, params=None) -> int:
        if params is None:
            params = []
        count: int = await cursor.execute(sql, params)
        print(f'updated row = {count}')
        return count

    @cursor_inject
    async def insert_and_get_last_id(self, sql: str, cursor, params=None) -> int:
        updated_row: int = await cursor.execute(sql, params)
        if updated_row == 0:
            raise Exception('insert error')
        return cursor.lastrowid

    @cursor_inject
    async def batch_insert(self, sql: str, cursor, params=None) -> int:
        return await cursor.executemany(sql, params)

    async def create_pool(self, loop) -> None:
        if self.__pool is None:
            conv = converters.conversions.copy()
            conv[10] = str  # convert dates to strings
            conv[7] = str  # convert datetime to strings
            self.__pool = await aiomysql.create_pool(minsize=1, maxsize=5, host=os.getenv("DB_HOST"), port=3306,
                                                     user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"),
                                                     db='lottery', loop=loop, conv=conv, autocommit=False)
            print('mysql connection pool created')
        else:
            print('connection pool already exist')


db = AioDBUtil()




