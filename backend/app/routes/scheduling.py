from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from typing import List

router = APIRouter()


class Constraint(BaseModel):
    instructor: str
    availability: List[str]


@router.post("/constraints")
def set_constraints(constraints: List[Constraint]):
    return {"status": "Constraints received"}


@router.post("/generate")
def generate_schedule():
    dummy_schedule = [
        {
            "course": "CS101",
            "instructor": "Dr. Smith",
            "room": "A1",
            "timeslot": "Mon 10:00",
        },
        {
            "course": "MA201",
            "instructor": "Prof. Jones",
            "room": "B2",
            "timeslot": "Tue 14:00",
        },
    ]
    return dummy_schedule


@router.get("/schedule")
def get_schedule():
    return generate_schedule()


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    return {"filename": file.filename}
