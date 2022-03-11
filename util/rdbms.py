import MySQLdb
from MySQLdb import converters
from dbutils.pooled_db import PooledDB
from MySQLdb.cursors import DictCursor
import os


class MyDBUtil:

    def __init__(self):
        try:
            conv = converters.conversions.copy()
            # break below line to check type conv
            conv[246] = float  # convert decimals to floats
            conv[10] = str  # convert dates to strings
            conv[7] = str  # convert datetime to strings
            self.__pool = PooledDB(creator=MySQLdb, mincached=1, maxcached=5, host=os.getenv("DB_HOST"),
                                   user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"), db='rabbit', port=3306,
                                   cursorclass=DictCursor, conv=conv, autocommit=True)
            print('MyDBUtil object created')
        except Exception as e:
            print(e)

    async def query_once(self, sql, params):
        cnx = self.__pool.connection()
        cursor = cnx.cursor()
        try:
            count = cursor.execute(sql, params)
            print('query_one find = {}'.format(count))
            return cursor.fetchall()
        finally:
            cursor.close()
            cnx.close()

    async def insert(self, sql, params):
        cnx = self.__pool.connection()
        cursor = cnx.cursor()
        try:
            affect_row_count = cursor.execute(sql, params)
            cnx.commit()
            return affect_row_count
        except Exception as e:
            cnx.rollback()
            raise e
        finally:
            cursor.close()
            cnx.close()

    def get_cnx(self):
        return self.__pool.connection()


db = MyDBUtil()


def transaction(func):
    async def wrapper(*args, **kwargs):
        conn = db.get_cnx()
        conn.autocommit = False
        try:
            result = await func(*args, **kwargs, conn=conn)
            conn.commit()
            return result
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.cursor().close()
            conn.autocommit = True
            conn.close()
    return wrapper


async def query(sql: str, params, conn) -> tuple:
    cursor = conn.cursor()
    try:
        count = cursor.execute(sql, params)
        print('fetch rows = {}'.format(count))
        return cursor.fetchall()
    finally:
        cursor.close()


async def execute(sql: str, params, conn) -> int:
    cursor = conn.cursor()
    try:
        return cursor.execute(sql, params)
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()


async def insert_and_get_last_id(sql: str, params, conn) -> int:
    cursor = conn.cursor()
    try:
        updated_row: int = cursor.execute(sql, params)
        if updated_row is 0:
            raise Exception('insert error')
        return cursor.lastrowid
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()


async def batch_insert(sql: str, params, conn) -> int:
    cursor = conn.cursor()
    try:
        # return cursor.execute(sql, params)
        return cursor.executemany(sql, params)
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
