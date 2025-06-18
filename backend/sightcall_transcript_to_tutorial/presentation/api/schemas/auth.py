from pydantic import BaseModel


class UserSchema(BaseModel):
    id: str
    name: str


class AuthResponseSchema(BaseModel):
    jwt: str
    user: UserSchema
