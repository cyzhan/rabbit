from typing import Optional
from pydantic import BaseModel, validator
import re


class User(BaseModel):
    id: Optional[int]
    name: str
    email: str
    password: str

    @validator('password')
    def password_rules(value, values, config, field):
        if len(value) < 8:
            raise ValueError('password too short')
        if len(set(value)) <= 3:
            raise ValueError('password too simple')
        return value

    @validator('name')
    def name_rules(value, values, config, field):
        p = re.compile('[^A-Za-z0-9]')
        if len(value) < 6 or len(value) > 15:
            raise ValueError('invalid length')
        if len(set(value)) <= 2:
            raise ValueError('too simple')
        if p.search(value) != None:
            raise ValueError('invalid character')
        return value
