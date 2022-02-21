from pydantic import BaseModel, validator


class Password(BaseModel):
    password: str
    confirmPassword: str

    @validator('password')
    def password_rules(cls, value, values, config, field):
        if len(value) < 8:
            raise ValueError('password too short')
        if len(set(value)) <= 3:
            raise ValueError('password too simple')
        return value

    @validator('confirmPassword')
    def password_confirm_rules(cls, value, values, config, field):
        if value != values["password"]:
            raise ValueError('password and confirm_password is not equal')
        return value
