import MySQLdb
from dbutils.pooled_db import PooledDB, SharedDBConnection
from MySQLdb.cursors import DictCursor

pool = PooledDB(creator=MySQLdb, mincached=1, maxcached=5, host='127.0.0.1', user='root', password='4qwer',
                db='rbmq', port=3306, cursorclass=DictCursor)


