from typing import Union
from model.page_model import Page
from sql import product_sql
from util.common import response_ok


class ProductService:
    def __init__(self):
        from util.aiodb_util import db
        self.__db = db

    async def get_products(self, page: Page, ids: Union[list, tuple]):
        sql_component = ['SELECT a.id, a.price, a.quantity FROM rabbit.product AS a']
        args = []
        if ids is not None and len(ids) > 0:
            ary = []
            where_clause = 'WHERE a.id IN ({})'
            for item in ids:
                ary.append('%s')
                args.append(item)
            sql_component.append(where_clause.format(','.join(ary)))
            sql_component.append('AND a.active = 1')
        else:
            sql_component.append('WHERE a.active = 1')
        sql_component.append('LIMIT %s,%s')
        args.append(page.offset())
        args.append(page.size)
        sql = " ".join(sql_component)
        print(sql)
        query_data = await self.__db.select_in(sql=" ".join(sql_component), params=args)
        return response_ok(data=query_data)


product_service = ProductService()
