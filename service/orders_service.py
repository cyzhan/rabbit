from typing import Union
from model.token_body import TokenBody
from util import rdbms
from util.common import response_ok, response_error
from util.rdbms import transaction
from sql import product_sql, user_sql, order_sql, common_sql


@transaction
async def create_order(items: list, token_body: TokenBody, conn):
    # token_body = request.ctx.token_body
    holder = []
    ids = []
    for item in items:
        ids.append(item.productId)
        holder.append('%s')
    s = ','.join(holder)
    dynamic_script = product_sql.SELECT_PRODUCT_FOR_UPDATE.format(s)
    query_result = await rdbms.db.query_once(dynamic_script, ids)
    bill_amount = 0
    for item in items:
        for product in query_result:
            if item.productId != product['id']:
                continue
            left_quantity = product['quantity'] - item.quantity
            if left_quantity < 0:
                return response_error(9, 'product id: {}, quantity is not sufficient, order quantity: {}, '
                                         'storage quantity: {}'.format(item.productId, item.quantity,
                                                                       product['quantity']))

            print('product id: {}, total: {}'.format(item.productId, item.quantity*product['price']))
            await rdbms.execute(sql=product_sql.UPDATE_PRODUCT_FOR_QUANTITY,
                                params=[left_quantity, item.productId],
                                conn=conn)
            bill_amount = bill_amount + item.quantity*product['price']
            break

    print('bill_amount = {}'.format(bill_amount))

    update_row = await rdbms.execute(sql=user_sql.UPDATE_USER_BALANCE_ON_PURCHASE,
                                     params=[bill_amount, token_body.id, bill_amount],
                                     conn=conn)
    if update_row == 0:
        return response_error(9, 'insufficient balance')
    print('update user balance row count = {}'.format(update_row))
    last_insert_order_id = await rdbms.insert_and_get_last_id(sql=order_sql.INSERT_ORDER_MAIN,
                                                              params=[bill_amount, 1],
                                                              conn=conn)

    print('last_insert_order_id = {}'.format(last_insert_order_id))

    data = []
    for item in items:
        data.append((last_insert_order_id, item.productId, item.quantity))
    sql: str = '''
    INSERT INTO rabbit.order_detail
    (order_id, product_id, price, quantity, created_time, updated_time)
    VALUES(%s, %s, 10, %s, current_timestamp(), current_timestamp())
    '''
    insert_rows = await rdbms.batch_insert(sql, data, conn)
    print('insert_rows = {}'.format(insert_rows))

    return response_ok(data={'billAmount': bill_amount, 'orderNo': last_insert_order_id})


async def select_products(ids: Union[list, tuple]):
    data = [1, 3, 7]
    val = []
    for i in data:
        val.append('%s')

    s = ','.join(val)
    dynamic_script = product_sql.GET_PRODUCT_BY_IDS.format(s)
    query_data = await rdbms.db.query_once(dynamic_script, data)
    return response_ok(data=query_data)
