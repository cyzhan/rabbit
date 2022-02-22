class UserSql:
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