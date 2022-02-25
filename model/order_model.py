from typing import List

from pydantic import BaseModel


class Order(BaseModel):
    productId: int
    quantity: int


class OrderList(BaseModel):
    items: List[Order]
