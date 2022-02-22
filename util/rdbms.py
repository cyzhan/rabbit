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
                                   cursorclass=DictCursor, conv=conv)
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


db = MyDBUtil()
