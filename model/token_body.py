from pydantic import BaseModel


class TokenBody(BaseModel):
    id: int
    name: str
    email: str
    exp: int

