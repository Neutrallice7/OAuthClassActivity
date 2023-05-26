import datetime as _dt
import pydantic as _pydantic

class userBase(_pydantic.BaseModel):
    email: str

class userCreate(userBase):
    hashed_password :str

    class Config:
        orm_mode = True

class User(userBase):
    id: int

    class Config:
        orm_mode = True