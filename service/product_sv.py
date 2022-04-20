from typing import Union
from sql import product_sql
from util.common import response_ok


class ProductService:
    def __init__(self):
        from util.aiodb_util import db
        self.__db = db

    async def get_products(self, ids: Union[list, tuple]):
        query_data = await self.__db.select_in(sql=product_sql.GET_PRODUCT_BY_IDS, params=ids)
        return response_ok(data=query_data)


product_service = ProductService()
