from pydantic import BaseModel

class InstructorBase(BaseModel):
    name: str

class InstructorCreate(InstructorBase):
    pass

class InstructorOut(InstructorBase):
    id: int

    class Config:
        orm_mode = True
