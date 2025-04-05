from pydantic import BaseModel
from typing import List

class Constraint(BaseModel):
    instructor: str
    availability: List[str]
