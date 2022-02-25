from typing import Union
from model.token_body import TokenBody
from util import rdbms
from util.common import response_ok, response_error
from util.rdbms import transaction
from sql import product_sql, user_sql


@transaction
async def create_order(items: list, token_body: TokenBody, conn):
    # token_body = request.ctx.token_body
    holder = []
    ids = []
    for item in items:
        ids.append(item.productId)
        holder.append('%s')
    s = ','.join(holder)
    dynamic_script = product_sql.GET_PRODUCT_BY_IDS.format(s)
    query_result = await rdbms.db.query_once(dynamic_script, ids)
    bill_amount = 0
    for item in items:
        for product in query_result:
            if item.productId == product['id']:
                print('product id: {}, total: {}'.format(item.productId, item.quantity*product['price']))
                bill_amount = bill_amount + item.quantity*product['price']
                break

    print('bill_amount = {}'.format(bill_amount))

    update_row = rdbms.execute(sql=user_sql.UPDATE_USER_BALANCE_ON_PURCHASE,
                               params=[token_body.id, bill_amount, token_body.id], conn=conn)
    if update_row == 0:
        return response_error(9, 'insufficient money')


    data = []
    for item in items:
        data.append((item.productId, item.quantity))
    sql: str = '''
    INSERT INTO rabbit.order_detail
    (order_id, product_id, price, quantity, created_time, updated_time)
    VALUES(1, %s, 10, %s, current_timestamp(), current_timestamp())
    '''
    insert_rows = await rdbms.batch_insert(sql, data, conn)
    print('insert_rows = {}'.format(insert_rows))
    return response_ok(data={'insertRow': insert_rows})


async def select_products(ids: Union[list, tuple]):
    data = [1, 3, 7]
    val = []
    for i in data:
        val.append('%s')

    s = ','.join(val)
    dynamic_script = product_sql.GET_PRODUCT_BY_IDS.format(s)
    query_data = await rdbms.db.query_once(dynamic_script, data)
    return response_ok(data=query_data)
