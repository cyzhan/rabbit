from pydantic import BaseModel, validator
from typing import Optional


class Page(BaseModel):
    index: int
    size: int
    # offset: Optional[int] = None

    @validator('index')
    def index_rules(value, values, config, field):
        if value < 0:
            raise ValueError('index must greater than 0')
        return value

    @validator('size')
    def seize_rules(value, values, config, field):
        return value
        # if value > 50:
        #     return 50
        # if value < 5:
        #     return 5

    def offset(self):
        return (self.index - 1)*self.size
