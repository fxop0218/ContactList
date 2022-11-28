from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str
    telephone: int
    owner: int

    class Config:
        orm_mode = True
