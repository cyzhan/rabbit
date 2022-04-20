from decimal import Decimal
from typing import Union
from exception.logic_error_exception import LogicErrorException
from model.token_body import TokenBody
from util.common import response_ok
from sql import product_sql, user_sql, order_sql
from util.aiodb_util import cursor_inject


class OrderService:
    def __init__(self):
        from util.aiodb_util import db
        self.__db = db

    @cursor_inject
    async def create_order(self, items: list, token_body: TokenBody, cursor):
        # token_body = request.ctx.token_body
        holder = []
        ids = []
        for item in items:
            ids.append(item.productId)
            holder.append('%s')
        s = ','.join(holder)
        dynamic_script = product_sql.SELECT_PRODUCT_FOR_UPDATE.format(s)
        fetch_count: int = await cursor.execute(dynamic_script, ids)
        query_result = await cursor.fetchall()
        bill_amount = 0
        for item in items:
            for product in query_result:
                if item.productId != product['id']:
                    continue
                if Decimal(item.price) != product['price']:
                    raise LogicErrorException(code=41, msg='price is not match. id: {}'.format(product['id']))
                left_quantity = product['quantity'] - item.quantity
                if left_quantity < 0:
                    raise LogicErrorException(4, 'product id: {}, insufficient quantity'.format(item.productId))

                await cursor.execute(product_sql.UPDATE_PRODUCT_FOR_QUANTITY, [left_quantity, item.productId])
                bill_amount = bill_amount + item.quantity * product['price']
                break

        update_row = await cursor.execute(user_sql.UPDATE_USER_BALANCE_ON_PURCHASE,
                                          [bill_amount, token_body.id, bill_amount])
        if update_row == 0:
            raise LogicErrorException(5, 'insufficient balance')

        await cursor.execute(order_sql.INSERT_ORDER_MAIN, [token_body.id, bill_amount, 1])
        last_insert_order_id = cursor.lastrowid

        data = []
        for item in items:
            data.append((last_insert_order_id, item.productId, item.price, item.quantity))
        insert_rows = await cursor.executemany(order_sql.INSERT_ORDER_DETAIL, data)

        return response_ok(data={'billAmount': bill_amount, 'orderNo': last_insert_order_id})

    async def get_products(self, ids: Union[list, tuple]):
        query_data = await self.__db.select_in(sql=product_sql.GET_PRODUCT_BY_IDS, params=ids)
        return response_ok(data=query_data)


order_service = OrderService()
