from pydantic import BaseModel
from typing import List


class User(BaseModel):
    user_id: int
    name: str
    email: str
    role: str


class UserList(BaseModel):
    user_list: List[User]
