from pydantic import BaseModel

class TimeslotBase(BaseModel):
    day: str
    time: str

class TimeslotCreate(TimeslotBase):
    pass

class TimeslotOut(TimeslotBase):
    id: int

    class Config:
        orm_mode = True
