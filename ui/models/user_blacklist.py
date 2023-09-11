from pydantic import BaseModel


class UserBlacklist(BaseModel):
    users: list = []
