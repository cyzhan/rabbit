GET_USER_INFO = '''
select a.id, a.name, a.email, a.balance, a.created_time AS createdTime, a.updated_time AS updatedTime 
from rabbit.user AS a where id = %s
'''

REGISTER = '''
INSERT INTO rabbit.`user`
(name, password, email, balance, created_time, updated_time)
VALUES(%s, %s, %s, 0.00, current_timestamp(), current_timestamp())
'''

GET_USER_INFO_BY_NAME = '''
select a.id, a.name, a.password, a.email, a.balance, a.created_time AS createdTime, a.updated_time AS updatedTime 
from rabbit.user AS a where a.name = %s
'''

GET_USERS_INFO = '''
select a.id, a.name, a.email, a.balance, a.created_time AS createdTime, a.updated_time AS updatedTime 
from rabbit.user AS a LIMIT %s,%s
'''


UPDATE_USER_BALANCE_ON_PURCHASE = '''
UPDATE rabbit.`user` AS a
SET a.balance = a.balance - %s
WHERE a.id = %s AND ((a.balance - %s)>=0)
'''


def get_users_info(user_ids: list, order_by: str):
    template: str = '''
    SELECT a.id, a.name, a.email, a.balance, a.created_time AS createdTime, a.updated_time AS updatedTime 
    FROM rabbit.user AS a
    {} 
    LIMIT %s,%s
    '''
    if user_ids is None:
        return template.format('')
    if len(user_ids) <= 0:
        return template.format('')
    where_sql = 'WHERE a.id in ({})'.format(','.join(user_ids))
    string = template.format(where_sql)
    print(string)
    return string
