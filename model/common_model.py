from typing import List
from pydantic import BaseModel


class IntegerList(BaseModel):
    items: List[int]
